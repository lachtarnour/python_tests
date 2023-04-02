# python_tests

## environment variables

Create an `environment.env` file to store environment variables.


|Variable|Meaning|Required| Default value | 
|---|---|---|---|
|SOURCE_PATH| Path of the folder containing files to parse | true ||
|NOTIFICATION_EMAIL| EMAIL adress to notify | true ||


## Use docker

build: 

```bash
DOCKER_BUILDKIT=1 docker build -t data_engineer:latest .
```
Run:

```bash
docker run --env-file environment.env data_engineer:latest
```
