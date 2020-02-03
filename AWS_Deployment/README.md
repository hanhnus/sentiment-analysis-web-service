# AWS Depolyment

Create and run Docker container on AWS ECS as a Fargate task using CloudFormation and CLI.

## Table of Contents

- [Push Docker Image to AWS ECR](#Push-Docker-Image-to-AWS-ECR)
- [Create CloudFormation Stack (All-in-one)](#Create-CloudFormation-Stack-(All-in-one))
- [CloudWatch Metrics](#CloudWatch-Metrics)
- [Switch between ML Models running in AWS](#Switch-between-ML-Models-running-in-AWS)
- [Appendix - Create CloudFormation Stacks (Step-by-step)](#Appendix---Create-CloudFormation-Stacks-(Step-by-step))
  - [VPC Stack](#VPC-Stack)
  - [IAM Stack](#IAM-Stack)
  - [ECS Cluster Stack](#ECS-Cluster-Stack)
  - [ECS Task Stack](#ECS-Task-Stack)


## Push Docker Image to AWS ECR
```
# create ECR repository
aws2 ecr create-repository --repository-name sentiment-analysis-api

# login to ECR
aws2 ecr get-login --no-include-email --region ap-southeast-2

# get the repo uri from the return of
aws2 ecr describe-repositories --repository-name sentiment-analysis-api

# push Docker Image to the repo on ECR
docker tag sentiment_analysis_image:v2.0 568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-api:v2.0
docker push 568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-api:v2.0
```

## Create CloudFormation Stack (All-in-one)

The Yaml file https://github.com/atomic-app/sentiment-docker/blob/master/AWS_Deployment/all-in-one.yml will create or define VPC, subnets, internet gateway, route table, IAM roles(for the container), ECS cluster, application load balancer, load balance listner, CloudWatch Log Group, security groups and ECS task.

```
aws2 cloudformation create-stack --stack-name all-in-one --template-body file://~/Documents/AWS/CloudFormation/Docker-on-ECS/infra_sentiment_analysis/all-in-one.yml
```

## CloudWatch Metrics
<img src="https://github.com/hanhnus/sentiment-analysis-web-service/blob/master/images/CloudWatch_metrics.png"/>

## Switch between ML Models running in AWS

By running the Shell file https://github.com/atomic-app/sentiment-docker/blob/master/AWS_Deployment/deploy_app.sh, the ML model running behind the app can be switched within a short time. The Docker Image with the new model needs to be uploaded together with app as an ECR Image. And either one of below statements can be run or commented in the Shell file.

Switch from Vader sentiment model to Support Vector Classifier model:
```
# Vader -> SVC
CONTAINER_DEFINITIONS=$(echo "$CONTAINER_DEFINITIONS" | sed 's@568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-repository:latest@568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-docker:latest@')
```

Switch from Support Vector Classifier model to Vader sentiment model:
```
# SVC -> Vader
CONTAINER_DEFINITIONS=$(echo "$CONTAINER_DEFINITIONS" | sed 's/568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-repository:latest/568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-docker:latest/')
```

## Appendix - Create CloudFormation Stacks (Step-by-step)

Create CloudFormation stack to define infrastructure and resources to run the container application on ECS, by defining CloudFormation stack templates to create VPC, subnets and resources to define Internet gateway and drop tables, etc.

### VPC Stack

VPC Stack CloudFormation template:
https://github.com/atomic-app/sentiment-docker/blob/master/AWS_Deployment/step-by-step/vpc.yml

The creating of VPC and subnets will also involve defining internet gateway, route tables and so on.

```
aws2 cloudformation create-stack --stack-name vpc --template-body file://~/Documents/AWS/CloudFormation/Docker-on-ECS/infra_sentiment_analysis/vpc.yml
```
Successful response:
```
{
    "StackId": "arn:aws:cloudformation:ap-southeast-2:568495135738:stack/vpc/5704f490-3f44-11ea-8d9a-06e276ca85be"
}
```
Result can be varified in CloudFormation

### IAM Stack

IAM Stack CloudFormation template:
https://github.com/atomic-app/sentiment-docker/blob/master/AWS_Deployment/step-by-step/iam.yml to create IAM roles for the containers to be able to interact with CloudWatch and ECR.

```
aws2 cloudformation create-stack --stack-name iam --template-body file://~/Documents/AWS/CloudFormation/Docker-on-ECS/infra_sentiment_analysis/iam.yml --capabilities CAPABILITY_IAM
```
Successful response:
```
{
    "StackId": "arn:aws:cloudformation:ap-southeast-2:568495135738:stack/iam/d119eab0-3f58-11ea-bc13-06d8fa8d4244"
}
```

### ECS Cluster Stack

ECS Cluster Stack CloudFormation template:
https://github.com/atomic-app/sentiment-docker/blob/master/AWS_Deployment/step-by-step/app-cluster.yml to create ECS cluster, application load balancer, load balance listner & CloudWatch Log Group (for container application logs); also create several security groups.

```
aws2 cloudformation create-stack --stack-name sentiment-analyser-cluster  --template-body file://~/Documents/AWS/CloudFormation/Docker-on-ECS/infra_sentiment_analysis/app-cluster.yml
```
Successful response:
```
{
    "StackId": "arn:aws:cloudformation:ap-southeast-2:568495135738:stack/sentiment-analyser-cluster/0e5b3bf0-3f5d-11ea-977a-0276b5cf65f2"
}
```

### ECS Task Stack

ECS Task Stack CloudFormation template:
https://github.com/atomic-app/sentiment-docker/blob/master/AWS_Deployment/step-by-step/api.yml to create the task that deploys our container image from ECR repo into ECS cluster.

```
aws2 cloudformation create-stack --stack-name api --template-body file://~/Documents/AWS/CloudFormation/Docker-on-ECS/infra_sentiment_analysis/api.yml
```
Successful response:
```
{
    "StackId": "arn:aws:cloudformation:ap-southeast-2:568495135738:stack/api/aa7efcc0-3fde-11ea-b60c-0643e0359b60"
}
```
The stack can be deleted by
```
aws2 cloudformation delete-stack --stack-name api
```
