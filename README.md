# Copy_Move_Forgery_Detection

This is a group project of the course Digital Image Processing done by,
  1. Harshit Gupta
  2. Jothi Krishnan M
  3. Kondapalli Suhali
  4. Sneha Sundararajan

## Table of contents

- [Overview](#overview)
  - [Pre requisites](#prerequisites)
  - [Resources](#resources)
- [Inputs](#input)
- [Outputs](#output)

## Overview
---
This is the implementation on a python script which detects Copy-Move forgery on images. 

We use overlapping blocks of 32*32 pixels (default size) and then extract 7 features using arithmetic operations and 3 features using Principal Component Analysis (PCA). We then sort the resulting arrays in lexographical order and locate similar arrays. We then find the distance between these blocks on the original image. The output is then shown as white blocks in the output image. Thus, we detect copy-move forgery in the images.

## Pre requisites
---

Users should have the following installed before running the python script.

- python 3

- See hover states for interactive elements

## Algorithm Used
---
The implementation of our python code is as follows:

First, using the overlapping blocks, we extract multiple features from each sub-block. These features are- 

- *Feature 1:* Average of all the red pixel values
- _Feature 2:_ Average of all the blue pixel values
- *Feature 3:* Average of all the green pixel values
<!-- 
Function C takes the pixel values of an image and sums up all the pixel values of the upper half of the block and divides this by the all pixel values of the block (A-method used in Research Paper 1). -->

**Y= 0.299R+0.587G+0.114B** where R,G and B are red, blue and green pixel values respectively. 

- *Feature 4:* Function C for greyscale or Y pixel values 
- *Feature 5:* Function C for red pixel values
- *Feature 6:* Function C for blue pixel values
- *Feature 7:* Function C for green pixel values

## Resources
---

We use two reference papers to aid us:
    1. https://ieeexplore.ieee.org/document/1699948- This paper outlines the Duplication detection algorithm we use in our project. 
    2. https://www.semanticscholar.org/paper/Exposing-Digital-Forgeries-by-Detecting-Duplicated-Popescu-Farid/b888c1b19014fe5663fd47703edbcb1d6e4124ab- This paper outlines the inspiration for our feature extraction before performing PCA on the extractedd features. 

## Inputs
---

This is the input we provide to our program:
![Input image](Inputs\threehundred_gcs500_copy_rb5.png "Input Image")

## Outputs
---
This is the output that the program gives us:
![Output image](Outputs\20221127_150658_marked_threehundred_gcs500_copy_rb5.png "Output Image")
![Output image](Outputs\20221127_150658_attacked_threehundred_gcs500_copy_rb5.png "Output Image")

## Running GUI version
---
Steps to be followed are:

1. Run `app.py`
2. A new window will apear, click open file and choose your image.
3. Click detect and the detection process will start.
4. After done, the detection result will be written in your CLI, while the result image will be shown in GUI.
