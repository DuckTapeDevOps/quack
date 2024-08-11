set dotenv-load


build:
    docker build -t $DOCKER_IMAGE .
    docker tag $DOCKER_IMAGE $ECR_ACCOUNT/$ECR_REPO:latest