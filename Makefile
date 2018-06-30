pylint:
	flake8

build: Dockerfile
	docker build -t ${DOCKERUSER}/hockey_squad:latest -f Dockerfile .

buildLocal: Dockerfile
	docker build -t hockey_squad:latest -f Dockerfile .

buildTest: Dockerfile.test
	docker build -t test_hockey_squad:latest -f Dockerfile.test .

push:
	docker push ${DOCKERUSER}/hockey_squad:latest

pull:
	docker pull ${DOCKERUSER}/hockey_squad:latest

publish: build push

test: buildTest
	docker run test_hockey_squad:latest
