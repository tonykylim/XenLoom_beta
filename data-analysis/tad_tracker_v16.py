import cv2, sys, time, math, numpy, imutils, csv, os
from datetime import datetime
from psychopy import gui
import numpy as np
from collections import deque

# Video filename
filename = "18_D6_Control_trial1"
animalID, timepoint, treatment, trial = filename.split("_")
trial_num = int(trial[-1:])

# initialize some values
alpha = 8
beta = 0
ellipse_quality = 1.2
crossover_angle = 70
playback_speed = 1

# tracker type
tracker_types = ['home brew', 'CSRT']
tracker_type = tracker_types[0]

if tracker_type == 'CSRT':
    tracker = cv2.TrackerCSRT_create()
else:
    pass

# instantiate the dictionary
capture_data = []

# open the csv file associated with thie video and save it
with open(animalID + '_' + timepoint + '_' + treatment + '_whiteloom_timings.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        capture_data.append(row)

# timing data 
stim_start = float(capture_data[trial_num]['stim time'])
trial_start = float(capture_data[trial_num]['start'])
stim_time = stim_start - trial_start
videofps = float(capture_data[trial_num]['fps'])
stim_frame = int( stim_time * videofps )

# Read video
video = cv2.VideoCapture(filename + ".avi")

# Exit if video not opened
if not video.isOpened():
        print("Could not open video")
        sys.exit()

# Read first frame
ok, frame = video.read()
if not ok:
    print('Cannot read video file')
    sys.exit()

# clone the last frame

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
#video.set(cv2.CAP_PROP_POS_FRAMES, 0)
video.set(cv2.CAP_PROP_POS_FRAMES, 266)
#video.set(cv2.CAP_PROP_POS_FRAMES, frame_count-1)
ok, frame = video.read()

last_frame = frame.copy()
img_output = np.zeros((last_frame.shape[0], last_frame.shape[1], 3), np.uint8)
scale = frame.copy()

# detect the petri dish

gray_scale = cv2.cvtColor(scale, cv2.COLOR_BGR2GRAY)
petri_dish = 560  # a default value
circles = cv2.HoughCircles(gray_scale, cv2.HOUGH_GRADIENT, 1.2, 800, param1=50,param2=30,minRadius=80,maxRadius=230)

# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    
    largest_r = 0

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(scale, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(scale, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        if largest_r < r:
            largest_r = r
    
    petri_dish = r * 2
 
    # show the output image
    cv2.imshow("Circle detection", scale)
    cv2.waitKey(0)



# Tadpole ROI
print("Select the tadpole and press SPACE or ENTER.")
tad_ROI = cv2.selectROI(last_frame, False)

# Background ROI
print("Select an area of background and press SPACE or ENTER.")
bg_ROI =  cv2.selectROI(last_frame, False)

# create the subtraction frame (removing tadpole from last_frame)
bg_img = last_frame[bg_ROI[1]:bg_ROI[1] + bg_ROI[3], bg_ROI[0]:bg_ROI[0] + bg_ROI[2]].copy()
bg_av = bg_img.mean(axis=0).mean(axis=0)
cv2.rectangle(last_frame, (tad_ROI[0], tad_ROI[1]), (tad_ROI[0] + tad_ROI[2] , tad_ROI[1] + tad_ROI[3]), bg_av, -1)
ret, last_frame = cv2.threshold(last_frame, 240, 255,cv2.THRESH_TRUNC)
last_frame = last_frame + 15

# Output file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_videos/' + filename + '_tracked.avi',fourcc, 30, (640,480))

# reset the video
video.set(cv2.CAP_PROP_POS_FRAMES, 0)
ok, frame = video.read()

# initialize the subtracted, high-contrast image
subtracted = cv2.subtract(frame, last_frame)
blurred = cv2.GaussianBlur(subtracted, (11, 11), cv2.BORDER_DEFAULT)
contrast = cv2.addWeighted(blurred, alpha, np.zeros(blurred.shape, frame.dtype), 0, beta)

# initialize the tadpole mask
bw = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
ret,mask = cv2.threshold(bw,50,255,cv2.THRESH_BINARY)
mask = cv2.erode(mask, None, iterations=1)
mask = cv2.dilate(mask, None, iterations=3)

# Initialize double ended queue of tracked points of length buffer
buffer = 30
pts = deque(maxlen= buffer )

# Initialize second buffer & deque for distance
buffer_2 = int(videofps * 2)
pts2 = deque(maxlen= buffer_2 )

#initialize counter, delta x & y, direction
counter = 0
counter2 = 0
(dX, dY) = (0, 0)
direction = ""
frame_num = 0
totaldis = 0
max_v = 0
curr_vel = 0
last_head = None
ellipse = None
stim_angle_start = None
deviation = 0

# scale
diameter = 52 #in mm
pixels = petri_dish 


if tracker_type == 'CSRT':
    bbox = cv2.selectROI(contrast, False)
    ok = tracker.init(contrast, bbox)


while True:
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break
        
    # preprocess the read frame
    subtracted = cv2.subtract(frame, last_frame)
    blurred = cv2.GaussianBlur(subtracted, (11, 11), cv2.BORDER_DEFAULT)
    contrast = cv2.addWeighted(blurred, alpha, np.zeros(blurred.shape, frame.dtype), 0, beta)
    bw = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    ret,mask = cv2.threshold(bw,50,255,cv2.THRESH_BINARY)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=3)
    
    # find contours
    contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    
    # increment frame counter
    frame_num += 1
    
    # draw contours if at least one contour was found (ie. tracking success)
    if len(contours) > 0:
        
        # find the largest contour in the mask
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        contour_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        
        if tracker_type == 'home brew':
            # draw the contour
            cv2.drawContours(frame, contours, max_index, (255, 0, 0),2)
        
            # track the contour center 
            pts.appendleft(contour_center)
        
        # compute the minimum enclosing ellipse
        if len(contours[max_index]) > 4:
            ellipse = cv2.fitEllipse(contours[max_index])
        else:
            ellipse = None
        
        
        if tracker_type == 'home brew':
            # if looming is occuring, add center to second deque
            if frame_num >= stim_frame and counter2 < buffer_2:
                pts2.appendleft(contour_center)
                counter2 += 1
    
    # if no contours found (ie. tracking failure)
    else:
        if tracker_type == 'home brew':
            pts.appendleft(None)
            if frame_num >= stim_frame and counter2 < buffer_2:
                pts2.appendleft(None)
                counter2 += 1

    if tracker_type == 'CSRT':
        # Update tracker
        ok, bbox = tracker.update(contrast)
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,255,0), 2, 1)
        
            #add center to deque
            bbox_center = ( int( int(bbox[0]) + 0.5 * bbox[2] ) , int(int(bbox[1]) + 0.5 * bbox[3] ))
            pts.appendleft(bbox_center)
            counter += 1
        
            if frame_num >= stim_frame and counter2 < buffer_2:
                pts2.appendleft(bbox_center)
                counter2 += 1
                
        else :
            # Tracking failure
            tracker = cv2.TrackerCSRT_create()
            bbox = cv2.selectROI(contrast, False)
            ok = tracker.init(contrast, bbox)
                   
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        
            #add center to deque
            bbox_center = ( int( int(bbox[0]) + 0.5 * bbox[2] ) , int(int(bbox[1]) + 0.5 * bbox[3] ))
            pts.appendleft(bbox_center)
            counter += 1
        
            if frame_num >= stim_frame and counter2 < buffer_2:
                pts2.appendleft(bbox_center)
                counter2 += 1
        
    
    

    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if frame_num >= 10 and i == 1 and pts[-10] is not None:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")
            
            # compute the velocity
            dxy = math.sqrt(dX**2 + dY**2)
            
            # update current velocity
            curr_vel = (dxy / (pixels / diameter)) / (10 / videofps)
            
            # update max velocity of current velocity > max_v (during a stimulation)
            if frame_num > stim_frame and frame_num < stim_frame + buffer_2:
                if curr_vel > max_v:
                    max_v = curr_vel
            
            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt( buffer / float(i + 1)) * 2)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    

    # check if stim occurred
    if frame_num > stim_frame and frame_num < stim_frame + buffer_2:
        
        
        # compute the distance
        # the difference between the x and y coordinates 
        if pts[0] is None or pts[1] is None:
            continue
        distance = math.sqrt( (pts2[1][0] - pts2[0][0])**2 + (pts2[1][1] - pts2[0][1])**2 ) / (pixels / diameter)
        totaldis += distance
        
        # check if there is an ellipse
        if ellipse != None:
            # check if ellipse is of good quality
            if ellipse[1][1] / ellipse[1][0]  > ellipse_quality:
                # check if this is the first angle after stimulation starts
                if stim_angle_start == None:
                    # if so, keep track of the starting angle
                    stim_angle_start = ellipse[2]
                    last_head = ellipse[2]
                else:
                    # calculate the deviation
                    # was there a crossover?
                    #print(str(ellipse[2]) + " - " + str(last_head) + " = " + str(ellipse[2] - last_head))
                    if abs(ellipse[2] - last_head) < crossover_angle:
                        deviation += ellipse[2] - last_head
                        last_head = ellipse[2]
                    elif ellipse[2] - last_head >= crossover_angle:
                        deviation +=  ellipse[2] - last_head - 180
                        last_head = ellipse[2]
                    elif ellipse[2] - last_head <= (-1 * crossover_angle):
                        deviation +=  ellipse[2] - last_head + 180
                        last_head = ellipse[2]
                    else:
                        pass
            
        # if there is no ellipse, don't do anything
        else:
            pass
        
    
    # show the start frame and end frame of visual stimulation
    if frame_num == stim_frame:
        start_frame = frame.copy()
    if frame_num == stim_frame + buffer_2:
        end_frame = frame.copy()
    
    
    
    # drawing the escape contrail
    
    for i in np.arange(1, len(pts2)):
        # if either of the tracked points are None, ignore them
        if pts2[i - 1] is None or pts2[i] is None:
            continue
    
        # compute the thickness of the line and draw the connecting lines
        thickness2 = int(np.sqrt( buffer_2 / float(i + 1)) * 2)
        cv2.line(frame, pts2[i - 1], pts2[i], (0, 255, 0), thickness2)
        
    
    
