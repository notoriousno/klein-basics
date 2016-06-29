from __future__ import print_function
from twisted.internet import defer


def addition(result, *numbers, **kw):
    return result + sum(numbers)

def errorHasHappened(failure, msg):
    print(msg)

d = defer.succeed(200).addCallback(addition, 10, 20).addCallback(print)
defer.fail(Exception()).addErrback(errorHasHappened, 'Errback executed')
