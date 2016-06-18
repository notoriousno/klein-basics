from time import sleep

from klein import Klein
from twisted.web.client import getPage
from twisted.internet import defer, threads, reactor


app = Klein()

with app.subroute('/tasks') as subroute:

    @subroute.route('/phishing/<url>')
    def phishAttack(request, url):
        bytesUrl = '.'.join(['http://www', url, 'com']).encode('utf-8')
        d = getPage(bytesUrl)
        # d.addCallback(convertToBytes)
        return d

    @subroute.route('/sleep/<int:n>')
    def sleepTask(request, n):
        d = threads.deferToThread(blockingTask,n)
        d.addCallback(addTag, 'h1')
        return d

def convertToBytes(result):
    return bytes(result.encode('utf-8'))

def error(failure):
    print('uh oh hotdog!')

def blockingTask(n):
    sleep(n)
    return 'Slept for %d seconds' % n

def addTag(string, tag):
    return '<{0}>{1}</{0}>'.format(tag, string)

app.run('localhost', 8000)
