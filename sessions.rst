Sessions: A more in depth look
==============================


Sessions can store objects around as long as the session exists.  The following demonstrates how to store the number of times a user visits a particular endpoint.

.. code-block:: python

   from klein import Klein
   from twisted.python.components import registerAdapter
   from twisted.web.server import Session
   from zope.interface import Interface, Attribute, implementer

   #---------- Session Interface ----------#
   class ICounter(Interface):
       count = Attribute("An int value which counts up")
       user = Attribute("A username associated with this session")

   @implementer(ICounter)
   class Counter(object):
       def __init__(self, session):
           self.count = 0 
           self.user = None

   registerAdapter(Counter, Session, ICounter)

   #---------- Klein ----------#
   app = Klein()

   @app.route('/session')
   def storedSession(request):
       session = request.getSession()
       counter = ICounter(session)
       counter.count += 1
       if not counter.user:
           counter.user = request.getHeader('UserName')

       return "Visit #{0} for {1}!".format(counter.count, counter.user)

   app.run('localhost', 9000)

Don't worry if you're confused, just put on your "conceptualization" cap on and allow me to explain.

.. code-block:: bash

   curl -v -H "UserName: GnomeMan" -c _cookie.jar -b _cookie.jar localhost:9000/session
