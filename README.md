[![Build Status](https://travis-ci.org/darkaico/mini-redis.svg?branch=master)](https://travis-ci.org/darkaico/mini-redis)
[![Coverage Status](https://coveralls.io/repos/github/darkaico/mini-redis/badge.svg?branch=master)](https://coveralls.io/github/darkaico/mini-redis?branch=master)


# Mini-Redis Implementation

Simple project of a mini REDIS implementation.

## Structure

This project is divided in 2 main apps and an utils module

### Mini Redis

We will find here our mini redis library which could be used as a library directly by using its singleton instance

```python
from mini_redis import MiniRedis

# Set a value using `x1` as key
MiniRedis.instance().set('x1', 'Wolverine')

# Get previous value
MiniRedis.instance().get('x1')
```

### Api

Simple HTTP server using flask.

[REST API](mini_redis_api.md)

### Utils

Simple utils to help about data parsing and singleton uses

## Requirements

- Python Version: 3.8+

**Required Libraries**

- [aiohttp](https://docs.aiohttp.org/en/stable/)

**Development Libraries**

- [pytest](https://docs.pytest.org/en/stable/)

## Usage

### Local Env

Im using [Poetry](https://python-poetry.org/) as a dependency management. So once you set your environment
to be python 3.8^ compatible you need to run

#### In case you dont have poetry installed

```shell
pip install poetry
```

#### Install dependencies

```shell
poetry install
```

### Docker

In case you are using docker there is a Dockerfile that will build the project image and will start the server.

#### Build the dockerfile

```
docker build .
```

#### Run the container

```
docker run <container id>
```

### Commands

In order simplify tasks I created a make file that have some useful commands

#### Run unit tests

```shell
make test
```

#### Start HTTP server

```shell
make start
```

#### Seed some data

```shell
make seed
```

#### Build docker image

```shell
make docker_build
```

#### Start docker image

```shell
make docker_start
```
