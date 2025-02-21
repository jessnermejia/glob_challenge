REGISTRY=gcr.io/interno-lumen-analitica
IMAGE_LOCAL_NAME = glob_challenge:latest
IMAGE_GCP_NAME = gcp_glob_challenge:latest
CHALLENGE_IMAGE = ${REGISTRY}/${IMAGE_GCP_NAME}
SERVICE_NAME = gcp-glob-challenge

## This Makefile save the commands and allow us build, push and deploy new version of backend
## using this kind of files we can make changes when ever we want and deploy fastly.

.PHONY: *

# Building a new image of app
build_local_app:
	@echo "Building image ${IMAGE_LOCAL_NAME} for local"
	docker buildx build \
    -t ${IMAGE_LOCAL_NAME}:latest \
	-f Dockerfile.back .
	@echo "${IMAGE_LOCAL_NAME} for local was built"

# Running a new image of app
run_local_app: 
	@echo "Running the app ${IMAGE_LOCAL_NAME}"
	docker run --name glob-challenge \
	-ti \
    --rm -p 8080:8080 \
    ${IMAGE_LOCAL_NAME}:latest

build_gcp_app:
	@echo "Building image ${IMAGE_GCP_NAME}"
	docker buildx build \
	--platform linux/amd64 \
	-t ${IMAGE_GCP_NAME} \
	-f Dockerfile.back .
	@echo "${IMAGE_GCP_NAME} was built"

push_gcp_app:
	@echo "tagging ${IMAGE_GCP_NAME} as glob-challenge latest image (${CHALLENGE_IMAGE})"
	docker tag ${IMAGE_GCP_NAME} ${CHALLENGE_IMAGE} 
	@echo "pushing image to Google Cloud Container Registry"
	docker push ${CHALLENGE_IMAGE}
	@echo "Pushed ${IMAGE_GCP_NAME} into ${CHALLENGE_IMAGE}"

build_and_push_gcp: build_gcp_app push_gcp_app

configure_docker:
	gcloud auth configure-docker

deploy_app:
	gcloud run deploy ${SERVICE_NAME} --image ${CHALLENGE_IMAGE}

