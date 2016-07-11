Expanding Your App
==================

Subroutes
---------

Let's start with a simple way to combine routes that share a common endpoint.  For example, lets say we need routes for ``/base/first``, ``/base/second``, ``/base/third``.  The crude way of achieving this would be to explicitly write out each route with the ``/base`` route, like so:

.. code-block:: python

   app.route('/base/first')
   def first(request):
      # ...

   app.route('/base/second')
   def second(request):
      # ...

   app.route('/base/third')
   def third(request):
      # ...

This is valid code, but there's simpler syntax that can help reduce some common human errors like misspellings.  The ``subroute`` function helps make the code more legible as well as simpler.

.. code-block:: python

   with app.subroute('/base') as sub:

        @sub.route('/first')
        def first(request):
            return 'first'

        @sub.route('/second')
        def second(request):
            return 'second'

        @sub.route('/third')
        def third(request):
            return 'third'

Expanding
---------

It's an inevitable fact that your application will grow and the need to import Klein objects from other module will become necessary.  Without going into great detail, Klein (or Twisted) handles rendering of responses using Twisted `Resource <http://twistedmatrix.com/documents/current/api/twisted.web.resource.Resource.html>`_ objects and behave very similar to graphs or trees.  In fact, if we continue with the tree concept, the Resource is either the "last render point" (aka. ``leaf``) or a point which splits off into other Resources (aka. a ``branch``). Find out a bit more about Twisted `Resources <http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html#web-howto-using-twistedweb-resources>`_.  If a route function passes ``branch=True`` to the ``route``, then the function can return a Twisted `Resource <http://twistedmatrix.com/documents/current/api/twisted.web.resource.Resource.html>`_.


Static Files
------------

Static files are a perfect way to illustrate how branching works.  The following example will serve the files at a specific local directory.

.. code-block:: python

   from twisted.web.static import File

   @app.route('/static', branch=True)
   def static(request):
       return File('/path/to/static/files')

Notice the ``branch`` keyword in the route decorator.  The ``branch`` syntax simply means there are other ``Resources`` (aptly labeled leaves) under this route.  ``File`` objects return a ``Resource`` object for every file in the path.


Distributed Modules
-------------------

Imagine the application you've built has grown large enough that placing all the routes in a single file has become too unwieldy.  Expanding on the ``branch`` concept, we can generate the ``Resource`` file from other Klein objects, making it possible to simply import Klein objects.

*blueprints.py*

.. code-block:: python

   app = Klein()

   @app.route('/hello')
   def index(request):
       return 'Hello from the subroutes example'

   with app.subroute('/blue') as sub:
       @sub.route('/first')
       def first(request):
           return 'first'

       @sub.route('/second')
       def second(request):
           return 'second'

       @sub.route('/third')
       def third(request):
           return 'third'

Now lets use this in another ``klein`` application.

.. code-block:: python

   from klein import Klein
   from twisted.web.static import File

   import blueprints

   app = Klein()

   @app.route('/branch', branch=True)
   def branchOff(request):
       return blueprints.app.resource()		# get the Resource object

   @app.route('/branch/2/', branch=True)
   def branchAgain(request):
       return blueprints.app.resource()

Final Example
-------------

*blueprints.py*

.. code-block:: python

   from klein import Klein

   app = Klein()

   @app.route('/hello')
   def index(request):
       return 'Hello from the subroutes example'

   with app.subroute('/blue') as sub:

       @sub.route('/first')
       def first(request):
          return 'first'

       @sub.route('/second')
       def second(request):
          return 'second'

       @sub.route('/third')
       def third(request):
          return 'third'

*branching.py*

.. code-block:: python

   from klein import Klein
   from twisted.web.static import File

   import blueprints

   app = Klein()

   @app.route('/static', branch=True)
   def staticFiles(request):
       return File('/path/to/static/files')

   @app.route('/branch', branch=True)
   def branchOff(request):
       return blueprints.app.resource()

   @app.route('/branch/2/', branch=True)
   def branchAgain(request):
       return blueprints.app.resource()


   app.run(host='localhost', port=9000)
