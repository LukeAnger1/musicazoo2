from . import endpoints
import os
from werkzeug import routing, exceptions
from werkzeug.wrappers import Response
from werkzeug.wsgi import wrap_file
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware

not_found_app = exceptions.NotFound()

url_map = routing.Map([
    routing.Rule('/', endpoint='index.html'),
])

static_path = endpoints.settings.static_path

def application(environ, start_response):
    adapter = url_map.bind_to_environ(environ)
    try: 
        endpoint, values = adapter.match()
    except:
        return not_found_app(environ, start_response)
    else:
        file_path = os.path.join(static_path, endpoint)
        f = open(file_path)
        response = Response(wrap_file(environ, f), mimetype="text/html")
        return response(environ, start_response)


application = SharedDataMiddleware(application, dict([endpoints.static_endpoint]))
application = DispatcherMiddleware(application, endpoints.wsgi_endpoints)
