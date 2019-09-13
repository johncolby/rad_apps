# README

## Installation

```
pip install <repo_URL>
```

## Setup

Create a configuration file using the template at [.env_template](.env_template)

## Development server

1. Start `redis`.

    ```bash
    sudo docker run -d -p 6379:6379 --name redis redis

    ```

1. Start `rq`.

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

## Production docker cluster

```
cd /path/to/rad_apps
```

Make sure an appropriate `.env` file is available in the current directory.

Build
```bash
sudo docker-compose build
sudo docker-compose build --no-cache
```

Startup
```bash
sudo bash -c "docker stack deploy -c <(docker-compose config) rad_apps"
sudo docker run --gpus 1 -itd --network rad_apps_net --name mms -p 8082:8082 -v /home/jcolby/Research/brats_service/:/mms mms:latest mxnet-model-server --start --model-store=/mms --models unet=unet.mar
```

Cluster management notes
```bash
sudo docker stack ls
sudo docker stack services rad_apps
sudo docker container ls
sudo docker service logs -f --no-task-ids rad_apps_worker
sudo docker service ps rad_apps_worker --no-trunc
sudo docker service scale rad_apps_worker=2
```


Shutdown
```bash
sudo docker rm -f mms
sudo docker stack rm rad_apps
```