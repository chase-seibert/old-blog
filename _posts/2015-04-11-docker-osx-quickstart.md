---
layout: post
title: Docker/OSX Quickstart (not grokking docker yet? start here)
tags: docker
---

Docker has only been around since 2013, but it seems like it's all over my Twitter feed and RSS reader. I've gone trough the "Hello world" example in the past, but never felt like I really understood either the value proposition, or exactly how it works. This week, I had some time to sit down and give it more of my attention. What I found was that it was neither as mysterious or as complicated as I anticipated.

## Installing on a Mac

Docker was born on Linux and uses Linux internals like [LXC](https://linuxcontainers.org/) to work its magic. There is a Windows native version in the works (not that anyone cares). But given that software engineering in the Bay Area is dominated by Macs, let's start by looking at how to get this installed and running on OSX.

First off, don't try to install it via `brew`, or any other package manager. Docker is written in Go, which has the advantage of compiling down to dependency-less binaries. Plus, the project is moving so fast that the versions in package managers are out of date. So, suck it up and install it manually by [downloading the binary](https://github.com/boot2docker/osx-installer/releases/tag/v1.5.0).

If you can open a terminal and run `docker --version`, you're good to go. This tutorial is for version 1.5.0.

## Boot2Docker

If you try to run a docker image now, you will get an cryptic error like `docker max dial unix /var/run/docker.sock: no such file or directory`. This is because the Docker daemon process is not running. Actually, it cannot run on a Mac! Instead, you *must* use [boot2docker](http://boot2docker.io/), which is a tiny virtual machine that runs in VirtualBox and has the Docker daemon. Again, use the binary installer (sorry!).

To get up and running, open a terminal the run the following.

```bash
boot2docker init
boot2docker up
eval "$(boot2docker shellinit)"
docker run ubuntu:14.04 /bin/echo 'Hello world'
```

That's your hello world example. Let's breakdown what's happening here. `boot2docker init` creates a new virtual machine in VirtualBox.

![boot2docker](/blog/images/boot2docker.png)

The next step, `boot2docker up` runs the virtual machine. The `eval "$(boot2docker shellinit)"` step is setting some environment variables that tell Docker what container context you are currently in. If you run just `boot2docker shellinit` by itself, you can see the raw output:

```bash
Writing /Users/chase/.boot2docker/certs/boot2docker-vm/ca.pem
Writing /Users/chase/.boot2docker/certs/boot2docker-vm/cert.pem
Writing /Users/chase/.boot2docker/certs/boot2docker-vm/key.pem
export DOCKER_HOST=tcp://192.168.59.104:2376
export DOCKER_CERT_PATH=/Users/chase/.boot2docker/certs/boot2docker-vm
export DOCKER_TLS_VERIFY=1
```

The first three lines are just informational, only the last three lines are printed to stdout.

The last line, `docker run ubuntu:14.04 /bin/echo 'Hello world'` actually instantiates a new Docker container (using Ubuntu 14.04), and runs a single command inside it.

### A Note about Containers

Containers are little sandboxed Linux instances. Images are the serialized file definition that containers are spun up from. The magic of Docker is that the images are completely portable. This concept escaped me at first. I was under the impression that you needed to build an image on your Mac to run it there, and then build a separate image on Amazon EC2 to run the same thing there.

In fact, you can build an image on your Mac, and then essentially `scp` that file up to AWS and run it. In reality, you don't even need to copy it manually, that's what Docker Hub is for.

Also, the Linux distribution used inside your Docker container does NOT have to match the distribution of the host operating system. You can run Ubuntu inside a CentOS host, and visa-versa.

Finally, images have a built-in [layering mechanism](https://docs.docker.com/terms/layer/). Essentially, you can have a base image and then any number of small layers of diffs on top of that. This is a powerful optimization and abstraction, which we will talk about later.

## Example Python Flask App

This is the canonical tutorial for Python folks getting started with Docker, and yet I could not complete is successfully with any of the documentation I found. Here is my own special snowflake version.

First, create a new directory called `flask`. Inside, you are going to create three files.

The first file is called `app.py`, which is just a simple hello world Flask app.

```python
from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

Then, create a `requirements.txt` file to list Flask as a dependency:

```bash
Flask==0.10.1
```

Finally, create your `Dockerfile`:

```bash
FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app.py
```

Let's take a moment and breakdown this last file. The `FROM` line tells Docker to base this container off of a named image in the public repository called `python`, and to use the named tag of that image (kind of like a version) of `2.7`.

The `ADD` line copies your code from the current directory `.` to `/code` inside the Docker container Linux instance. `WORKDIR` settings the working directory there as well.

`RUN` can be specified multiple times. It tells Docker to run these commands when building the container for the first time. Run steps are actually cached; changing one of them later will only result in that one being run again. This is possible due to the container layering we talked about earlier.

`EXPOSE` tells Docker that the container will be serving port 5000 externally. This is the port we will run the flask app on.

Finally, the `CMD` line specifies the command that will run inside the container as your main daemon process. If you need multiple daemons, look into [docker-compose](https://docs.docker.com/compose/).

### Run it

To run the example, execute the following commands:

```bash
open "http://$(boot2docker ip):5000"
docker build -t flask-example .
docker run -it -p 5000:5000 -v $(pwd):/code:ro flask-example
```

This should have opened a browser tab before spawning flask. That likely came up with a "This webpage is not available" error page, but if you refresh it now, you should see your "Hello World!" text.

What you have done is create a named image called `flask-example` and run it. You can even edit the code on your local file system and it will sync over to Docker (thanks to `-v`) and flask will restart.

## Running the same container on AWS

Now, let's look at how to run that same container on AWS. First, go sign up for [Docker Hub](https://hub.docker.com/). It's free.

Let's assume your Docker Hub username is `foobar`. First, re-build and publish your image:

```bash
docker build -t foobar/flask-example .
docker login
docker push foobar/flask-example
```

Now, create a new EC2 instance. Make sure to use the "Amazon Linux" base image, which will make installing Docker easier. SSH into your instance and run the docker container:

```bash
sudo yum install -y docker; sudo service docker start
sudo docker run -it -p 8000:5000 foobar/flask-example
```

The first line simply installs Docker and starts it. The second line pulls down your image from Docker Hub (note: no need to authenticate!), runs it in an interactive shell, and maps the external port 8000 on the host EC2 instance to port 5000 inside the container.

If you have your security group setup to expose port `8000`, you should be able to open this EC2 public host name on port 8000 in a web browser.

# More Stuff

When I was getting started with this, I made the mistake of reading about and trying to leverage `docker-compose` and `docker-machine` right away. These are official plugins, which ease the configuration of multi-service and multi-machine capabilities in Docker, respectively. I suggest NOT starting in with those until you have the above basics buttoned down. I found that they clouded my understanding of what was happening at first.
