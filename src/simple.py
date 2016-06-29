from twisted.internet import defer


def generateDeferred():
    d = defer.Deferred()
    d.addCallback(addition, 1, 2, 3, 4)
    d.addErrback(errorHasHappened, '^^^ Error ^^^')
    d.addCallback(print)
    return d

def addition(result, *numbers, toString=False):
    if toString:
        return str(result + sum(numbers))
    return result + sum(numbers)

def errorHasHappened(failure, msg):
    """
    Print the traceback and a short message.

    :param failure: 
    """
    print()
    print('Traceback: {0}'.format(failure))
    print(msg)

generateDeferred().callback(200)
generateDeferred().callback('hello')
