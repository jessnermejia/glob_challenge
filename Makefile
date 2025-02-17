IMAGE_NAME = glob_challenge

## This Makefile save the commands and allow us build, push and deploy new version of backend
## using this kind of files we can make changes when ever we want and deploy fastly.

.PHONY: *

# Building a new image of app
build_local_app:
	@echo "Building image ${IMAGE_NAME} for local"
	docker buildx build \
    -t ${IMAGE_NAME}:latest \
	-f Dockerfile.back .
	@echo "${IMAGE_NAME} for local was built"

# Running a new image of app
run_local_app: 
	@echo "Running the app ${IMAGE_NAME}"
	docker run --name glob-challenge \
	-ti \
    --rm -p 8080:8080 \
    ${IMAGE_NAME}:latest
