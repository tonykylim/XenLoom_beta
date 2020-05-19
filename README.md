# XenLoom_beta
XenLoom (beta): Visual stimulus presentation and tracking for Xenopus tadpoles

What is this repository for?
This repository contains a software framework for a visual-evoked behavioural assay in Xenopus laevis tadpoles.
Specifically, this repository includes code that allows:
a) Presention of virtual looming stimuli and simultaneous recording of behavioural responses,
b) analysis of recorded responses to discern escape behaviour from the absence of escape behaviour, and
c) tadpole tracking for the automated extraction of motor activity.

How is this repository organized?
The code has been partitioned into 3 modules (stim-present, loom-decision, tad-tracker) which correspond to the above 3 functions.
The stim-present module presents dark or bright looming stimuli and tadpole behavioural responses in the form of avi video and timing data are collected.
This data is in turn fed into the loom-decision module, where the data is coded for the blinded discrimination of escape behaviour, the absense of escape behaviour, or undeterminable (excluded from analysis).
Finally, the tad-tracker module is a tool for the automated tracking of Xenopus tadpoles, extracting: pre- and post-loom motor activity, contrails, escape distance, maximum escape velocity, and initial escape angle.
