from klein import Klein
from twisted.python.components import registerAdapter
from twisted.web.server import Session
from zope.interface import Interface, Attribute, implementer


#---------- Interface and Classes ----------#
class ICounter(Interface):
    """
    An interface or template class which documents parameters a Counter 
    class should have.
    """
    count = Attribute("An int value which counts up")
    user = Attribute("A username associated with this session")

@implementer(ICounter)
class Counter(object):
    """
    Keeps track user visits
    """

    def __init__(self, session):
        self.count = 0
        self.user = None

registerAdapter(Counter, Session, ICounter)     # don't worry about what this does, just do it!


#---------- Klein Routes ----------#
app = Klein()

@app.route('/session')
def GET(request):
    """
    Retrieves the session for the request, bumps up the counter, and sets
    a user if provided in the header.
    """
    session = request.getSession()
    counter = ICounter(session)
    counter.count += 1
    if not counter.user:
        counter.user = request.getHeader('UserName')

    return "Visit #{0} for {1}!".format(counter.count, counter.user)


if __name__ == '__main__':
    app.run('localhost', 9000)

