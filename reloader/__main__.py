from reloader import *

print("Reloader settings:")
print("NAMESPACE: %s" % NAMESPACE)
if CONFIGMAP:
    print("CONFIGMAP: %s" % CONFIGMAP)
if SECRET:
    print("SECRET:    %s" % SECRET)
if ENDPOINT:
    print("ENDPOINT:  %s" % ENDPOINT)
elif PIDFILE:
    print("PIDFILE:   %s" % PIDFILE)
    print("SIGNAL:    %i" % SIGNAL)
elif TOUCHFILE:
    print("TOUCHFILE: %s" % TOUCHFILE)
stream = watch()
if not INIT:
    next(stream)
for e_type, e_object in stream:
    if SECRET and PATH:
        update_base64(e_object)
    elif CONFIGMAP and PATH:
        update(e_object)
    if INIT:
        break
    reload()
