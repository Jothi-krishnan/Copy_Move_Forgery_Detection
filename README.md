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
- [Input](#input)
- [Output](#output)

## Overview
This is the implementation on a python script which detects copy-move forgery on images. 

We use overlapping blocks of 32*32 and then extract 7 features using arithmetic operations and 3 features using Principal Component Analysis.We then sort the resulting arrays in lexographical order and locate similar arrays. We then find the distance between these blocks on the original image. We then plot these blocks at white squares in our output. Thus, we detect copy-move forgery in these images.

### Pre requisites

Users should have the following installed before running the python script

- python 3

- See hover states for interactive elements


### Algorithm Used
This is the implementation on a python script which detects copy-move forgery on images. 

We use overlapping blocks of 32*32 and then extract 7 features that we use to analyse our image. These seven features are- 

Feature 1: Average of all the red pixel values
Feature 2: Average of all the blue pixel values
Feature 3: Average of all the green pixel values

Function C takes the pixel values of an image and sums up all the pixel values of the upper half of the block and divides this by the sum of all pixel values of the block (A method used in Research Paper 1).

Y= 0.299R+0.587G+0.114B where R,G and B are red, blue and green pixel values respectively. 

Feature 4: Function C for greyscale or Y pixel values 
Feature 5: Function C for red pixel values
Feature 6: Function C for blue pixel values
Feature 7: Function C for green pixel values

### Resources

- Solution URL: [My Github Repository](https://github.com/Jothi-krishnan/FEM_junior01)
- Live Site URL: [Live Website](https://jothi-krishnan.github.io/FEM_junior01/)

We use two reference papers to aid us:
    1. https://ieeexplore.ieee.org/document/1699948- This paper outlines the Duplication detection algorithm we use in our project. 
    2. https://www.semanticscholar.org/paper/Exposing-Digital-Forgeries-by-Detecting-Duplicated-Popescu-Farid/b888c1b19014fe5663fd47703edbcb1d6e4124ab- This paper outlines the inspiration for our feature extraction before performing PCA on the extractedd features. 

## Input

This is the input we provide to our program:
![Input image](Inputs\threehundred_gcs500_copy_rb5.png "Input Image")

## Output
This is the output that the program gives us:
![Output image](Outputs\20221127_150658_marked_threehundred_gcs500_copy_rb5.png "Output Image")
![Output image](Outputs\20221127_150658_attacked_threehundred_gcs500_copy_rb5.png "Output Image")


