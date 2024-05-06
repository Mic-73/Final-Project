#######################################
#//*** Author: Babak Forouraghi (taken from https://github.com/bforoura/AI/blob/main/Final_Project/convert.py)
#//*** Edited by: Michael Wood, Jack Gallagher
#//*** Course Title: CSC 362 Artificial Intelligence Spring 2024
#//*** Submission Date: 5/12/2024
#//*** Assignment: Final Project
#//*** Purpose of Program: Borrowed code used to convert a binary image to a matrix of 0s and 1s and save to a text file
#//***                     Mainly used to help establish the matrix used for the main project
#######################################

# at the command prompt type:
# pip install opencv-python


# OpenCV is a library of programming functions for computer vision applications
import cv2
import numpy as np

# Load the image
image = cv2.imread('floor_plan.jpg')

# Check if the image was loaded successfully
if image is None:
    print("Error: Unable to load image.")
    exit(1)

# Resize the image to 50x50
resized_image = cv2.resize(image, (36, 30))

# Convert the resized image to grayscale
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Threshold the image
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

# Invert the binary image
binary = cv2.bitwise_not(binary)

# Convert the binary image to a matrix of 0s and 1s
matrix = (binary / 255).astype(int)

# Save the matrix into a text file
np.savetxt('matrix.txt', matrix, fmt='%d')

print("Matrix saved to wall_matrix.txt")



