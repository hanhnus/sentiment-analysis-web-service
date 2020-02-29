# Sentiment Analysis Web Service

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![standard-readme compliant](https://img.shields.io/badge/coverage-78%25-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Architecture

<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/Architecture.png"/>


## Table of Contents

- [Background](#background)
- [Feature](#feature)
- [Installation (Docker Deployment)](#installation)
- [Usage](#usage)
	- [UI in Browser](#Access-the-Sentiment-Analysis-UI-in-Browser)
	- [cURL Request in Terminal](#Send-cURL-Request-in-Terminal)
- [Testing](#API-testing)
	- [Unit Testing (pytest)](#Unit-Testing-pytest)
	- [API Testing (Swagger UI)](#API-Testing-Swagger-UI)
- [Running in AWS](#Running-in-AWS)
- [Maintainers](#maintainers)
- [Contributing](#contributing)

## Background

Sentiment analysis is a method for gauging the attitude of notifications from customers in communication with an end user or a group of end users. Based on a scoring mechanism, sentiment analysis monitors the wording and evaluates language to quantify attitudes, opinions, and emotions related to a business, product or service, or topic. 

A relative sentiment analysis score provides insight into the effectiveness of cards and also serves as a useful measurement to gauge the overall opinion on customers' services. When sentiment analysis scores are compared across certain cards, customers can identify the areas for improvement in the delivery of message. 

By monitoring attitudes and opinions about cards continuously, customers are also able to detect subtle shifts in opinions and adapt readily to meet the changing needs of their end users.

## Feature

- User Interface in Browser (Flask Framework)
- JSON Interaction through Terminal (cURL)
- Requests Error Handling
- Unit Testing (Pytest)
- API Testing (Swagger UI)
- Logging
- Docker Deployment
- Healthcheck
- AWS Deployment

## Installation

### Deploy Sentiment Analysis Server in Docker

#### Step 1: Build Docker image from Dockefile
Download https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/Dockerfile and other project files to ~/Documents/Dockerfiles/sentiment_analysis/
```
docker build -t sentiment_analysis_image:v1.0 ~/Documents/Dockerfiles/sentiment_analysis/
```
After building, images can be checked by
```
docker image ls
```

#### Step 2: Create & Run a Docker container from Docker image
```
docker run --name sentiment_analysis_container -p 99 -dit sentiment_analysis_image:v1.0
```
The port needs to be aligned with the one in https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/app.py.

#### Step 3: Attach the container and run services
```
docker attach sentiment_analysis_container
```
After attaching the Docker container, Nginx service and app will run automatically.


## Usage

### Access the Sentiment Analysis UI in Browser
```
http://localhost:32768
http://127.0.0.1:32768
```
The port to access can be checked by running:
```
docker port sentiment_analysis 
```

#### Sample Response
<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/UI_browser.png" width="600"/>


### Send cURL Request in Terminal
```
curl --header "Content-Type: application/json"    \
     --request POST                               \
     --data '{"sentence":"I love dog."}'          \
     http://localhost:32768/curl
```

```
curl --header "Content-Type: application/json" --request POST --data '{"sentence":"I love dog."}' http://localhost:32768/curl
```
#### Sample Response

<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/cURL_request.png" width="500"/>


## API Testing

### Unit Testing (pytest)

Run test case in PyCharm Terminal:
```
pytest -vv --disable-warnings
```


Tests cover:  

&emsp; - empty payload  
&emsp; - more than one element in payload (variances & cases in different sequences are also tested)  
&emsp;&emsp;&emsp; -- same key, same value  
&emsp;&emsp;&emsp; -- same key, diff value  
&emsp;&emsp;&emsp; -- diff key, same value  
&emsp;&emsp;&emsp; -- diff key, diff value  
&emsp; - one element in payload, but the key is not "sentence"  
&emsp; - JSON Decode Errors  
&emsp;&emsp;&emsp; -- value is not string  
&emsp;&emsp;&emsp; -- key is not string  
&emsp; - ML model tests  

<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/unit_test_result.png"/>

### API Testing (Swagger UI)

A bad request, as an example, is tested in Swagger UI as showed below (which contains no English letter in the input sentence), the correct error code and error message are responded.

<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/swager_API_test_1.png"/>

<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/swager_API_test_2.png"/>

## Running in AWS

<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/access_service_thr__public_IP_(AWS).png"/>

### AWS Deployment

https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/AWS_Deployment/README.md

## Maintainers

[@HanHan](https://github.com/hanhnus).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/hanhnus/sentiment-analysis-web-service/issues/new) or submit PRs.
 
