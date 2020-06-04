# XenLoom (beta): Visual stimulus presentation and tracking for Xenopus tadpoles

This repository contains a software framework for a visual-evoked behavioural assay in Xenopus laevis tadpoles.
Specifically, this repository includes code that allows:
- Presention of virtual looming stimuli and simultaneous recording of behavioural responses,
- analysis of recorded responses to discern escape behaviour from the absence of escape behaviour, and
- tadpole tracking for the automated extraction of motor activity.

This tool was developed by Tony KY Lim under the supervision of Dr Edward S Ruthazer. http://ruthazerlab.mcgill.ca/

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

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc



# XenLoom_beta
