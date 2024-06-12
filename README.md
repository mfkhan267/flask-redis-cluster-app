# flask-redis-cluster-app

 git clone https://github.com/mfkhan267/flask-redis-cluster-app.git
 
 cd flask-redis-cluster-app/k8s/
 
 kubectl create namespace example
 
 kubectl --namespace example apply -f statefulset.yaml
 
 kubectl --namespace example get svc
 
 kubectl --namespace example get pods
 
 kubectl --namespace example get pods ## Wait for for all the 5 redis-cluster Pods to come up
 
 IPs=$(kubectl --namespace example get pods -l app=redis-cluster -o jsonpath='{.items[*].status.podIP}' | awk '{for(i=1;i<=NF;i++) printf $i":6379 "; print ""}')
 
 kubectl --namespace example exec -it redis-cluster-0  -- /bin/sh -c "redis-cli -h 127.0.0.1 -p 6379 --cluster create ${IPs}"
 
 kubectl --namespace example exec -it redis-cluster-0  -- /bin/sh -c "redis-cli -h 127.0.0.1 -p 6379 cluster info"
 
 kubectl --namespace example apply -f example-app.yaml
 
 kubectl --namespace example get pods
 
 kubectl port-forward --address 0.0.0.0 svc/hit-counter-lb 8080:80 --namespace example

