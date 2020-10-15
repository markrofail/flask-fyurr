all: upbuild
upbuild: build up

up:
	docker-compose up

build:
	docker-compose build

down:
	docker-compose down

destroy:
	docker-compose down -v

test:
	docker-compose run --service-ports --rm python nosetests -sv
