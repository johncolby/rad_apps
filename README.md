# README

## Individual services

1. Start `redis`.

    ```bash
    docker run -d -p 6379:6379 redis --name redis

    ```

1. Start `rq`.

    ```bash
    rq worker
    ```

1. Start `flask`.

    ```bash
    export FLASK_APP=brats_app.py
    export FLASK_ENV=development
    flask run
    ```

## Docker

Build
```bash
sudo docker-compose build
sudo docker-compose build --no-cache
```

Startup
```bash
sudo docker stack deploy -c docker-compose.yml brats_app
sudo docker run --gpus 1 -itd --network brats_app_net --name mms -p 8082:8082 -v /home/jcolby/Research/brats_service/:/mms mms:latest mxnet-model-server --start --model-store=/mms --models unet=unet.mar
```

Monitoring
```bash
sudo docker stack ls
sudo docker stack services brats_app
sudo docker container ls
sudo docker service logs -f --no-task-ids brats_app_worker
sudo docker service scale brats_app_worker=2
```


Shutdown
```bash
sudo docker rm -f mms
sudo docker stack rm brats_app
```