#    # show the movement deltas and the direction of movement on
#    # the frame
#    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#        0.65, (0, 0, 255), 2)
#    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
#        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
#        0.35, (0, 0, 255), 1)
    
    if ellipse != None:
        cv2.putText(frame, "Current Heading: {}".format(round(ellipse[2], 1)),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 255, 255), 2)
    elif last_head != None:
        cv2.putText(frame, "Current Heading: {}".format(round(last_head, 1)),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 255, 255), 2)
    else:
        cv2.putText(frame, "Current Heading: N/A",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 255, 255), 2)
    
    cv2.putText(frame, "Deviation: {}".format(round(deviation,1)),
        (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 255, 255), 2)
    
    
    # display LOOMING when stimulus occurs
    
    if frame_num > stim_frame and frame_num < stim_frame + buffer_2:
    
        cv2.putText(frame, "LOOMING", (frame.shape[1] - 180, 40), cv2.FONT_HERSHEY_SIMPLEX, 
        1.2, (255, 0, 0), 4)
    
    
    #display velocity
    cv2.putText(frame, "Vel: " + str(round(curr_vel,1)) ,
    (int(frame.shape[1]-140), frame.shape[0]-70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
    
    
    # display distance travelled during looming event
    cv2.putText(frame, "Dist: " + str(round(totaldis,1)),
    (int(frame.shape[1]-140), frame.shape[0]-40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
    # display Vmax
    cv2.putText(frame, "Vmax: " + str(round(max_v,1)),
    (int(frame.shape[1]-140), frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
    # display frame number
    cv2.putText(frame, "Frame: " + str(frame_num),
    (int(10), frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    
    
    # Display result
    #cv2.imshow("Video", np.hstack([frame, contrast]))
    cv2.imshow("Video", frame)
    
    # Write result
    out.write(frame)

    # Exit if ESC pressed
    k = cv2.waitKey(playback_speed) & 0xff
    if k == 27 : break

# display the start and end frames
cv2.imshow("Start and End", np.vstack([start_frame, end_frame]))


# drawing the escape contrail
for i in np.arange(1, len(pts2)):
    # if either of the tracked points are None, ignore them
    if pts2[i - 1] is None or pts2[i] is None:
        continue
    
    # compute the thickness of the line and draw the connecting lines
    thickness2 = int(np.sqrt( buffer_2 / float(i + 1)) * 5)
    cv2.line(img_output, pts2[i - 1], pts2[i], (255, 255, 255), thickness2)

now = datetime.now()
print('Animal ID. Timepoint, Treatment, Trial #, Esc Dis, Esc Vel, Esc Ang, Timestamp')
data_to_save = [ animalID, timepoint, treatment, trial[-1:], round(totaldis,1), round(max_v,1), abs(round(deviation,1)), now.strftime("%y/%m/%d %H:%M") ]
print(data_to_save)


save_or_not = gui.Dlg()
save_or_not.addText('Save data?')
save_or_not.show()


if save_or_not.OK:
    cv2.imwrite('output_contrails/' + filename + '.jpg',img_output)
    
    if os.path.exists('data.csv') == False:
        with open ('data.csv', 'w', newline='') as datafileinit:
            datafileinitwriter = csv.writer(datafileinit)
            datafileinitwriter.writerow( [ 'Animal ID', 'Timepoint', 'Treatment', 'Trial #', 'Esc Dis', 'Esc Vel', 'Esc Ang', 'Timestamp' ] )
        
    
    with open('data.csv', 'a', newline='') as datafile:
        datafilewriter = csv.writer(datafile)
        datafilewriter.writerow( data_to_save )
        print("Data saved to data.csv")
else:
    print("Data not saved.")

cv2.destroyAllWindows()