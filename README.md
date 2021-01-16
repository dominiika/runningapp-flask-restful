# runningapp-flask-restful

##### ** **The application is still in development** **

This is an application which enables the user to track their trainings. The user can add trainings to the database, calculate calories burnt during a training, calculate BMI and daily caloric needs.

## Built with 

- Python 3.8.0
- Flask 1.1.2
- Flask-RESTful 0.3.8

## Getting started 

### Installing and Prerequisites

##### To run the app locally using Docker:

1. Clone this repository and cd into its directory.

2. Create a Docker image:
```
docker build -t runningapp:latest .
```

3. Create a volume:
```
docker volume create runningapp_data
```

4. Create a container and mount the volume in it:
```
docker run --network host --name runningapp -d -v runningapp_data:/runningapp runningapp
```

5. Start a container:
```
docker start [container_id]
```

6. You can visit the app at port 5000.

7. To stop the server, type:
```
docker stop [container_id]
```

8. To see running containers, type:
```
docker ps
```
<br/>

##### To run the app locally using virtual environment:
1. Clone this repository.

2. Create virtual environment and run it:

```
virtualenv venv

source venv/bin/activate
```

3. Go into the app directory and install dependencies:

```
cd /runningapp-flask-restful
pip install -r requirements.txt
```

4. Run the server:

```
python3.8 run.py
``` 

5. You can visit the app at http://127.0.0.1:5000 or http://localhost:5000

## Running tests

The app contains unit tests. <br/> To run them, use the following command:

```
python -m unittest discover
``` 

To test the linting, run:
```
flake8
```

To lint all the files, run:
```
black .
```
