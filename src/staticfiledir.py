import os

from klein import Klein
from twisted.web import server, static
from twisted.internet import reactor


app = Klein()
# staticFileDir = os.environ['HOME']
staticFileDir = './static'

@app.route('/static/', branch=True)
def staticFiles(request):
    return static.File(staticFileDir)

app.run('localhost', 9000)
