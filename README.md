# Скрипт трансформации -- запуск

## Docker
### Сборка образа
```shell
docker build -t cfsfmba:1.0.0 .
```
### Запуск образа
```shell
docker run -it --volume=PATH_TO_REF:/home/docker_user/ref --gpus all cfsfmba:1.0.0
```
Вместо PATH_TO_REF необходимо указать директорию с предпоготовленным референсом
