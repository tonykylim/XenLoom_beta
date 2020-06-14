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
   - imutils
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
     - Black umbrella, or a black shade on a microphone boom arm
       - important for blocking glare from ceiling lights

## Installing

1. Install Psychopy 3 https://www.psychopy.org/
2. Download code to a directory where you would like to save:
   - .csv files (timing data)
   - .avi files (video data)
3. Install additional python libraries
   - Open a command prompt (Windows button + R, type "cmd" and hit enter)
   - "python -m pip install imutils" 

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

Instructions to come

## Versioning

A version of XenLoom with more advanced stimulus presentation and data extraction features is in the works and will be available at http://github.com/tonykylim/XenLoom and http:/ruthazerlab.mcgill.ca/

## Authors

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://media.giphy.com/media/mCRJDo24UvJMA/giphy.gif" width=12% height=12% />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" width=12% height=12% /><br />
This tool was developed by Tony K.Y. Lim and Edward S. Ruthazer. http://ruthazerlab.mcgill.ca/

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Apologies to all the tadpoles on the receiving end of a looming stimulus. &nbsp;:slightly_smiling_face:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:black_small_square:&nbsp;&nbsp;:black_medium_small_square:&nbsp;&nbsp;:black_medium_square:&nbsp;&nbsp;:black_large_square:&nbsp;&nbsp;&nbsp;&nbsp;:astonished:
