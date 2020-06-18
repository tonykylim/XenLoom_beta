import numpy, cv2, datetime, threading, time, csv, math
from psychopy import visual, core, event, gui
from psychopy.visual import ShapeStim


experiment_types = ['darkloom', 'brightloom']


## Here, choose the experiment type. 0 = dark looming stimuli; 1 = bright looming stimuli
experiment_type = experiment_types[0]

if experiment_type == 'blackloom':
    background_colour = (1, 1, 1)
    loom_colour = (-1, -1, -1)
if experiment_type == 'whiteloom':
    background_colour = (-1, -1, -1)
    loom_colour = (1, 1, 1)

## if your computer opens the wrong webcam, change the 0 to a 1
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

# capture settings
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 40)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# turn on camera
while True:
    ret, frame = cap.read()
    if ret==False:
        continue
    break

# experiment info (animal ID, timepoint, treatment)
expInfo = {'Animal ID':'', 'timepoint':'', 'treatment':''}
expInfo['exp_type'] = experiment_type
expInfo['dateStr'] = str(datetime.date.today())

# user input to fill in experiment info
dlg = gui.DlgFromDict(expInfo, fixed=['exp_type', 'dateStr'])
if dlg.OK:
    pass 
else:
    core.quit()

# timing data by trial
capture_data = []

# capture function
switch = False
def capture(trial_num):
    global switch
    
    # codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    # filename
    out = cv2.VideoWriter(expInfo['Animal ID'] + '_'+ expInfo['timepoint'] + '_' + expInfo['treatment'] +'_trial' + str(trial_num)+'.avi',fourcc, 30, (640,480))
    
    # timing data dictionary
    trial_dict = {}
    trial_dict['trial num'] = trial_num
    
    # instantiate variables
    length = 0
    frame_timer = 0
    frame_count = 0
    
    # define the start of the trial
    start = time.time()
    trial_dict['start'] = start
    
    # capturing frames
    while switch == False:
        ret, frame = cap.read()
        out.write(frame)
        frame_count += 1
        length = time.time() - start
    else:
        frame_timer = frame_count + 150
        while frame_count < frame_timer:
            ret, frame = cap.read()
            out.write(frame)
            frame_count += 1
            length = time.time() - start
            
    # store timing data
    trial_dict['frames'] = frame_count
    trial_dict['duration'] = length
    trial_dict['fps'] = frame_count/length
    capture_data.append(trial_dict)

# stimulus setup
mywin = visual.Window([800, 600], monitor="projector", screen=1, fullscr=True, units="pix", pos=None, color=background_colour, colorSpace='rgb')

# timing of the looming stimulus
stim_time =[]
stim_end = []

# looiming function
def stimulus():
    global switch
    
    # circle variables
    myradius = 1.0
    mysize = 1.0
    
    # draw circle
    mycircle = visual.Circle(win = mywin, radius = myradius, edges = 128, color=loom_colour, size = mysize )
    mycircle.draw()
    mywin.flip()
    
    # wait
    core.wait(2)
    
    # slowly increase size of circle
    for i in range(250):
        mysize += 0.1
        mycircle.size = mysize
        mycircle.draw()
        mywin.flip()
    
    # wait
    core.wait(2)
    
    # stim start time
    stim_time.append(time.time())
    
    # looming stimulus
    while math.sqrt((mywin.size[0]/2)**2+(mywin.size[1]/2)**2) > mycircle.size:
        mycircle.setSize(1.1, '*')
        mycircle.draw()
        mywin.flip()
    stim_end.append(time.time())
    switch = True
        for i in range(50):
        mycircle.draw()
        mywin.flip()
    
    # wait
    core.wait(0.5)
    
    # reset
    mycircle.size = 1
    mycircle.draw()
    mywin.flip()
    switch = False

# run 10 trials
for trial in range(10):
    mythread = threading.Thread(target=capture,args=[trial])
    mythread.start()  
    stimulus()
    mythread.join()
    core.wait(1)

# close and clean up webcam capture
cap.release()
cv2.destroyAllWindows()

# update looming timing data
for x in range(len(stim_time)):
    capture_data[x].update( {'stim begin': stim_time[x] } )
for x in range(len(stim_end)):
    capture_data[x].update( {'stim end': stim_end[x] } )
keys = capture_data[0].keys()

# create timing csv file
with open(expInfo['Animal ID'] + '_'+ expInfo['timepoint'] + '_' + expInfo['treatment'] + '_' +  expInfo['exp_type'] + '_timings.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(capture_data)

# close psychopy
mywin.close()
core.quit()