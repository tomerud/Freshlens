# Freshlens

![image](https://github.com/user-attachments/assets/f8d4a865-584b-4bf8-afbe-fa5c1091537b)

## About

FreshLens is a innovative project developed during our university E-commerce workshop (0368-3557).
in the workshop we have worked with MBA and design students, in order to develop our own project.

FreshLens aims to transforms any standard refrigerator into a smart fridge by combining affordable cameras and machine learning tech.  
The system detects and tracks products in the fridge, monitors their freshness (by leveraging DL module), provides alerts, purchase recommendations, and recipe suggestions to reduce food waste and improve consumer habits.


## Table of Contents

- [Main Features](#main-Features)
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
- **Data Visualization and Analytics**: Displays fridge statistics and consumption.
- **Recipe Suggestions**: Recommends recipes using the available ingredients in the fridge.
- **Highly Responsive App**: Receive real-time alerts about your products and fridge


<img src="https://github.com/user-attachments/assets/d0cd3a48-56eb-4912-8b85-32657afcac47" alt="App Screenshot" width="300" />


## Technologies Used
- **Frontend:** React.js , TypeScript, Vite.
- **Backend:** Rest API using Flask (Python), prophet (for data science).
- **Database:** MySQL, MongoDB.
- **Deep learning:** Pytourch, YOLO, DeepSORT.
- **OCR:** EasyOCR.
- **LLM:** OpenAI.
- **Streaming Protocol:** RTSP (Real-Time Streaming Protocol).
- **WebSocket:** For real-time data communication between module and backend.


![image](https://github.com/user-attachments/assets/a3949139-635d-4753-bc09-0d897cea7904)


for a more detailed documentation about the feature and implementation, we have a more comprehensive readme in the folders for each of the app components


[Frontend documentation](https://github.com/tomerud/Freshlens/blob/main/frontend/README.md), 
[Backend documentation](https://github.com/tomerud/Freshlens/blob/main/backend/README.md) and
[Module Documentation](https://github.com/tomerud/Freshlens/blob/main/module/README.md)


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
npm run dev
```

in freshlens/backend/mysqlDB, put a .env file in this format:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=  # fill your password
DB_NAME=freshlens
USDA_API_KEY=  # fill USDA API key
KAGGLE_DATASET=joelmills2/canadian-grocery-store-prices
KAGGLE_FILE_PATH=atlantic_superstore.csv
```

[you can get a USDA_API_KEY here](https://www.ers.usda.gov/developer/data-apis)
we have used OpenAI api key for generating recipes, to have that option working, you will need to replace it with your own.

## Usage
If its your first time, make sure you Go to freshlens-> backend and run the create table script:
```bash
cd backend
python -m mysqlDB.create_tables
```

and then also create the mongodb:
```bash
cd backend
python -m mongo.create_db
```

Set up backend server (for communicating between front and back):
```bash
cd backend
python server.py
```

Set up websocket server between module and backend:
```bash
cd backend
python -m module_connect
```

Start the app
```bash
cd frontend
npm run dev
```

To run a video file:
- First change the settings in the run_demo: Ip, Port and path to the video you want to run
(for now there is a "defult" setting that do work if you want to run as is)
then
from freshlens folder run the following code:

``` bash
cd freshlens
python -m module.run_demo
```


- Another option, [set up RTSP server on the computer](https://github.com/insight-platform/Fake-RTSP-Stream), change the settings in scheduler file and run
from freshlens folder

``` bash
python -m module.scheduler
```

for the updates from the module to be shown at the app, the Ip camera that is inserted must be connected to the user_id is on the app.

## Acknowledgements

special thanks to all our friends and teammates, from Tel Aviv University MBA:
- Abby Levi: Growth Marketing
- Matt Kornowitz - Strategic Finance
- Mitchell Glazer - Business Development

and from Shenker design school:
- Dana Adler - Product Designer
- Shay Zipori - Product Designer

special thanks to the university E-commerce Workshop stafff: 
- Slava Novgorodov - our computer science lecturer
- Yuval Ran-Milo - our computer science TA
- Tamar Many - Design Thinking Lecturer
- Nir Tober - Product Designer

For providing the platform and guidance for this project.

## Contributors
**Sofia Panchenko:** FullStack Developer - Built the responsive user interface using React.js, TypeScript, and Vite, and played a key role in integrating backend functionalities with the Flask REST API,
developed the app's authentication system, integrating secure Google login for user access.

**Tomer Rudnitzky:**  DBA – Designed and managed the database architecture using MySQL for relational data and MongoDB for image storage, ensuring efficient fridge inventory management. implemented REST API endpoints.

**Elya Avital:** Deep learning Engineer - Worked on building the largest possible database for deep learning models within the given time constraints. Trained the neural network for freshness classification, validated OCR results, and integrated the OpenAI API for recipe generation.

**Elad Shaba:** Deep learning and Computer vision Engineer  - Responsible for the development of object detection and tracking algorithms using YOLO and DeepSORT. Tasks include integrating deep learning models, designing the module logic and functions to achieve detection, tracking, and expiry date estimation (using neural networks and OCR), and setting up the WebSocket connection for secure and fast communication between the module and backend.
For a detailed overview of the responsibilities and functionality of the module, please read the README file located in the module folder.
