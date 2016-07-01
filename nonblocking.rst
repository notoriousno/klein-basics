Non-blocking Routes
===================

Do you like ``expressjs``, but don't want to switch to Node.js?  Want non-blocking execution in Python?  Then look no further!  Non-blocking, otherwise known as asynchronous, execution is the very essence of what makes Klein a contender in todays web framework landscape.  It's also the most difficult concept to grasp since most Pythonistas are not accustomed to asynchronous programming.  This will hopefully change over time because Python has introduced ``asyncio``.  Since Klein is built atop Twisted, developers can expose ``Deferred`` objects, which are similar to Promises (from Node.js) and Futures (from Python's own ``asyncio``).  However, in this example, a very brief overview will be given on Twisted ``Deferred``, instead you're encouraged to read the Twisted documents on the subject (provided in the links near the bottom).


Deferred Overview
-----------------

* think of it in reverse order!

Create a ``Deferred`` object and attach functions (otherwise known as ``callbacks``) that will occur after a result has been returned.  Callbacks are appended to ``Deferred`` objects by way of ``addCallback()`` for when a successful result is returned or ``addErrback()`` for when an error has occurred.  The callback functions take the function name, followed by arguments and keyword arguments.  Then, when the result is available, the ``callback`` function is executed and the callback chain will be executed.  Don't worry if this doesn't make sense now, the code should clear it up.

.. code-block:: python

   from __future__ import print_function
   from twisted.internet import defer

   def addition(result, *numbers, **kw):
       return result + sum(numbers)

   def errorHasHappened(failure, msg):
       print(msg)

   # Create deferred obj and callback chain
   d = defer.Deferred()
   d.addCallback(addition, 1, 2, 3, 4)
   d.addErrback(print, 'This is an error!')
   d.addBoth(print)         # addBoth states the function is both called as a callback and errback

   d.callback(100)          # start the callback chain

First, callback and error-back functions are established (``adition()`` and ``errorHasHappend()`` in this case).  Then upon successful execution and returning of a valid result of 100 (ie. ``d.callback(100)``), the callback chain starts, ``1, 2, 3, 4`` are added to ``100`` then the final result is printed (via ``d.addBoth(print)``.  Alternative way to fire callbacks immediately.

.. code-block:: python

   def addition(result, *numbers, **kw):
       return result + sum(numbers)

   def errorHasHappened(failure, msg):
       print(msg)

   d = defer.succeed(200).addCallback(addition, 10, 20).addCallback(print)
   defer.fail(Exception()).addErrback(errorHasHappened, 'Errback executed')


Simple Deferred
---------------

Let's take a simple spin on deferreds.  Two endpoints will be created, one will create a callback chain and another will actually start the callback chain.  "What's a callback chain?"  I'm glad you asked!  In layman's terms, a callback chain is a sequence of events that that occur after an event occurs.  To do this using Twisted, we use what are known as ``Deferred``.  We first instantiate a ``Deferred`` and then append functions we want to execute after a value is returned.  Finally, when the value is ready, the callback chain is executed.  Hopefully the following example will help make sense of all this.

.. code-block:: python

    def addTag(text, tag):
        return '<{0}>{1}</{0}>'.format(tag, text)

    @app.route('/simple')
    def simple(request):
        global D
        D = defer.Deferred()
        D.addCallback(addTag, 'i')  # italics
        D.addCallback(addTag, 'u')  # underline
        return D

    @app.route('/simple/fire')
    def startSimpleChain(request):
        global D
        try:
            D.callback('This is a simple callback...FIRE!')     # start the callback chain
        except defer.AlreadyCalledError:
            return 'The callback has already been fired or not set! Go back to <a href="/async/simple" target="new">/async/simple</a> and initiate the Deferred.'
        return 'Look at the <a href="/simple">/simple</a> request tab.'    


The ``/simple`` route, initializes a global ``Deferred`` object and subsequent callbacks.  The ``/simple/fire`` route will start the callback chain and pass the text ``"This is a simple callback...FIRE!"``, but only if the ``Deferred`` hasn't been called already since ``Deferred`` objects can only be executed once.  So basically, when the ``Deferred`` is started (via ``D.callback('...')``) in the ``/simple/fire`` route, the text that's passed in will be passed along the callback chain which was created in the ``/simple`` route.  Let's test this out using ``curl`` or you can easily test this in a web browser:

.. code-block:: bash

    curl localhost:8000/simple &    # execute this in the background
    curl localhost:8000/simple/fire


Error Handling
--------------

With standard Python exception handling, when an error is raised, a specific code can be run in the ``exception`` section.  ``Deferred`` objects can be utilized like try/except blocks, in fact, the underlaying code actually uses this exception handling to launch error callbacks.  To execute a specific function when an error occurs, we have to add an error callback by using ``Deferred.addErrback()`` or ``Deferred.addCallbacks()`` (notice the 's' for plural, for callbacks and errorbacks).

.. code-block:: python

    @app.route('/error')
    def asyncError(request):

        def addTag(text, tag):
            return '<{0}>{1}</{0}>'.format(tag, text)

        def raiseError():
            int('hello')        # this will cause an error

        def errorCallback(failure, request):
            request.setResponseCode(400)
            return 'Uh oh spaghetti-Os!<br><br>ERROR: {0}'.format(failure)


        d = defer.maybeDeferred(raiseError)
        err = d.addErrback(errorCallback, request)      # returns a deferred so you can chain callbacks to it
        err.addCallback(addTag, 'strong')               # make the error msg bold
        return d

In this example, the function ``raiseError()`` results in a traceback and a triggers an error-back, which itself returns a ``Deferred``.  Since error-backs return ``Deferred``, you can chain callbacks to them.  In this case, the error message is displayed in bold.  Basically this is what's happening:

.. code-block:: python

    try:
        int('hello')
    except Exception as e:
        failure = errorCallback(e, request)
        return addTag(failure, 'strong')


"Coroutines"
------------

With the advent of Tornado, many have grown to like coroutines as opposed to callbacks or promise approaches.  Klein can leverage what are known as ``inlineCallbacks`` which work very similarly to coroutines.  With coroutines and ``inlineCallbacks``, you can "wait" or ``yield`` a result without blocking your entire application.:

.. code-block:: python

    def addTag(text, tag):
        return '<{0}>{1}</{0}>'.format(tag, text)

    @app.route('/coro')
    @defer.inlineCallbacks
    def coro(request):
        text = 'This is a coroutine-like function!'
        result = yield addTag(text, 'i')
        result = yield addTag(result, 'strong')
        result = yield addTag(result, 'body')
        result = yield addTag(result, 'html')
        # defer.returnValue(result)   # Python 2.x
        return result               # Python 3.x

Threads
-------

As a rule of thumb, developers should stay away from threads if possible.  With that being said, there are times where threads are necessary, such as executing code that can take an unpredictable amount of time.  Even then, it would be best to look for other alternative solutions, but let's move on.


Load Test
---------

Final Example
-------------
