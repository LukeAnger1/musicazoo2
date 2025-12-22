import shmooze.wsgi
import shmooze.settings
import werkzeug.serving

print("=" * 60)
print(f"[WSGI] Starting WSGI server on port {shmooze.settings.ports['wsgi']}")
print(f"[WSGI] Configured service endpoints:")
for service, port in shmooze.settings.ports.items():
    if service != "wsgi":
        print(f"  - /{service} -> localhost:{port}")
print("=" * 60)

werkzeug.serving.run_simple('',shmooze.settings.ports["wsgi"],shmooze.wsgi.application,use_reloader=False, use_debugger=False)
