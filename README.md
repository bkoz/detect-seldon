# Boat detection using seldon-core s2i
Deploy a custom model using OpenShift s2i and Seldon. 

## Steps

### Create and start a new build.

```
oc new-build --strategy docker --docker-image registry.redhat.io/ubi8/python-38 --name detection -l app=detection --binary

oc start-build detection --from-dir=. --follow

```

Edit `detection-seldon-deploy.yaml` and change image url namespace to match the environment and deploy.

```
oc apply -f resources/detection-seldon-deploy.yaml

oc expose svc <svc-name>
```

To trigger a redeploy after a new build. This does not always work so the pod may have to be deleted.

```
oc patch deployment <deployment-name> -p "{\"spec\": {\"template\": {\"metadata\": { \"labels\": {  \"redeploy\": \"$(date +%s)\"}}}}}"
```

Testing the service.

```
curl -X POST $(oc get route detection-redhat -o jsonpath='{.spec.host}')/api/v1.0/predictions -H 'Content-Type: application/json' -d '{ "data": { "ndarray": [[5.1, 3.5, 1.4, 0.2]] } }'

curl -X GET $(oc get route detection-redhat -o jsonpath='{.spec.host}')/prometheus
```

### Prometheus and Grafana configuration.

Create a Grafana dashboard.

Create a Prometheus data source.

Create a service monitor.

```
oc apply -f resources/seldon-service-monitor.yml
```

Deploy outside of OpenShift directly from a Python environment.

```
seldon-core-microservice detection REST --service-type MODEL

curl -X POST -H 'Content-Type: application/json' -d '{"data": { "ndarray": [[1,2,3,4]]}}' http://localhost:5000/api/v1.0/predictions
```
