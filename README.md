# PR-lab1-kitchen

> Network Programming Laboratory Work No1 [Kitchen]
>
> FAF 192
>
> Moglan Mihai
> 

#### Run

```bash
$ # clone repository
$ pip install -r requirements.txt # install dependecies
$ py main.py # start the server
```

#### with docker

```bash
$ docker build -t kitchen . # create kitchen image
$ docker network create pr_lab1 # create docker network 
$ docker run -d --net pr_lab1 --name kitchen kitchen # run docker container on created network
```

