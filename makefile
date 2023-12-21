build:
	docker build --network=host -t hm-dj-image:v1.0.0 .


run:
	docker run -d --restart always --name hol4-mund0-django -p 8000:8080 -v `pwd`:/`pwd` -w `pwd` -it hm-dj-image:v1.0.0


restart:
	docker stop hol4-mund0-django	


stop:
	docker stop hol4-mund0-django


delete-container:
	docker rm hol4-mund0-django


delete-image:
	docker rmi hm-dj-image:v1.0.0


logs:
	docker logs hol4-mund0-django -f

stats:
	docker stats hol4-mund0-django