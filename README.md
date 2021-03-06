# XenLoom (beta): Tracking visual-evoked behaviours in Xenopus tadpoles :frog:

This repository contains a software framework for a visual-evoked behavioural assay in Xenopus laevis tadpoles.
Specifically, this repository includes code that allows:
- Presention of virtual looming stimuli and simultaneous recording of behavioural responses,
- Analysis of recorded responses to discern escape behaviour from the absence of escape behaviour, and
- Tadpole tracking for the automated extraction of motor activity.

## Getting Started

The code has been partitioned into 3 modules (stim-present, loom-decision, tad-tracker) which correspond to the above 3 functions.

The stim-present module presents dark or bright looming stimuli and tadpole behavioural responses in the form of avi video and timing data are collected.

This data is in turn fed into the loom-decision module, where the data is coded for the blinded discrimination of escape behaviour, the absense of escape behaviour, or undeterminable (excluded from analysis).

Finally, the tad-tracker module is a tool for the automated tracking of Xenopus tadpoles, extracting: pre- and post-loom motor activity, contrails, escape distance, maximum escape velocity, and initial escape angle.

## Expected results

Representative response to dark looming stimuli in a control tadpole (Stage 47):<br />
![example-video](https://github.com/tonykylim/XenLoom_beta/blob/master/~expected-results/looming-example.gif) 

## Prerequisites

Requirements to run this behavioural assay:
1. Windows PC
   - Verified to work on Windows 10
   - Initial tests have found this tool incompatable with macOS
1. Python 3
   - Easiest tried and true method: install Psychopy 3 https://www.psychopy.org/
     - Python 3 is included in this standalone package
2. Additional python libraries:
   - cv2
   - psychopy
      - these packages come with the Psychopy 3
3. Required equipment
   - Carolina 8-inch culture dish https://www.carolina.com/lab-dishes/culture-dishes-carolina-8-in-1500-ml/741006.pr
   - 3D printed stage https://www.thingiverse.com/thing:4335395
     - Filament used: https://www.iprint-3d.com/products/transparent-purple-pla-3d-filament?variant=35097294661
   - 2000 lumens projector (modified) [Photo](https://cdn.thingiverse.com/assets/e2/15/bd/b0/b2/featured_preview_Picture1.jpg)
     - The projector lens is removed from the housing and moved forwards, in order to shorten the focal length of the projector
     - Tested to work with this <$100 projector https://www.amazon.ca/gp/product/B07F7RT9XZ/
     - 3D printed lens holder https://www.thingiverse.com/thing:4335379
     - This projector is currently no longer available, if you are having trouble please contact me and I will try to find a solution for you
   - Webcam
     - Tested to work with logitech C920 and C922 webcams
   - Petri dishes
     - We use these https://www.fishersci.ca/shop/products/fisherbrand-petri-dishes-clear-lid-12/fb0875713a
     - Other Petri dishes can work, but you'll likely have to tweak the settings
   - Other useful things:
     - Microphone boom arm to hold webcam eg. https://www.amazon.ca/gp/product/B07QH4J3GZ/
       - Or 3D print your own here https://www.thingiverse.com/thing:2194278
     - Black umbrella, or a black shade on a microphone boom arm
       - important for blocking glare from ceiling lights

## Installing

1. Install Psychopy 3 https://www.psychopy.org/
2. Download the XenLoom code

## Experimental setup

Diagram of setup: <br /> <img src="https://github.com/tonykylim/XenLoom_beta/blob/master/~expected-results/diagram.png" width=50% height=50% />

...What the setup actually looks like in reality: <br /><img src="https://github.com/tonykylim/XenLoom_beta/blob/master/~expected-results/experimental-setup.jpg" width=50% height=50% /> 

1. It is recommended to run the experiment in a well lit room (under typical lighting for an office or laboratory)
2. Fill the 8-inch Carolina glass culture dish (bowl) with 0.1X MBSH, until ~90-95% full.
3. Place the 8-inch Carolina glass bowl onto the 3D printed stage.
4. Connect the webcam and projector to the computer and boot up the computer.
5. The resolution of the projector should be set to 800X600 pixels.
6. Cut out a white piece of paper to serve as a projector screen. It should be as tall as the Carolina glass bowl, and wide enough so that the projector image stays within the bounds of the paper screen.
7. Tape the paper onto the 8-inch Carolina glass bowl.
8. Focus the projector onto the screen so that the middle of the screen is in focus, and that the image from the projector takes up the full height of the paper screen. The side edges of the projector image will be slightly blurry as the paper follows the curvature of the bowl.
9. Using powder free gloves, place both halves of a petri dish into the Carolina glass bowl so that the halves fill with MBSH without bubbles. Place a tadpole into the bottom petri dish half, and entrap the tadpole by covering with the matching petri dish half. Be careful to note introduce bubbles within the petri dish.
   - Use of gloves is recommended to reduce the chance of introducing particles into the MBSH which may complicate tracking.
10. Maneuveur the petri dish into the middle of the Carolina glass bowl.
11. Align the webcam so that the entire the petri dish is in the field of view, and that the webcam is viewing the petri dish from directly overhead.
12. View the webcam feed and remove ceiling light glare by covering lights with black shades or umbrellas.

## Running the experiment

### Collecting Data

1. Run the videocapturetest.py script to view the webcam feed. Ensure that:
   - The petri dish is centered
   - The webcam is positioned directly overhead
   - No glare obscures the petri dish
2. Open "background image settings" in windows system settings, and from the dropdown menu select "solid color".
   - Set the background to white if doing dark looming stimuli experiments.
   - Set the background to black if doing bright looming stimuli experiments.
3. Place the stimpresent-videocapturethread.py script in a directory where you would like to save the behavioural data.
   - It is recommended that you use a new folder for each group of animals, and separate dark looming experiments from bright looming experiments
4. Open PsychoPy and open the videocapturethread script. Press the run button (Control + R).
5. Fill in the prompt that pops up with the following info:
   - Animal ID
      - Eg. Pepe, Kermit, PluToad, MC Hopper, Toadie, Sir Croaks-A-Lot, SnoopFrogg, etc
   - Timepoint
      - Eg. S47, Stage 47, Day 2, Timepoint 4, IShouldBeAsleepButInsteadIAmRunningExperiments, etc
   - Treatment
      - Eg. Vehicle, Drugs!, Visual Stimulation, Soft Rock Music, etc
   - **Important: Do not use _ underscores, / back slashes, \ forward slashes, | vertical bar, ? question marks, < less than, > greater than, : colon, or * asterisks, when filling out the above info. Recommended that you use alphanumeric responses. Spaces are OK. Periods are probably OK but I would avoid using them.**
   - **Note that if you enter in values that correspond to previously captured data, the script will overwrite the old data.**
6. The script will now run. Ten avi video files will be collected and one timings csv file.

### Categorization of escape behaviour

1. Copy the escape-decision.py script to the folder with the video files.
2. Open the escape-decision.py script with PsychoPy and run it.
3. A random video will play. Categorize the behaviour as:
   - Escape behaviour
   - Lack of escape behaviour
   - Undeterminable (If you are unsure just pick this. Usually this happens if the tadpole was moving quickly just before the looming stimulus was sent.)
   - If you are unsure, you can replay the video. Evaluating tadpole escape responses may take some getting used to.
4. The next random video will then play. Do step 3 for all video files in the directory.
5. After all videos in the directory are categorized, a csv file is generated called response_to_loom_sorted.csv
   - Escape behaviour is coded as 1, lack of escape behaviour is coded as 0, and undeterminable is coded as an empty cell.

### Motor activity

0. First time setup:
   - Measure the diameter of the bottom of your petri dish. Edit the `diameter=52` line so that the value corresponds to the diameter of the dish in mm. No need to change this line if you use the Fisherbrand petri dishes that we use.
   
1. Copy the tadpole-tracker.py script to the directory with the video files.
2. Change the filename line to match the filename of the video to analyze (without the .avi extension)
3. Run tadpole-tracker.py
4. The first prompt asks to confirm that the petri dish is properly detected. This sets the scale of the video data.
   <img src="https://github.com/tonykylim/XenLoom_beta/blob/master/~expected-results/circle_detect.png" width=50% height=50% />
   -  A green circle should be drawn over the perimeter of the petri dish bottom. If everything looks OK, press space to continue.
   -  If the circle isn't the right size, modify the `pdmaxrad=230` value to be a slightly larger (if the circle was too small) or smaller number (if the circle was too large) and try again.
5. At the next prompt, draw a rectangle over the tadpole using the mouse.
   <img src="https://github.com/tonykylim/XenLoom_beta/blob/master/~expected-results/roi_tadpole.png" width=50% height=50% />
   -  Then press spacebar.
6. If the tadpole moved out of the drawn box by the end of the video, then it will have been subtracted from the image.
   <img src="https://github.com/tonykylim/XenLoom_beta/blob/master/~expected-results/background_subtracted.png" width=50% height=50% />
   -  If the tadpole has been removed from the image, press yes.
   -  If the tadpole has not been removed from the image, press no, and at the next prompt, select a region of background instead. It may work better if you restart the script and initially select a small region around the tadpole (such as just the belly).
7. Automatic tracking commences. If the script cannot detect the tadpole's location, it will prompt you to select the location of the tadpole manually. 
   -  If the tracking was unsuccessful:
      - Try changing the value for `alpha`. 8 is a good starting point, but it may work better in the 2-30 range.
   -  If angle tracking seems innacurate:
      - Try a different value for `crossover_angle`. 70, 90, 130 are good numbers to try.
      - Try a different value for `ellipse_quality`. Values from 1.01 to 1.3 are good numbers to try.
8. After successful tracking, save the data by pressing yes.
9. If it doesn't already exist, a csv file called data.csv will be generated. If it already exists, data will be appended to this file. This file contains escape distance, maximum escape velocity, and escape angle data.
10. Contrails will be outputted into the /contrails/ directory.
11. Instantaneous velocity 3 seconds before and after the looming stimulus is outputted in the /output_speed/ directory in a csv file.
12. After running all the trials through the tadpole-tracker.py script, contrails within animals can be merged using the contrail-merger.py script in the /contrails/ directory.
 
## Versioning

A version of XenLoom with more advanced stimulus presentation and data extraction features is in the works and will be available at http://github.com/tonykylim/XenLoom and http:/ruthazerlab.mcgill.ca/

## Authors

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://media.giphy.com/media/mCRJDo24UvJMA/giphy.gif" width=12% height=12% />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" width=12% height=12% /><br />
This tool was developed by Tony K.Y. Lim and Edward S. Ruthazer. http://ruthazerlab.mcgill.ca/

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Apologies to all the tadpoles on the receiving end of a looming stimulus. &nbsp;:slightly_smiling_face:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:black_small_square:&nbsp;&nbsp;:black_medium_small_square:&nbsp;&nbsp;:black_medium_square:&nbsp;&nbsp;:black_large_square:&nbsp;&nbsp;&nbsp;&nbsp;:astonished:
