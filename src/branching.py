"""
How to test using curl:

?> curl localhost:9000/branch/hello
?> curl localhost:9000/branch/blue/first
?> curl localhost:9000/branch/blue/second
?> curl localhost:9000/branch/blue/third
"""

from klein import Klein
from twisted.web.static import File

import blueprints


app = Klein()

@app.route('/branch', branch=True)
def branchOff(request):
    return blueprints.app.resource()    # get the Resource object from the Klein app in the blueprints module


if __name__ == '__main__':
    app.run(host='localhost', port=9000)
