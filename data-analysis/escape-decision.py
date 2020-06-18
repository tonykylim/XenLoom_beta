import glob, random, cv2, csv, os
from datetime import datetime
from tkinter import *

## set playback speed (eg. 3 = 3X real-time)
playback_speed = 3

def user_yes():
    global replay
    replay = False
    input = 1
    now = datetime.now()
    data_to_save = [ animalID, timepoint, treatment, trial[-1:], input, now.strftime("%y/%m/%d %H:%M") ]
    with open('response_to_loom.csv', 'a', newline='') as datafile:
        datafilewriter = csv.writer(datafile)
        datafilewriter.writerow( data_to_save )
        print("Trial data saved to response_to_loom.csv")
    win.destroy()

def user_no():
    global replay
    replay = False
    input = 0
    now = datetime.now()
    data_to_save = [ animalID, timepoint, treatment, trial[-1:], input, now.strftime("%y/%m/%d %H:%M") ]
    with open('response_to_loom.csv', 'a', newline='') as datafile:
        datafilewriter = csv.writer(datafile)
        datafilewriter.writerow( data_to_save )
        print("Trial data saved to response_to_loom.csv")
    win.destroy()
    
def user_unsure():
    global replay
    replay = False
    input = ''
    now = datetime.now()
    data_to_save = [ animalID, timepoint, treatment, trial[-1:], input, now.strftime("%y/%m/%d %H:%M") ]
    with open('response_to_loom.csv', 'a', newline='') as datafile:
        datafilewriter = csv.writer(datafile)
        datafilewriter.writerow( data_to_save )
        print("Trial data saved to response_to_loom.csv")
    win.destroy()
    
def user_replay():
    global replay
    replay = True
    win.destroy()

# create CSV file if none exists
if os.path.exists('response_to_loom.csv') == False:
        with open ('response_to_loom.csv', 'w', newline='') as datafileinit:
            datafileinitwriter = csv.writer(datafileinit)
            datafileinitwriter.writerow( [ 'Animal ID', 'Timepoint', 'Treatment', 'Trial #', 'Response', 'Timestamp' ] )

# load video files
video_file_list = glob.glob("*.avi")

# randomize order
random.shuffle(video_file_list)

# number of videos
num_videos = len(video_file_list)

# play all of the videos
video_num_counter = 0
for video_file in video_file_list:
    
    # print the video number
    video_num_counter += 1
    print('Playing video ' + str(video_num_counter) + ' of ' + str(num_videos))
    
    # Read video
    video = cv2.VideoCapture(video_file)
    
    # Exit if video not opened
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # get timing data
    filename = video_file[:-4]
    animalID, timepoint, treatment, trial = filename.split("_")
    trial_num = int(trial[-1:])
    
    # retreive timing settings
    capture_data = []
        timingscsvlist = glob.glob(f'{animalID}_{timepoint}_{treatment}_*_timings.csv')
    with open(timingscsvlist[0], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            capture_data.append(row)
    
    # timing data
    stim_start = float(capture_data[trial_num]['stim begin'])
    stim_end = float(capture_data[trial_num]['stim end'])
    trial_start = float(capture_data[trial_num]['start'])
    stim_time = stim_start-trial_start
    videofps = float(capture_data[trial_num]['fps'])
    stim_frame = int(stim_time*videofps)
    stim_end_time = stim_end-trial_start
    stim_end_frame = int(stim_end_time*videofps)
    
    replay = True
    # play the video
    while replay == True:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_num = 0
        while True:
            # Read a new frame
            ok, frame = video.read()
            if not ok:
                break
            frame_num += 1
            
            # display LOOMING when stimulus occurs
            if frame_num > stim_frame and frame_num < stim_end_frame+1:
                cv2.putText(frame, "LOOMING", (frame.shape[1] - 180, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 4)
            
            # Display the frame
            cv2.imshow("Video", frame)
            # Exit if ESC pressed
            k = cv2.waitKey(30/playback_speed) & 0xff
            if k == 27 : break
        
        # get user response
        win = Tk()
        f = Frame(win)
        b1 = Button(f, text="Yes", command=user_yes)
        b2 = Button(f, text="No", command=user_no)
        b3 = Button(f, text="Unsure", command=user_unsure)
        b4 = Button(f, text="Replay", command=user_replay)
        b1.pack(side=LEFT)
        b2.pack(side=LEFT)
        b3.pack(side=LEFT)
        b4.pack(side=LEFT)
        l = Label(win, text="Did the tadpole respond to the looming stimuli?")
        l.pack()
        f.pack()
        f.mainloop()

# sort data
with open('response_to_loom.csv', mode='rt', newline='') as data, open('response_to_loom_sorted.csv', 'w', newline='') as sorted_data:
    writer = csv.writer(sorted_data, delimiter=',')
    reader = csv.reader(data, delimiter=',')
    writer.writerow(next(reader))
    data = sorted(reader, key=lambda row: (int(row[0]), int(row[3])))  
    for row in data:
        writer.writerow(row)