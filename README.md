# flask-graphql-jwt-example
A small example of using GraphQL and JWT authentication through Auth0 in a Flask API.

## Build the Image
The first thing to do is build the docker image
```
$ docker build -t <imagename>:<tag> .
```
replacing `<imagename>` and `<tag>` with a name and tag for the image.

## Run the Container
The following command will create and run a container based on the image created above. The `-v` flag
will mount the current directory to the container so whenever you change the code the container
will be automatically updated.
```
$ docker run --name <containername> -p 5000:5000 -v $PWD:/app <imagename>
```
You can stop the container with 
```
$ docker stop <containername>
```
and start it with
```
$ docker start <containername>
```
