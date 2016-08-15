from klein import Klein
from twisted.internet import defer, reactor


app = Klein()

@app.route('/interrupted')
def interruptRoute(request):
    d = defer.Deferred()
    d.addCallback(_delayedRender)
    reactor.callLater(5, d.callback, request)
    request.notifyFinish().addErrback(_responseFailed, d)
    return d

def _responseFailed(error, call):
    print('Cancelled!')
    call.cancel()

def _delayedRender(request):
    request.write('Sorry for the delay'.encode('utf-8'))


if __name__ == '__main__':
    app.run('localhost', 9000)
