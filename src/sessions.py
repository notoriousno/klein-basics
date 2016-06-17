from klein import Klein
from twisted.python.components import registerAdapter
from twisted.web.server import Session
from zope.interface import Interface, Attribute, implementer


class ICounter(Interface):
    value = Attribute("An int value which counts up")

@implementer(ICounter)
class Counter(object):
    def __init__(self, session):
        self.value = 0

registerAdapter(Counter, Session, ICounter)


app = Klein()

@app.route('/')
def GET(request):
    session = request.getSession()
    counter = ICounter(session)
    counter.value += 1
    return "Visit #%d for you!" % (counter.value)

app.run('localhost', 9000)
