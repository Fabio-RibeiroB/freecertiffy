clean:  
	rm -f myenv-dist-env-configmap.yaml mongo-persistentvolumeclaim.yaml freecertiffylan-networkpolicy.yaml flaskapp-service.yaml mongo-service.yaml redis-service.yaml initialise-user-service.yaml flaskapp-deployment.yaml mongo-deployment.yaml redis-deployment.yaml initialise-user-deployment.yaml


apply:
	#kompose  convert -f ../docker-compose-dist.yaml
	kubectl apply -f myenv-dist-env-configmap.yaml,mongo-persistentvolumeclaim.yaml,freecertiffylan-networkpolicy.yaml,flaskapp-service.yaml,mongo-service.yaml,redis-service.yaml,initialise-user-service.yaml,flaskapp-deployment.yaml,mongo-deployment.yaml,redis-deployment.yaml,initialise-user-deployment.yaml
	#minikube service flaskapp
delete:
	kubectl delete -f myenv-dist-env-configmap.yaml,mongo-persistentvolumeclaim.yaml,freecertiffylan-networkpolicy.yaml,flaskapp-service.yaml,mongo-service.yaml,redis-service.yaml,initialise-user-service.yaml,flaskapp-deployment.yaml,mongo-deployment.yaml,redis-deployment.yaml,initialise-user-deployment.yaml
