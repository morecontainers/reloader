import json
import logging
import os
import signal
import binascii
import requests
from .config import (
    CONFIGMAP,
    ENDPOINT,
    INIT,
    NAMESPACE,
    PATH,
    PIDFILE,
    SECRET,
    SIGNAL,
    TOUCHFILE,
)


def watch():
    e_type = "configmaps" if CONFIGMAP else "secrets"
    e_name = CONFIGMAP or SECRET
    if os.path.isfile("/run/secrets/kubernetes.io/serviceaccount/token"):
        k8s_host = os.environ["KUBERNETES_SERVICE_HOST"]
        k8s_port = os.environ["KUBERNETES_SERVICE_PORT_HTTPS"]
        url = "https://%s:%s/api/v1/watch/namespaces/%s/%s/%s" % (
            k8s_host,
            k8s_port,
            NAMESPACE,
            e_type,
            e_name,
        )
        with open("/var/run/secrets/kubernetes.io/serviceaccount/token", "rb") as f:
            token = f.read()
        headers = {"Authorization": "Bearer %s" % token.decode()}
        cacert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
        r = requests.get(url, stream=True, headers=headers, verify=cacert)
    else:
        url = "http://localhost:8001/api/v1/watch/namespaces/%s/%s/%s" % (
            NAMESPACE,
            e_type,
            e_name,
        )
        r = requests.get(url, stream=True)
    r.raise_for_status()
    print("Watching %s" % url)
    for line in r.iter_lines():
        e_type, e_object = json.loads(line).values()
        yield (e_type, e_object)


def update_base64(config):
    for key, data in config["data"].items():
        path = os.path.join(PATH, key)
        print("Updating config %s" % path)
        data = binascii.a2b_base64(data)
        with open(path, "wb") as f:
            f.write(data)


def update(config):
    for key, data in config["data"].items():
        path = os.path.join(PATH, key)
        print("Updating config %s" % path)
        with open(path, "wb") as f:
            f.write(data.encode())


def reload():
    if ENDPOINT:
        try:
            requests.post(ENDPOINT)
        except:
            logging.exception("Reload endpoint failure:")
    elif PIDFILE:
        try:
            with open(PIDFILE, "rb") as f:
                pid = int(f.read())
            os.kill(pid, SIGNAL)
        except:
            logging.exception("Reload signalling failure:")
    elif TOUCHFILE:
        try:
            with open(TOUCHFILE, "wb"):
                pass
        except:
            logging.exception("Reload touch file failure:")
    else:
        pass
