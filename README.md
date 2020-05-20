# README

This package contains a micro-application framework for performing medical image analysis on a clinical PACS.

## Installation

```
pip install git+https://github.com/johncolby/rad_apps
```

## Setup

Create a configuration file using the template at [.env_template](.env_template).

## Run development server

1. Start `redis` message broker.

    ```bash
    docker run -d -p 6379:6379 --name redis redis

    ```

1. Start redis queue, `rq`.

    ```bash
    rq worker
    ```

1. Start `flask`.

    ```bash
    export DOTENV_FILE=/path/to/.env # generated above
    export FLASK_APP=rad_apps.py
    export FLASK_ENV=development
    flask run
    ```

***
## Build docker image

```
cd /path/to/rad_apps
```

Make sure an appropriate `.env` file is available in the current directory.

Build
```bash
sudo docker-compose build
sudo docker-compose build --no-cache
```

## Run production docker cluster

Startup
```bash
bash -c "docker stack deploy -c <(docker-compose config) rad_apps"
docker run --gpus 1 -itd --network rad_apps_net --name mms -p 8082:8082 -v /home/jcolby/Research/mms/:/mms awsdeeplearningteam/multi-model-server:nightly-mxnet-gpu mxnet-model-server --start --mms-config /mms/config.properties --model-store /mms --models gbm=gbm.mar heme=heme.mar
```

Cluster management notes
```bash
docker stack ls
docker stack services rad_apps
docker container ls
docker service logs -f --no-task-ids rad_apps_worker
docker service ps rad_apps_worker --no-trunc
docker service scale rad_apps_worker=2
```

Shutdown
```bash
docker rm -f mms
docker stack rm rad_apps
```