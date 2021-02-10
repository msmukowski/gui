# Recruitment task

[![image](https://img.shields.io/badge/python-3.7.0-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/version-1.0.0-informational)]()

### Recruitment task, the aim of which was to create a simple **GUI** that allows you to read the image from the **camera** and analyze it - detecting green objects along with identifying them in the image and determining whether they are round.

## Functions

- It displays real-time image from the camera detecting green objects
- It allows you to calibrate the sensitivity of the system to green color

## Dependency

* __opencv-python 4.5.1.48__
* __numpy 1.20.1__

## Usage

>- Suggested use of a virtual environment

### How to run:

1. ```console
    python3 -m venv venv 
    ```

2. > Windows: 
    ```console
    venv\Scripts\activate
    ```
    > Linux:
    ```console
    source mypython/bin/activate
    ```
    
3. ```console
    pip install -r requirements.txt 
    ```
    
4. ```console
    python main\main.py
    ```


- ## Result:

<p align="center"><img src="imgs\gui.gif" width="60%"></p>

- ### Where:
> #### The bounding box with the yellow line indicates the object in the image.

> #### The blue line shows the outline of the object.

> #### If the object is likely to be rounded, "CIRCLE" will be displayed in its center.


