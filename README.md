# Chatbot Concierge

## Objective

This is a simple chatbot that briefly converses with the user and finds restaurants based on the conversation from the yelp databse and sends a text message of the recommendations.

This was a part of Cloud Computing course at New York University, and was a way to get used to various AWS services

Following services were used in building this application out

* S3
* API Gateway
* Lambda
* Lex
* SQS
* SNS
* Elastic Search
* DynamoDB
* Yelp API for data sourcing

## Architechture

![](img/arch.png)

## Components and Flow

* **S3** is used to host the [frontend](frontend/) of the site
* **API Gateway** is used to connect the frontend with our chatbot and is defined by [api.yaml](api/api.yaml)
* **Lambda** hosts many functions, one of them is [entry](lambdas/entry.py) which acts as an interface between the user and **Lex**
* [lex-validation](lambdas/lex-validation.js) is another **Lambda** function that works with **Lex** to validate input and finally send the gathered information to an **SQS** queue
* Every minute through **CloudWatch** events we trigger another **Lambda**, [recommendations](lambdas/recommendations.py].
* [recommendations](lambdas/recommendations) uses the data from the **SQS** entry to search for relevant results using **Elastic Search** and get detailed information about the restaurants from **DynamoDB**.
* Then it constructs and sends a text message filled with recommendations to the user using **SNS**

NOTE:
Data is first scraped using the **Yelp API**, stored in **DynamoDB** for quick access and indexed in **Elastic Search** for quick search.
[Development code](development_code) contains the programs used to accomplish this.




