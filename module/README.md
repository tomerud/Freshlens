# FreshLens CV Module

## Table of Contents
- [Overview](#overview)
- [Example](#example)
- [Module Structure](#module-structure)
- [Main Files Explanation](#main-files-explanation)
  - [`scheduler.py`](#schedulerpy)
  - [`detect_and_track.py`](#detect_and_trackpy)
  - [`pass_obj_to_exp_date.py`](#pass_obj_to_exp_datepy)
  - [`products_ocr.py`](#products_ocrpy)
  - [`fruit_veg_freshness.py`](#fruit_veg_freshnesspy)
  - [`draw_bb.py`](#draw_bbpy)
  - [`backend_connect.py`](#backend_connectpy)
  - [`code_formatting.py`](#code_formattingpy)
- [Future Work](#future-work)
- [Configuration](#configuration)

## Overview  
This module manage the whole CV part of the app, the main tech is:
RTSP - real time streaming protocol, to get the stream from the camera in the fridge.
Object detection and tracking - using YOLO + DeepSORT
Expiration estimation - using OCR, YOLO and resNet
Websocket - to send data to the backend (encrypted)

## Example
Here we can see a video of the object detection and tracker in action,
this video was presented as part of the pitch in the workshop competition

![video of YOLO+DeepSort](assets/tracked_vid.gif)


Here we can see cheese, that was analysed with this module, first we detected the dates on the produt cover,
then we have cleaned the image of the date using cv techniques and used OCR to extract the text

Red - date bounding boxes

Black - the output of the ocr

![Picture of cheese, that using detection and ocr we got the exp date](assets/cheese_ocr.png)

## Module Structure:
```
📂 project_root/
│
│── 📂 assets/                       # for running locally
│
│── 📂 model_training/               # scripts used to train the models
│
│── 📂 models/                       # Deep Learning models to load
│
│── 📂 scripts/                      
│   ├── 📄 code_formatting.py        # Checks formatting using pylint and flake8
│   ├── 📄 run_demo.py               # Runs demo and showcases the system
│
│── 📜 README.md                     # Module documentation
│
│── 📄 backend_connect.py            # Sends data to the backend
│── 📄 detect_and_track.py           # Object detection and tracking
│── 📄 draw_bb.py                    # Draws bounding boxes based on freshness
│── 📄 fruit_veg_freshness.py        # Freshness detection using classification
│── 📄 pass_obj_to_exp_date.py       # Determines which expiration date function is needed
│── 📄 products_ocr.py               # Optical character recognition for expiration date detection
│── 📄 scheduler.py                  # Manages the system
```

## Main files explanation:


### `scheduler.py`
This script, establish the connection to the backend,
get the cameras IP and the ports, and start a thread for each camera,
each thread "listen" untill it notice an event (for now we are using light base)
once a camera start streaming, we are passing it to the "pipeline"

#### Considerations:
- We are using threads on each camera, since we are not interested in wasting resources and time on cameras that are not streaming actual changes in the fridge.
- RTSP was chosen for its low-latency streaming,and since many IP camers support RTSP, enabling real time video feeds. it was also chosen since we could find a fake server to test it, unfortunately we could not find a SRTSP server for more secure comminication.

#### Assumptions/limitations:
- GIL: even when using threads, in python, cant leverage multi cpu,
need to study more about multi proccess, async etc' options in python.
- Hardware limitation : we didnt have an actual IP camera,
so some configuration is missing (like the get event function),
we have used a fake RTSP server to mimic a IP camera functionality and to actually use the protocol.
Also, we should configurate the cameras to manually stream for a couple of seconds in case no event has happen for more than a day, since we didnt have actual camera, we were unable to preform it.
- camera IP and ports: Ideally we will have multiple copys of this module each with its own gpus, camera IP and ports to listen etc.
we "hard-coded" the camera IP and port to listen to - based on the fake RTSP server, so we only listen to this specific combination. 
We will need to switch with call to server to get the list of IP and ports that is respobsible to listen to.


### `detect_and_track.py`
This script uses YOLOv8 and DeepSORT to detect the objects in the stream and track them as they are moved.

#### Considerations:
- YOLO was chosen for its speed and efficiency in real-time object detection.
- We have chosen YOLOv8 instead of more "advanced" version like YOLOV11, since in our testing phase (admittedly small to be significant statistically) it achived the best results.

#### Assumptions/limitations:
- We started by using BotSORT, but after many problems, we have discovered there is a PR in the yolo implementation, about bug in the botSORT (still open at 23/02 ), so we have quickly transitioned over to DeepSORT that is less advanced (but still good results thanks to its kalman filter),
this occurence, limited our time to finetune the DeepSORT, since preparing the dataset is very time consuming.
- Since we have changed the dataset in the "last minute" to include more items,
we dont have enough time to train deepsort / Siamese neural network on our custom dataset,
so the tracking capabilities can be imporved 


### `pass_obj_to_exp_date.py`
This script get the detected objects (from detect_and_track), and by its category (fruits and veg or closed products), will call upon each object the right function to estimate the expiration date.


### `products_ocr.py`
This script gets a photo of a closed product, and will try to find and read the expiration date,
it uses YOLO to detect Expiration date and "expired by", then it uses EasyOCR
this function relay on a lot of "dirty work" that is in procces_img_and_date,
that does a lot of actions like cleaning the photo, validating date format etc'.

#### Considerations:
- We found OCR to give bad results if we just pass the product image, so we have trained a YOLO model to detect "dates" on the product, then the OCR only need to scan spesific places on the product, which gave much better results.
- there can be several "dates" on a product, since price can look like a valid date format (12.5 can look very similar to the model to actual date), and also production date will look the same as expiration date.
so we have trained the YOLO model to also detect words like "expired by", "BY:", " use before" etc'
if we have found a "expired by" on the product, we will analyse the biggest IOU/closest date box (since its probably the expiration date), if not, we will try to detect all the dates, and see which one give the "best" candidate for expiry date (for example, give one date of foramt DD/MM/YY, is a better canidate than DD/MM (can be actually price)).
- since the Expiration dates are not always aligned, we are using the detection bounding box to approximate the angle by which its rotated, then we rotate it and pass it to the OCR model.

#### Assumptions/limitations:
- in our testing phase (admittedly small to be significant statistically) we have found the current operations in proccess_img_and_date.preprocess_image to give the best results,
they are considerably limited and small in comparison to reccomendations we saw online, it does need more work to check and see if play adding more operations, we can reach better results.
- We tried at first to implement a more robust way to do all the above, by using [generalized framework for recognition of expiration dates](https://doi.org/10.1016/j.eswa.2022.117310), due to time and gpu limitations, we were not able to achieve it.
- ideally, the object detecion and expiration date detection will be implemented in the same NN by adding heads.
- filtering based on conf level (detail=1) is problematic because of the printing format of digits on exp dates.


### `fruit_veg_freshness.py`
Script for freshness detection using classification.

#### Considerations:
- we have used basic shelf life from USDA, foodkeeper and other resources available online, to estimate the "base" shelf life of the products

#### Assumptions/limitations:
- There is no available dataset for actual expiry date detection for fruit/veg,
while there are some similar dataset (mainly categorical), they are intended for the growing the fruit/veg phase, and not for the storing in the consumer fridge. - more on that in the future work


### `draw_bb.py`
This script take the image of the shelf (last frame from the camera stream), and draw bounding boxes on it, each product according to its expiration date (red, orange, green), this image will be passed to the app, this way we are able to display to the user its fridge content visually.


### `backend_connect.py`
This script define the functions that send data to the backend using the websocket
We have three main functions:
- send_to_db: this function send the data of what we have in the fridge and the expiration date, to be saved at MYSQL.
- send_to_mongo: this function send the image (from draw_bb) to the backend, to be saved at Mongo DB.
- alert_server: this function alert the server in case of errors.

#### Considerations:
- we considerd if each camera should have its own websocket, but we have decided it makes more sense, that each scheduler have 1 web sockets that all the cameras its responsible for will share,
since that is the design we have chosen,we use a single shared socket for all cameras (threads), guarded by a lock to enforce sequential access, and avoid concurrency issues.
- we are using a TLS websocket (as defined in scheduler), so the connection and data should be secured.
- Socket auto reconnects with exponential backoff.

#### Assumptions/limitations:
- Potential throughput bottleneck, since we have one socket and multiple cameras can wait to acquire the lock,
there is a need to research more about this type of problems


### `code_formatting.py`
Due disclosure - This file was generated with the help of ChatGPT,
this code was only run in effort to improve the formating of the code in the diffrenet files.
I have used its output (the pylint and flake8 notes) in order to practice better code writing practices,
the changes to the code in the file themself was done manually.


## Future work:
- Expand the dataSet to support more items.
- Improve object detection accuracy.
- Imporve Tracker abilities and fine tune it on the dataset.
- Switch RTSP to a more secure protocol.
- Have an actual IP camera to understand the necessary configurations
- Finetune OCR / CRNN in effort to imporve the results and recognition of expiration dates (hard to read font).
- While there is no publicly available dataset for fruit/vegetable expiration dates, there are several proposed methods to approximate the expiration date using traditional CV techniques. Unfortunately, most of the papers focus on the commercial stage (before the produce arrives at the store), but it should be possible to create similar tests to learn techniques and data that can be adapted for our usage case.
- We want to expand the TLS connection into mTLS or nginx (reverse proxy etc...)
- Learn more about Asyncio and multiprocessing as a possible alternative to threading.


## Configuration
To run the code there are two possible ways:

- use run_demo file -> upload the video you want to scan, change the ip:port so it will fit an existing user in the DB (if not, it will not know to connect the data), change the PATH to your video, choose to either connect to the backend before hand (so you will see results in the db updated - if yes, please look at the FreshLens Readme.md)
or # the connection lines and run without.

- download RTSP server on the computer,upload the files to stream using RTSP from the server,  and change the ip:port so it will fit an existing user in the DB then connect to the backend as instructed in FreshLens\README.md,
please notice you will need to "break" the listening loop by using crtl+c


Due disclosure - ChatGPT was used in this README.md file in the Module Structure part to insert the icons: 📂, 📜, 📄
