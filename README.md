# Pod Reloader

TODO:

* Proper logging

## Example deployment

Kubernetes still does not have a formal sidecar pattern,
so the deployment is a bit verbose.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      initContainers:
      - name: reloader-init
        image: docker.io/morecontainers/reloader:latest
        env:
        - {name: RELOADER_INIT,      value: "1"}
        - {name: RELOADER_CONFIGMAP, value: prometheus}
        - {name: RELOADER_PATH,      value: /config}
        - {name: RELOADER_ENDPOINT,  value: "http://localhost:8428/-/reload"}
      containers:
      - name: prometheus
        image: victoriametrics/victoria-metrics:v1.56.0
        args: ["-promscrape.config","/config/prometheus.yml"]
        ports:
        - containerPort: 8428
        volumeMounts:
        - name: config-volume
          mountPath: /config
      - name: reloader
        image: docker.io/morecontainers/reloader:latest
        env:
        - {name: RELOADER_CONFIGMAP, value: prometheus}
        - {name: RELOADER_PATH,      value: /config}
        - {name: RELOADER_ENDPOINT,  value: "http://localhost:8428/-/reload"}
        volumeMounts:
        - name: config-volume
          mountPath: /config
      volumes:
      - name: config-volume
        emptyDir: {}
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus
data:
  prometheus.yml: |
    global:
      scrape_interval: 5s
    scrape_configs:
     - job_name: haproxy
       static_configs:
       - targets: ['haproxy:8428']
```

NOTE:  You need to setup the service account to have view permissions on the configmap,
as described in RBAC section below.

## Prebuilt containers

Prebuilt docker containers available at Docker Hub:

https://hub.docker.com/repository/docker/morecontainers/reloader

## RBAC

https://kubernetes.io/docs/reference/access-authn-authz/rbac/#service-account-permissions

```sh
kubectl create rolebinding serviceaccounts-view \
  --clusterrole=view \
  --group=system:serviceaccounts:default \
  --namespace=default
```

## Application support

TODO: Describe the integration paths in some more detail.

* [Prometheus](https://github.com/prometheus/prometheus/issues/1572)
* [NGINX](https://www.nginx.com/resources/wiki/start/topics/tutorials/commandline/)
* [HAProxy](https://www.haproxy.com/blog/haproxy-process-management/)

## Authors

* [Henrik Holst](mailto:hholst80@gmail.com)
