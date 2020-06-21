test:
	poetry run pytest

start:
	poetry run python mini_redis_server/server.py

seed:
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/x1' \
	--header 'Content-Type: text/plain' \
	--data-raw 'Wolverine'


	curl --location --request PUT 'http://0.0.0.0:8080/api/store/x2' \
	--header 'Content-Type: text/plain' \
	--data-raw 'Gambit'


	curl --location --request PUT 'http://0.0.0.0:8080/api/store/x3' \
	--header 'Content-Type: text/plain' \
	--data-raw 'Quicksilver'

	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd/1/Wolverine'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd/1/Guepardo'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd/2/Gambit'
	curl --location --request PUT 'http://0.0.0.0:8080/api/store/mutants/zadd/3/Quicksilver'
