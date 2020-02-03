#!/bin/bash

# Usage 1: sh deploy_app.sh
# Usage 2: sh deploy_app.sh <CLUSTER NAME> <SERVICE NAME> <TASK FAMILY>

CLUSTER=Sentiment-Analyser-Cluster # $1
SERVICE=sentiment-analysis-service # $2
TASK_FAMILY=apis                   # $3

echo ${CLUSTER}
echo ${SERVICE}
echo ${TASK_FAMILY}

# Get the current task definition
TASK_DEFINITION=$(aws2 ecs describe-task-definition --task-definition "${TASK_FAMILY}")
echo ${TASK_DEFINITION}

# Use 'jq' (json processor) to read current container and task properties
CONTAINER_DEFINITIONS=$(echo "$TASK_DEFINITION" | jq '. | .taskDefinition.containerDefinitions')
TASK_EXEC_ROLE_ARN=$(echo "$TASK_DEFINITION" | jq '. | .taskDefinition.executionRoleArn | tostring' | cut -d'/' -f2 | sed -e 's/"$//')
TASK_CPU=$(echo "$TASK_DEFINITION" | jq '. | .taskDefinition.cpu | tonumber')
TASK_MEMORY=$(echo "$TASK_DEFINITION" | jq '. | .taskDefinition.memory | tonumber')

echo ${CONTAINER_DEFINITIONS}

# SIA -> LR
CONTAINER_DEFINITIONS=$(echo "$CONTAINER_DEFINITIONS" | sed 's@568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-repository:latest@568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-docker:latest@')
# LR -> SIA
#CONTAINER_DEFINITIONS=$(echo "$CONTAINER_DEFINITIONS" | sed 's/568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-repository:latest/568495135738.dkr.ecr.ap-southeast-2.amazonaws.com/sentiment-analysis-docker:latest/')

echo ${CONTAINER_DEFINITIONS}

# Register new task. No change to container definition.
aws2 ecs register-task-definition --family ${TASK_FAMILY} --requires-compatibilities FARGATE --network-mode awsvpc --task-role-arn $TASK_EXEC_ROLE_ARN --execution-role-arn $TASK_EXEC_ROLE_ARN --cpu ${TASK_CPU} --memory ${TASK_MEMORY} --container-definitions "${CONTAINER_DEFINITIONS}"

# Update service to use new task defn - This should pick the new image for the new revision of task defn
aws2 ecs update-service --cluster "${CLUSTER}" --service "${SERVICE}"  --task-definition "${TASK_FAMILY}"