

to build the application have docker installed and run the following command in the app base directory

docker build -t morty-api .

to run the application after you build the image do the following command 

docker run -d -p 80:80 morty-api

note that the application expose the api on port 80


rest api endpoints 

Get /healthcheck

should return the following

healthy

Get /api/characters

to get all the characters that are human alive and thier origin is from any earth 

return object is json objet with 
name,location,image of each character that have the conditions above

example 

{
  {
    "image": "https://rickandmortyapi.com/api/character/avatar/786.jpeg",
    "location": "Earth (Replacement Dimension)",
    "name": "Birdperson & Tammy's Child"
  }
}




deployment to k8s 
since i deply localy with minikube after building the docker image 
the image needs to be loaded to minikube so 
first run 

minikube start 

so minikube runs 
then run 

minikube image load morty-api:latest

to load the image 

can verify that the image exist with 

minikube ssh -- docker images

to deploy run the following command 

kubectl apply -f Deployment.yaml

to allow access from outside the cluster run 

kubectl apply -f Service.yaml

to get the connection port run 

kubectl get svc morty-api-service

and to get the ip you need to acces run 

minikube ip

so the curl request should look like 

curl <minikubeIp>:NodePort/healthcheck 


for ingress with minikube need to ebable the addon 

minikube addons enable ingress


to deploy the ingress run 

kubectl apply -f Ingress.yaml



to create the helm use 

helm create morty-api

should do 

helm lint ./morty-api 

to make sure everything is correct 

then can do a dry run with 

helm install morty-api ./morty-api --dry-run

then can run

helm install morty-api ./morty-api


the github workflow action steps and what do each of them do 

step:
Checkout code
clone the github repo to the machien 

step
helm/kind-action@v1.8.0

install kind(which is the kube in docker) and helm 

step
Build Docker image

uses the docker file to create the docker image

step
Load image into KinD

loads the created docker image to the kind cluster

step
Deploy Helm chart

deploy the app using helm with the passed configs 

step
Wait for app to be ready

runing a command to make sure the next step only runs after the app is up and runing 


