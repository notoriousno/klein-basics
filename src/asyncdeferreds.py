from hashlib import md5
from io import BytesIO
from time import sleep

from klein import Klein
from twisted.web.client import getPage
from twisted.internet import defer, threads, reactor


app = Klein()
D = defer.Deferred()

#---------- Routes ----------#

with app.subroute('/async') as sub:

    @sub.route('/simple')
    def simple(request):
        """
        Create a callback chain that will underline and italicise some text.
        """
        global D
        D = defer.Deferred()
        D.addCallback(addTag, 'i')  # italics
        D.addCallback(addTag, 'u')  # underline
        return D

    @sub.route('/simple/fire')
    def startSimpleChain(request):
        """
        Start the callback chain, if it hasn't started already.
        """
        global D
        try:
            D.callback('This is a simple callback...FIRE!')     # start the callback chain
        except defer.AlreadyCalledError:
            return 'The callback has already been fired or not set! Go back to <a href="/async/simple" target="new">/async/simple</a> and initiate the Deferred.'
        return 'Look at the <a href="/simple">/simple</a> request tab.'

    @sub.route('/error')
    def asyncError(request):
        """
        Non-blocking errors
        """

        def raiseError():
            int('hello')        # this will cause an error

        def errorCallback(failure, request):
            """
            Return a message and the error.

            :param failure: Traceback info
            """
            request.setResponseCode(400)
            return 'Uh oh spaghetti-Os!<br><br>ERROR: {0}'.format(failure)


        d = defer.maybeDeferred(raiseError)
        err = d.addErrback(errorCallback, request)      # returns a deferred so you can chain callbacks to it
        err.addCallback(addTag, 'strong')               # make the error msg bold
        return d

    @sub.route('/coro')
    @defer.inlineCallbacks
    def coro(request):
        """
        A coroutine like function.
        """
        text = 'This is a coroutine-like function!'
        result = yield addTag(text, 'i')
        result = yield addTag(result, 'strong')
        result = yield addTag(result, 'body')
        result = yield addTag(result, 'html')
        # defer.returnValue(result)   # Python 2.x
        return result               # Python 3.x

    @sub.route('/phish/<url>')
    def phish(request, url):
        """
        Get the HTML from a website and generate a MD5 hash using deferreds
        and inlineCallbacks (similar to coroutines).

        :param url: The root name of a website. Ex: google, yahoo, twistedmatrix
        """

        @defer.inlineCallbacks
        def somethingAwesome(result):
            """
            You can do something awesome here, like scrape a website!
            We're just going to generate a hash though.

            :param result: In this case, the getPage func returns a byte representation of the website source code.
            """
            strio = BytesIO(result)
            md5hash = md5()
            for chunk in iter(lambda: strio.read(1024), b''):
                yield md5hash.update(chunk)         # use yield so that it doesn't block

            # defer.returnValue(md5hash.hexdigest())  # Python 2.X
            return md5hash.hexdigest()              # Python 3.x

        bytesUrl = '.'.join(['http://www', url, 'com']).encode('utf-8')
        d = getPage(bytesUrl)               # get the source from a website, return a deferred
        d.addCallback(somethingAwesome)     # do something asynchronously
        d.addCallback(addTag, 'h1')         # enclose in a header tag...
        d.addCallback(addTag, 'body')       # enclose in a body...
        d.addCallback(addTag, 'html')       # finally enclose in html tags
        return d

    @sub.route('/sleep/<int:n>')
    def sleepTask(request, n):
        """
        A silly blocking task that will execute in a thread and return.

        :param n: Number of seconds to sleep
        """
        
        def blockingTask(n):
            """
            A trivial function that will block or n seconds.
            """
            sleep(n)
            return 'Slept for %d seconds' % n

        d = threads.deferToThread(blockingTask, n)
        d.addCallback(addTag, 'h1')
        return d


#---------- Functions ----------#

def addTag(text, tag):
    """
    Enclose text in an HTML tag.

    :param text: String
    :param tag: HTML tag such as "body", "html", "strong", etc.
    :return: String
    """
    return '<{0}>{1}</{0}>'.format(tag, text)


if __name__ == '__main__':
    app.run('localhost', 8000)
