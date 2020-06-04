# XenLoom (beta): Visual stimulus presentation and tracking for Xenopus tadpoles

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
   - 2000 lumens projector (modified)
     - Tested to work with this projector https://www.amazon.ca/gp/product/B07F7RT9XZ/
     - 3D printed lens holder
       - https://www.thingiverse.com/thing:4335379
     - This projector is currently no longer available, if you are having trouble please contact me and I will try to find a solution for you
   - Webcam
     - Tested to work with the logitech C920 as well as the logitech C922 camera
   - Other useful things:
     - Microphone boom arm to hold webcam eg. https://www.amazon.ca/gp/product/B07QH4J3GZ/
     - Black umbrella, or a microphone boom arm to hold a black shade
       - important for blocking ceiling lights

## Installing

Instructions to come

## Running the code

Instructions to come

## Versioning

A version of XenLoom with more advanced stimulus presentation and data extraction features is in the works.

## Authors

This tool was developed by Tony KY Lim under the supervision of Dr Edward S Ruthazer. http://ruthazerlab.mcgill.ca/

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Apologies to all the tadpoles on the receiving end of a looming stimulus. We <3 you.
