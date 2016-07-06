Non-blocking Routes
===================

Do you like ``expressjs``, but don't want to switch to Node.js?  Want non-blocking execution in Python?  Then look no further!  Asynchronous execution is the very essence of what makes Klein a contender in todays web framework landscape.  It's also the most difficult concept to grasp since most Pythonistas are not accustomed to asynchronous programming.  Hopefully with the addition ``asyncio`` to Python's standard library, this will change.  Klein is built atop Twisted and developers can expose ``Deferred`` objects for asynchronous behavior.  A very brief overview will be given on Twisted ``Deferred``, afterwards aspiring developers are encouraged to read the Twisted documents on the subject (provided in the links near the bottom).


Deferred Overview
-----------------

* think of it in reverse order!

To demonstrate how ``Deferred`` objects work, we will create a chain of callback functions that execute after a result is available.  Don't worry if this confuses you right now, the code will clear things up.

.. code-block:: python

   from __future__ import print_function
   from twisted.internet import defer

   def addition(result, *numbers, **kw):
       """
       This is the callback function
       """
       return result + sum(numbers)

   def errorHasHappened(failure, msg):
       """
       This is the error-back function
       """
       print(msg)

   # Create deferred obj and callback chain
   d = defer.Deferred()
   d.addCallback(addition, 1, 2, 3, 4)
   d.addErrback(print, 'This is an error!')
   d.addBoth(print)         # addBoth states the function is both called as a callback and errback

   d.callback(100)          # start the callback chain

First, callback and error-back functions are established (``adition()`` and ``errorHasHappend()`` in this case).  These callbacks are "registered" by the ``addCallback()`` and ``addErrback()`` functions.  Notice the callback functions (``addition()`` and ``errorHasHappend()``) take an argument ``result`` and ``failure``, these are the results returned from the previous function.  Upon successful execution and returning of a valid result of 100 (ie. ``d.callback(100)``), the callback chain starts.  First the ``addition`` function executes and adds ``1, 2, 3, 4`` to ``100`` then the final result is printed (via ``d.addBoth(print)``.  To execute the errorback chain, a value which would raise an error in the ``addition()`` function could be used, such as ``d.callback("one hundred")``.

Alternatively, if the result is available immediately, ``succeed()`` or ``failure()`` can be executed:

.. code-block:: python

   def addition(result, *numbers, **kw):
       return result + sum(numbers)

   def errorHasHappened(failure, msg):
       print(msg)

   d = defer.succeed(200).addCallback(addition, 10, 20).addCallback(print)
   defer.fail(Exception()).addErrback(errorHasHappened, 'Errback executed')

Now let's get back to the main web framework!


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


Error Callbacks
---------------

With standard Python exception handling, when an error is raised, specific code can be run in the ``exception`` section.  ``Deferred`` objects can be utilized like try/except blocks, in fact, the underlaying code actually uses this exception handling to launch error callbacks.  To execute a specific function when an error occurs, we have to add an error callback by using ``Deferred.addErrback()``.

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

With the advent of Tornado, many have grown to like coroutines as opposed to callbacks or promise approaches for web development.  Klein can leverage what are known as ``inlineCallbacks`` which work very similarly to coroutines.  With coroutines and ``inlineCallbacks``, you can "wait" or ``yield`` for a result without blocking your entire application.:

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
