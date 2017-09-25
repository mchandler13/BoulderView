# BoulderView
Using social networks to predict where photos are being taken, based on the associated text. 

## Table of Contents
1. [Early Steps](#Early-Steps)
   * [Dataset](#Dataset)
   * [Building The Dataset](#Building-the-Dataset)
2. [Acoustic Features of Speech](#acoustic-features-of-speech)
    * [Segmentation](#segmentation-code)
    * [Feature Extraction](#feature-extraction-code)

## Early Steps

1) Getting a Twitter API, and learning how to use it with Python.
2) Creating a dataset
    * Pulling data from Twitter can be messy!
3) Feature Engineering: Which features are important?


<img alt="Initial Findings" src="data/images/EDA_1.jpg" width='800' height = '550'>

## Dataset
All audio recordings and associated depression metrics were provided by the [DAIC-WOZ Database](http://dcapswoz.ict.usc.edu/), which was compiled by USC's Institute of Creative Technologies and released as part of the 2016 Audio/Visual Emotional Challenge and Workshop ([AVEC 2016](http://sspnet.eu/avec2016/)). The dataset consists of 189 sessions, averaging 16 minutes, between a participant and virtual interviewer called Ellie, controlled by a human interviewer in another room via a "[Wizard of Oz](https://en.wikipedia.org/wiki/Wizard_of_Oz_experiment)" approach. Prior to the interview, each participant completed a psychiatric questionnaire ([PHQ-8](http://patienteducation.stanford.edu/research/phq.pdf)), from which a binary "truth" classification (depressed, not depressed) was derived.

A representative transcribed interview excerpt is seen below:

> **Ellie:** Who’s someone that’s been a positive influence in your life?

> **Participant:** Uh my father.

> **Ellie:** Can you tell me about that?
