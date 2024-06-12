# flask-redis-cluster-app

 git clone https://github.com/mfkhan267/flask-redis-cluster-app.git
 
 cd flask-redis-cluster-app/k8s/
 
kubectl create namespace statefulns
 
kubectl --namespace statefulns apply -f statefulset.yaml
 
kubectl --namespace statefulns get svc
 
kubectl --namespace statefulns get pods 

# Wait for for all the 5 redis-cluster Pods to come up
 
IPs=$(kubectl --namespace statefulns get pods -l app=redis-cluster -o jsonpath='{.items[*].status.podIP}' | awk '{for(i=1;i<=NF;i++) printf $i":6379 "; print ""}')
 
kubectl --namespace statefulns exec -it redis-cluster-0  -- /bin/sh -c "redis-cli -h 127.0.0.1 -p 6379 --cluster create ${IPs}"

# Type YES to Accept
 
kubectl --namespace statefulns exec -it redis-cluster-0  -- /bin/sh -c "redis-cli -h 127.0.0.1 -p 6379 cluster info"
 
kubectl --namespace statefulns apply -f example-app.yaml
 
kubectl --namespace statefulns get pods

kubectl --namespace statefulns get svc
 
kubectl port-forward --address 0.0.0.0 svc/hit-counter-lb 8080:80 --namespace statefulns

