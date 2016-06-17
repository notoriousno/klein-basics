from time import sleep

from klein import Klein
import treq
from twisted.internet import defer, threads, reactor


app = Klein()

with app.subroute('/tasks') as subroute:

    @subroute.route('/phishing/<url>')
    def phishAttack(request, url):
        d = treq.get('www.%s.com' % url)
        d.addCallbacks(treq.content, error)
        return d

    @subroute.route('/sleep/<int:n>')
    def sleepTask(request, n):
        d = threads.deferToThread(blockingTask,n)
        d.addCallback(addTag, 'h1')
        return d

def error(failure):
    print('uh oh hotdog!')

def blockingTask(n):
    sleep(n)
    return 'Slept for %d seconds' % n

def addTag(string, tag):
    return '<{0}>{1}</{0}>'.format(tag, string)

app.run('localhost', 8000)
