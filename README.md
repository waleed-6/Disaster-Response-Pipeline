
# Disaster-Response
![alt text](https://github.com/waleed-6/Disaster-Response-Pipeline/blob/main/Screenshots/Screenshot3.png)

### Table of Contents

1. [Description](#Description)
2. [files in the repository](#files)
3. [Installation](#installation)
4. [Screenshots](#Screenshots)
5. [Results](#results)


## Description <a name="Description"></a>

Analyzing message of different disaster have greet impact on ability to help other in need 
That can really help  in saving people live , this project is part of data science nanodegree 
Using NLP we were able to analyze message that predict the type of disaster 
The project contain 3 key :
1-	Building ETL pipeline 
2-	Building machine learning pipeline 
3-	Run app that predict type of disaster in real time 

## files in the repository <a name="files"></a>
~~~~~~~
app
| - template
| |- master.html # main page of web app
| |- go.html # classification result page of web app
|- run.py # Flask file that runs app
data
|- disaster_categories.csv # data to process
|- disaster_messages.csv # data to process
|- process_data.py
|- InsertDatabaseName.db # database to save clean data to
models
|- train_classifier.py
|- classifier.pkl # saved model
Screenshots
|- Screenshots1
|- Screenshots2
|- Screenshots3
|- Screenshots4
|- Screenshots5
README.md
~~~~~~~

## Installation <a name="installation"></a>

```
git clone https://github.com/waleed-6/Disaster-Response-Pipeline
```
### To create a processed sqlite db
```
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```
### To train and save a pkl model
```
python ./models/train_classifier.py './data/InsertDatabaseName.db' './models/model.pkl'.
```
### To deploy the application locally
```
python run.py
```

## Screenshots<a name="Screenshots"></a>
![alt text](https://github.com/waleed-6/Disaster-Response-Pipeline/blob/main/Screenshots/Screenshot%201.png)

-------------------------------
![alt text](https://github.com/waleed-6/Disaster-Response-Pipeline/blob/main/Screenshots/Screenshot%202.png)



## Results<a name="results"></a>
the massage 'i am thirsty' is enterd 
![alt text](https://github.com/waleed-6/Disaster-Response-Pipeline/blob/main/Screenshots/Screenshot4.png)

and the result category was

![alt text](https://github.com/waleed-6/Disaster-Response-Pipeline/blob/main/Screenshots/Screenshot%205.png)

