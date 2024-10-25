# Udin backend task

This project is an application built using FastAPI, SQLModel, and Docker. It handles champions and their base stats for a game called league of legends.

## Overview
The project is a simplified version of a league of legends champion resource, with its base stats. The design was implemented with extension in mind, for example a champion can have multiple skills in the future and it will be implemented the same way
base stats was implemented.
####
The app uses SQLmodel as an orm which is built on top of sqlalchemy and pydantic. It also uses
FastAPI as a web server.
####
All commands are best run through the provided MAKE file, it abstracts the interactions with the system through a series of pre-defined commands that makes it easier to interact with the app.
####
The app contains an auto-generated docs using swagger that can be used to try out the app routes.
####
The app structure was designed to go with a larger codebase for demonstration purposes.
####
Environment variables and secrets are included in the docker-compose file to make it easier to run the project without the hassle of creating a .env file on your machine, in typical production environment this should not be the case.

## Setup Instructions
### Prerequisites
Before you begin, ensure you have met the following requirements:
1. Docker & Docker Compose
2. Make

### Cloning the Repository
```bash
git clone git@github.com:abdelrahmenAyman/udin-task.git
cd udin-task
```
### Running the Project
To start the server, run:
```bash
make run
```
To start the server in detached mode (background):
```bash
make run-detached
```
### Running Tests
To run the test suite, execute:
```bash
make test
```
### Building Docker Images
To build the Docker image for the project:
```bash
make build
```
To build the Docker image for testing:
```bash
make build-test
```
### Stopping and Cleaning Up Containers
To stop all running containers:
```bash
make stop
```
To remove all containers, networks, and volumes:
```bash
make down
```
## Accessing API Documentation
To access the API documentation, navigate to:
http://localhost:8000/docs
This will provide interactive documentation of your API using Swagger.