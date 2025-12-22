import werkzeug
import json
import socket

def wsgi_control(addr,port,timeout=10):

    def query(inp):
        print(f"[WSGI->Service] Connecting to {addr}:{port}")
        print(f"[WSGI->Service] Sending data: {json.dumps(inp)}")
        data=json.dumps(inp)
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((addr,port))
            print(f"[WSGI->Service] Connection established to {addr}:{port}")
        except Exception as e:
            print(f"[WSGI->Service] ERROR: Failed to connect to {addr}:{port} - {e}")
            raise
        s.sendall((data+'\n').encode('utf-8'))
        result=b''
        while True:
            result+=s.recv(4096)
            if b'\n' in result:
                result=result[0:result.find(b'\n')].decode('utf-8')
                break
        s.close()
        print(f"[WSGI<-Service] Received response from {addr}:{port}: {result}")
        return json.loads(result)

    @werkzeug.Request.application
    def wsgi(request):
        mime_type = request.headers.get('content-type').partition(';')[0]
        if mime_type in {'text/json', 'application/json'}:
            inp=json.loads(request.data)
            print(f"[WSGI] Received JSON request on /{addr}:{port} endpoint")
            try:
                outp=query(inp)
            except Exception as e:
                print(f"[WSGI] ERROR during query: {e}")
                return werkzeug.exceptions.InternalServerError(e)
            return werkzeug.Response(json.dumps(outp),content_type='text/json')
        return werkzeug.Response('Endpoint only accepts JSON.')
    return wsgi

def wsgi_settings_json(settings_dict):
    settings_json = json.dumps(settings_dict)
    @werkzeug.Request.application
    def wsgi(request):
        return werkzeug.Response(settings_json, content_type='text/json')
    return wsgi
