import numpy, cv2, datetime, threading, time, csv
from psychopy import visual, core, event, gui
from psychopy.visual import ShapeStim

experiment_types = ['blackloom', 'whiteloom']
# here define whether it is a black on white loom or a white on black loom
experiment_type = experiment_types[1]

if experiment_type == 'blackloom':
    background_colour = (1, 1, 1)
    loom_colour = (-1, -1, -1)
if experiment_type == 'whiteloom':
    background_colour = (-1, -1, -1)
    loom_colour = (1, 1, 1)

# set up capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 40)
cap.set(cv2.CAP_PROP_FPS, 30)

# turn on camera
while True:
    ret, frame = cap.read()
    if ret==False:
        continue
    break

# create dictionary for saving experiment info (animal ID, timepoint, treatment)
expInfo = {'Animal ID':'', 'timepoint':'', 'treatment':''}
expInfo['exp_type'] = experiment_type
expInfo['dateStr'] = str(datetime.date.today())

# create GUI request for user input to fill in experiment info
dlg = gui.DlgFromDict(expInfo, fixed=['exp_type', 'dateStr'])
if dlg.OK:
    pass 
else:
    core.quit()

# instantiate list to store timing data from all trials
capture_data = []

# define the capture function
def capture(trial_num):
    
    # codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # filename
    out = cv2.VideoWriter(expInfo['Animal ID'] + '_'+ expInfo['timepoint'] + '_' + expInfo['treatment'] +'_trial' + str(trial_num)+'.avi',fourcc, 30, (640,480))

    # instantiate a dictionary to store timing data
    trial_dict = {}
    trial_dict['trial num'] = trial_num

    # instantiate variables (length is the duration of video capture)
    length = 0
    frame_count = 0

    # define the start of the trial and store it in the dictionary
    start = time.time()
    trial_dict['start'] = start    

    # the length of the capture... will need to change this...!
    while(length < 15):
        ret, frame = cap.read()
        out.write(frame)
        frame_count += 1
        length = time.time() - start
    
    # store other timing data into dictionary
    trial_dict['frames'] = frame_count
    trial_dict['duration'] = length
    trial_dict['fps'] = frame_count/length
    
    # add trial data into big list outside of function
    capture_data.append(trial_dict)

# set up the stimulus display
mywin = visual.Window([800, 600], monitor="projector", screen=1, fullscr=True, units="pix", pos=None, color=background_colour, colorSpace='rgb')

# instantiate the variable to store the timing of the looming stimulus
stim_time =[]

# define the looming function
def stimulus():
    # instantiate circle variables
    myradius = 1.0
    mysize = 1.0
    
    # create the circle and draw it
    mycircle = visual.Circle(win = mywin, radius = myradius, edges = 128, color=loom_colour, size = mysize )
    mycircle.draw()
    mywin.flip()
    
    # wait 2 secs
    core.wait(2)
    
    # slowly increase size of circle
    for i in range(250):
        mysize += 0.1
        mycircle.size = mysize
        mycircle.draw()
        mywin.flip()
        
    # wait 2 seconds
    core.wait(2)
    
    # save stimulus time to list
    stim_time.append(time.time())
    
    # start the looming stimulus
    for i in range(50):
        mycircle.setSize(1.1, '*')
        mycircle.draw()
        mywin.flip()
    
    # wait half a sec
    core.wait(0.5)
    
    # reset the circle
    mycircle.size = 1
    mycircle.draw()
    mywin.flip()

# set up the loop to run 10 trials
for trial in range(10):
    print("Beginning trial " + str(trial))
    mythread = threading.Thread(target=capture,args=[trial])
    mythread.start()  
    stimulus()
    mythread.join()
    core.wait(1)

# close and clean up webcam capture
cap.release()
cv2.destroyAllWindows()

# add stimulation time to the trial dictionarys
for x in range(10):
    capture_data[x].update( {'stim time': stim_time[x] } )

# write the trial dictionary with the row titles of the dictionary keys to a csv
keys = capture_data[0].keys()
with open(expInfo['Animal ID'] + '_'+ expInfo['timepoint'] + '_' + expInfo['treatment'] + '_' +  expInfo['exp_type'] + '_timings.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    # write the data of each trial into the csv
    dict_writer.writerows(capture_data)

# close and cleanup stimulus window
mywin.close()
core.quit()