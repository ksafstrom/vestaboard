IMAGE_NAME=app
IMAGE_TAG=latest
JFROG=''
PYPI_USR?='artifactory-username'
PYPI_PSW?='artifactory-api-token'

run-app:
	python launcher.py $(app) $(sandbox)

install-deps:
		@ pip install -r requirements.txt -i

freeze:
		pip freeze > requirements.txt

docker-purge:
		docker images purge

docker-build:
		@ docker build --build-arg=PYPI_USR="$(PYPI_USR)" --build-arg=PYPI_PSW="$(PYPI_PSW)" \
			-t $(IMAGE_NAME) -f Dockerfile .

docker-clean:
		docker images -a | grep "$(IMAGE_NAME)" | awk '{print $$3}' | xargs docker rmi -f

docker-tag: docker-build
		docker tag $(IMAGE_NAME) docker.jfrog.io/$(IMAGE_NAME):$(IMAGE_TAG)

docker-push: docker-tag
		docker push docker.jfrog.io/$(IMAGE_NAME):$(IMAGE_TAG)

docker-run-sh: docker-tag
		docker run -it --entrypoint "/bin/bash" $(IMAGE_NAME):$(IMAGE_TAG)

docker-run: docker-build
		docker run $(IMAGE_NAME):$(IMAGE_TAG)

docker-rm:
		@ # we add the redirect and the true to make sure this always succeeds even
		@ # when there isn't anything to delete
		docker rm $(IMAGE_NAME) 2> /dev/null; true

docker-compose: docker-rm docker-compose-down
		docker-compose run app
		$(MAKE) docker-compose-down

docker-compose-down:
		docker-compose down

format:
		black $(IMAGE_NAME)/ --line-length 120
		black launcher.py --line-length 120
