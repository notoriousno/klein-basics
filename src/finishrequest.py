from time import time
from klein import Klein
from twisted.internet import defer
from twisted.python import log


app = Klein()

@app.route('/onfinish')
def onfinish(request):

    def displayTime(null, start):
        """
        Display in the logs after the request is finished
        """
        now = time()
        log.msg('end - start time = {0}'.format(now-start))

    begin = time()
    request.notifyFinish().addCallback(displayTime, begin)
    return 'Start Time: {0}'.format(begin)


if __name__ == '__main__':
    app.run('localhost', 9000)
