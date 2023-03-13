# Running with kubernetes
## convert the docker-compose file  with kompose
On MacOS
```
    brew install kompose
    brew install minikube
    brew install kubernetes-cli
```
```
    minkube start
or
    minikube start --addons=dashboard --addons=metric-server --addons=ingress --addons=ingress-dns
```

## Convert your docker-compose file
```
 kompose convert -f ../docker-compose-dist.yaml
INFO Network freecertiffylan is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Network freecertiffylan is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Network freecertiffylan is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Network freecertiffylan is detected at Source, shall be converted to equivalent NetworkPolicy at Destination 
INFO Kubernetes file "flaskapp-service.yaml" created 
INFO Kubernetes file "initialise-user-service.yaml" created 
INFO Kubernetes file "mongo-service.yaml" created 
INFO Kubernetes file "redis-service.yaml" created 
INFO Kubernetes file "flaskapp-deployment.yaml" created 
INFO Kubernetes file "myenv-dist-env-configmap.yaml" created 
INFO Kubernetes file "freecertiffylan-networkpolicy.yaml" created 
INFO Kubernetes file "initialise-user-deployment.yaml" created 
INFO Kubernetes file "mongo-deployment.yaml" created 
INFO Kubernetes file "mongo-persistentvolumeclaim.yaml" created 
INFO Kubernetes file "redis-deployment.yaml" created 
```

## Apply the configmap (environment variables)
```
    kubectl apply -f myenv-dist-env-configmap.yaml
```
## Apply the volume
```
    kubectl apply -f  mongo-persistentvolumeclaim.yaml
```
## Apply the servicess
```
    kubectl apply -f flaskapp-service.yaml,mongo-service.yaml,redis-service.yaml,initialise-user-service.yaml 
service/flaskapp created
service/mongo created
service/redis created
service/initialise-user created
```

## Apply the deployments
```
% kubectl apply -f flaskapp-deployment.yaml,mongo-deployment.yaml,redis-deployment.yaml,initialise-user-deployment.yaml
deployment.apps/flaskapp created
deployment.apps/mongo created
deployment.apps/redis created
deployment.apps/initialise-user created
```

```
 % minikube kubectl get deployments        
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
flaskapp          0/1     1            0           3m49s
initialise-user   0/1     1            0           3m49s
mongo             0/1     1            0           3m49s
redis             1/1     1            1           3m49s
```

```
% kubectl get pods
NAME                               READY   STATUS                       RESTARTS   AGE
flaskapp-5759c974dc-92fdn          0/1     CreateContainerConfigError   0          4m6s
initialise-user-75c775c55c-58p46   0/1     CreateContainerConfigError   0          4m6s
mongo-64c55d6cf5-l7567             0/1     Pending                      0          4m6s
redis-f758d554b-n4zzh              1/1     Running                      0          4m6s
```

```
kubectl get pods -o wide
NAME                               READY   STATUS                       RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
flaskapp-5759c974dc-92fdn          0/1     CreateContainerConfigError   0          5m51s   10.244.0.3   minikube   <none>           <none>
initialise-user-75c775c55c-58p46   0/1     CreateContainerConfigError   0          5m51s   10.244.0.5   minikube   <none>           <none>
mongo-64c55d6cf5-l7567             0/1     Pending                      0          5m51s   <none>       <none>     <none>           <none>
redis-f758d554b-n4zzh              1/1     Running                      0          5m51s   10.244.0.4   minikube   <none>           <none>
```

```
kubectl get services -A
NAMESPACE     NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
default       flaskapp          ClusterIP   10.107.168.88   <none>        90/TCP                   9m20s
default       initialise-user   ClusterIP   10.96.30.18     <none>        8000/TCP                 9m19s
default       kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP                  26m
default       mongo             ClusterIP   10.102.145.71   <none>        27017/TCP                9m20s
default       redis             ClusterIP   10.98.174.147   <none>        6379/TCP                 9m20s
kube-system   kube-dns          ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   26m
```

Was fully expecting it to be accessible on port 90 here but this didn't happen.
And the volume is not peristent

## Connect to the app using minikube tunnel
```
    minikube service flaskapp 
```
## Using as fewcommands as possible:
Apply
```
	kompose  convert -f ../docker-compose-dist.yaml
	kubectl apply -f myenv-dist-env-configmap.yaml,mongo-persistentvolumeclaim.yaml,freecertiffylan-networkpolicy.yaml,flaskapp-service.yaml,mongo-service.yaml,redis-service.yaml,initialise-user-service.yaml,flaskapp-deployment.yaml,mongo-deployment.yaml,redis-deployment.yaml,initialise-user-deployment.yaml
	minikube service flaskapp
```
Delete
```
	kubectl delete -f myenv-dist-env-configmap.yaml,mongo-persistentvolumeclaim.yaml,freecertiffylan-networkpolicy.yaml,flaskapp-service.yaml,mongo-service.yaml,redis-service.yaml,initialise-user-service.yaml,flaskapp-deployment.yaml,mongo-deployment.yaml,redis-deployment.yaml,initialise-user-deployment.yaml
```
