# README

This package contains a micro-application framework for performing medical image analysis on a clinical PACS.

## Run development server

### Installation

```
pip install git+https://github.com/johncolby/rad_apps
```

### Setup

Create a `.env` configuration file using the template at [`.env_template`](.env_template).

### Start application services

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
## Run production docker cluster

### Setup

1. Install [`docker`](https://www.docker.com/get-started).

1. Initialize swarm mode (e.g. `docker swarm init` for a simple one node swarm). This is only needed the first time you use swarm mode.

1. Clone the `rad_apps` repository.

    ```
    git clone https://github.com/johncolby/rad_apps
    cd rad_apps
    ```

1. Make sure an appropriate [`.env`](.env_template) file is available in the current directory.

### Start cluster
```bash
bash -c "docker stack deploy -c <(docker-compose config) rad_apps"
```

This command will automatically parse the [`docker-compose.yml`](docker-compose.yml) cluster specification, download the requisite docker images including [`johncolby/rad_apps`](https://hub.docker.com/r/johncolby/rad_apps), and spin up the cluster.

In some use cases you might find yourself needing to connect other containers to the `rad_apps_net` overlay network. For example, to spin up a GPU-enabled deep learning model library, and connect it to the app cluster, one could do something like this:
```
docker run --gpus 1 -itd --network rad_apps_net --name mms -p 8082:8082 -v /home/jcolby/Research/mms/:/mms awsdeeplearningteam/multi-model-server:nightly-mxnet-gpu multi-model-server --start --mms-config /mms/config.properties --model-store /mms --models gbm=gbm.mar heme=heme.mar
```
This tells docker to:

1. Fetch the `multi-model-server` image from docker hub (if not already done so).
1. Launch a container instance named `mms` with 1 available GPU, connect it to the `rad_apps_net` overlay network, and bind mount our local model store so it is available within the container.
1. Launch `multi-model-server` with the following command line arguments: `--start --mms-config /mms/config.properties --model-store /mms --models gbm=gbm.mar heme=heme.mar`

While beyond our scope here, more info on mms is available at [`awslabs/multi-model-server`](https://github.com/awslabs/multi-model-server).

### Useful cluster management commands
```bash
docker stack ls
docker stack services rad_apps
docker container ls
docker service logs -f --no-task-ids rad_apps_worker
docker service ps rad_apps_worker --no-trunc
docker service scale rad_apps_web=2 rad_apps_redis=2 rad_apps_worker=8
```

### Stop cluster
```bash
docker rm -f mms
docker stack rm rad_apps
```

***
## Build docker image (optional)

```
cd /path/to/rad_apps
```

Make sure an appropriate [`.env`](.env_template) file is available in the current directory.

Build image:
```bash
docker-compose build
```
or
```
docker-compose build --no-cache
```
