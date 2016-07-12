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

It's an inevitable fact that your application will grow and it may prove useful to import Klein objects from another module.  Without going into great detail, Klein can handle nested routes by passing in ``branch=True`` in the ``route`` decorator, which allows then additional endpoints can be exposed.  The route function should return Twisted a `Resource <http://twistedmatrix.com/documents/current/api/twisted.web.resource.Resource.html>`_ object, which contain endpoints of their own.  The actual implementation is much easier and less intimidating so please read on!


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

   import blueprints    # this module holds the other Klein app

   app = Klein()

   @app.route('/branch', branch=True)
   def branchOff(request):
       return blueprints.app.resource()		# get the Resource object

   @app.route('/branch/2/', branch=True)
   def branchAgain(request):
       return blueprints.app.resource()     # get the Resource object

For those who are familiar, this is similar to Flask and their concept of ``Blueprints``.  In my personal opinion, I favor Klein's approach as it contains less obscure function calls.


Final Examples
--------------

* `static.py <https://github.com/notoriousno/klein-basics/blob/intro/src/static.py>`_
* `blueprints.py <https://github.com/notoriousno/klein-basics/blob/intro/src/blueprints.py>`_
* `branching.py <https://github.com/notoriousno/klein-basics/blob/intro/src/branching.py>`_


References
----------

* `How to Use Resources <http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html#web-howto-using-twistedweb-resources>`_
* `Resource API <http://twistedmatrix.com/documents/current/api/twisted.web.resource.Resource.html>`_
