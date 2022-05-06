import os
import signal


def _namespace():
    default_namespace = "default"
    if os.path.isfile("/run/secrets/kubernetes.io/serviceaccount/token"):
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            default_namespace = f.read()
    namespace = os.environ.get("RELOADER_NAMESPACE", default_namespace)
    return namespace


INIT = os.environ.get("RELOADER_INIT", False)
NAMESPACE = _namespace()
CONFIGMAP = os.environ.get("RELOADER_CONFIGMAP")
SECRET = os.environ.get("RELOADER_SECRET")
PATH = os.environ["RELOADER_PATH"]
ENDPOINT = os.environ.get("RELOADER_ENDPOINT")
PID = os.environ.get("RELOADER_PIDFILE")
PIDFILE = os.environ.get("RELOADER_PIDFILE")
TOUCHFILE = os.environ.get("RELOADER_TOUCHFILE")
SIGNAL = signal.Signals[os.environ.get("RELOADER_SIGNAL", "SIGUSR2")].value

assert bool(CONFIGMAP) ^ bool(SECRET)
