# agent-cloud
gcloud init

gcloud auth configure-docker us-central1-docker.pkg.dev

podman build -t us-central1-docker.pkg.dev/k8s-taller-4/docker-images/agent-cloud:latest .     

podman push us-central1-docker.pkg.dev/k8s-taller-4/docker-images/agent-cloud:latest

docker build -t us-central1-docker.pkg.dev/k8s-taller-4/docker-images/agent-cloud:latest .     

docker push us-central1-docker.pkg.dev/k8s-taller-4/docker-images/agent-cloud:latest

