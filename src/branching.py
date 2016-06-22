from klein import Klein
from twisted.web.static import File

import blueprints


app = Klein()


@app.route('/branch', branch=True)
def branchOff(request):
    return blueprints.app.resource()

@app.route('/static', branch=True)
def static(request):
    return File('/path/to/static/files')


app.run(host='localhost', port=9000)
