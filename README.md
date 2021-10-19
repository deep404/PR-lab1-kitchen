# PR-lab1-kitchen

> Network Programming Laboratory Work No1 [Kitchen]
>
> FAF 192
>
> Moglan Mihai
> 


More detailed README will be added later!


#### Run

```bash
$ docker build -t kitchen . # create kitchen image
$ docker network create pr_lab1 # create docker network 
$ docker run -d --net pr_lab1 --name kitchen kitchen # run docker container on created network
```

