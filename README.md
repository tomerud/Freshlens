# Freshlens

![image](https://github.com/user-attachments/assets/f8d4a865-584b-4bf8-afbe-fa5c1091537b)

## About

FreshLens is a innovative project developed during our university E-commerce workshop.
in the workshop we have worked with MBA and design students, in order to develop our own project.

IMAGE FROM PRESENTATION
IMAGE FROM PRESENTATION

FreshLens aims to transforms any standard refrigerator into a smart fridge by combining affordable cameras and machine learning tech.  
The system detects and tracks products in the fridge, monitors their freshness (by leveraging DL module), provides alerts, purchase recommendations, and recipe suggestions to reduce food waste and improve consumer habits.


## Table of Contents

- [Main Features](#main-Features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Project Status](#project-status)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)


## Main Features
- **Item Detection and Tracking**: Automatically identifies and monitors items placed in the refrigerator using YOLO and DeepSORT algorithms.
- **Freshness Monitoring**: Utilizes OCR to read expiration dates and YOLO to estimate the freshness level.
- **Real-Time Notifications**: Alerts for items nearing expiration.
- **Purchase Recommendations**: Suggests grocery purchases based on inventory levels and user preferences - in progress.
- **Data Visualization**: Displays fridge statistics and consumption - in progress.
- **Recipe Suggestions**: Recommends recipes using the available ingredients in the fridge.
***SOFIA: PLEASE ADD MORE ABOUT THE APP, FOR EXAMPLE:***
- **Highly Responsive App**: something something from front end README
- **User Authentication**: Secure login by using Google account.


## Demo

```![Project Demo](link-to-demo-gif-or-video)```  


## Core Technologies Used
- **Frontend:** React.js , TypeScript, Vite.
- **Backend:** Rest API using Flask (Python), prophet (for data science).
- **Database:** MySQL, MongoDB.
- **Deep learning:** Pytourch, YOLO, DeepSORT.
- **OCR:** EasyOCR.
- **LLM:** LangChain, gemini, OpenAI.
- **Streaming Protocol:** RTSP (Real-Time Streaming Protocol).
- **WebSocket:** For real-time data communication between module and backend.

![image](https://github.com/user-attachments/assets/a3949139-635d-4753-bc09-0d897cea7904)



## Project Status
While we have developt quite a bit, there are still things to expand this project, that due to time and money constraints we were unable to expand upon for now:
- Increase the dataset size for training the deep learning module.
- Switch to multi headed NN structure.
- Migrate to cloud services.
- Improve and expand the data science component.
- Enable other sensors beside cameras (temp, humidity etc)
- Ensure secure communication between IoT components (cameras and other sensors) and the application, as well as between the frontend and backend.


## Installation

```bash
git clone https://github.com/tomerud/Freshlens.git
cd Freshlens
pip install requirements.txt

cd ../frontend
npm install
```

## Usage
***add Usage instructions***

## Acknowledgements

special thanks to all our friends and teammates, from Tel Aviv University MBA:
- Abby Levi: Growth Marketing
- Matt Kornowitz - Strategic Finance
- Mitchell Glazer - Business Development

and from Shenker design school:
- Dana Adler - Product Designer
- Shay Zipori - Product Designer

special thanks to the university E-commerce Workshop stafff: 
Slava Novgorodov - our computer science lecturer
Yuval Ran-Milo - our computer science TA
Tamar Many - Design Thinking Lecturer
Nir Tober - Product Designer

For providing the platform and guidance for this project.

## Contributors
**Sofia Panchenko:** FullStack Developer - Built the responsive user interface using React.js, TypeScript, and Vite, and played a key role in integrating backend functionalities with the Flask REST API,
developed the app's authentication system, integrating secure Google login for user access.

**Tomer Rudnitzky:**  Backend Developer and DBA – Designed and managed the database architecture using MySQL for relational data and MongoDB for image storage, ensuring efficient fridge inventory management. implemented REST API endpoints, and set up secure real-time updates with Flask-SocketIO.

**Elya Avital:** Deep learning Engineer - Worked on building the largest possible database for deep learning models within the given time constraints. Trained the neural network for freshness classification, validated OCR results, and integrated the OpenAI API for recipe generation.

**Elad Shaba:** Deep learning and Computer vision Engineer  - Responsible for the development of object detection and tracking algorithms using YOLO and DeepSORT. Tasks include integrating deep learning models, designing the module logic and functions to achieve detection, tracking, and expiry date estimation (using neural networks and OCR), and setting up the WebSocket connection.
For a detailed overview of the responsibilities and functionality of the module, please read the README file located in the module folder.
