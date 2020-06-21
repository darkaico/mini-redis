test:
	poetry run pytest

start:
	poetry run python mini_redis_server/server.py

seed:
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/x1' --header 'Content-Type: application/json' --data-raw '{"value": "Wolverine"}'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/x2' --header 'Content-Type: application/json' --data-raw '{"value": "Gambit"}'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/x3' --header 'Content-Type: application/json' --data-raw '{"value": "Quicksilver"}'

	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd?score=1&member=Wolverine'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd?score=1&member=Guepardo'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd?score=2&member=Gambit'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd?score=3&member=Quicksilver'

docker_remove:
	docker rm miniredisserver

docker_build: docker_remove
	docker build -t mini-redis-server .

docker_start:
	docker run -p 8080:8080 --name miniredisserver -d mini-redis-server