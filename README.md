# To-Do-List

To-Do-List is mini-project made with Flask and MongoDB. Dockerfile is also available to make docker image and docker containers.

## Built using :
```sh
	Flask : Python Based mini-Webframework
	MongoDB : Database Server
	Pymongo : Database Connector ( For creating connectiong between MongoDB and Flask )
	HTML5 (jinja2) : For Form and Table
```
## Using [Docker](https://www.docker.com) [Docker-Compose](https://docs.docker.com/compose)

Make sure that you are inside the project directory, where `docker-compose.yaml` file is present. Now, building and running the application server container and mongodb container using `docker-compose` :
```
Building or fetching the necessary images and later, creating and starting containers for the application
    $ docker-compose up -d

Go to http://localhost with any of browsers and DONE !!
    $ open http://localhost
```

### Running, Debugging and Stopping the application under the hood
```
For almost all of the `docker-compose` commands, make sure that you are inside the project directory, where `docker-compose.yaml` file is present.

Passing `-d` flag along with docker-compose, runs the application as daemon
    $ docker-compose up -d

Seeing all of the logs from the application deployed.
    $ docker-compose logs

Stopping the application
    $ docker-compose down
```

## Screenshot :

![Screenshot of the Output](https://github.com/CoolBoi567/ToDo-List-using-Flask-and-MongoDB/blob/master/static/images/screenshot.jpg?raw=true "Screenshot of Output")
