import json

from klein import Klein
from werkzeug.exceptions import HTTPException


class BrewTea(HTTPException):
    """
    Set status code and brief message. Overloading functions like ``get_
    """
    code = 418
    description = 'DEFAULT: Someone is brewing tea'

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json'), ('Quote-of-the-Day', 'To be or not to be. That is the question.')]

    def get_body(self, environ=None):
        message = {}
        message['description'] = self.description
        return json.dumps(message)


app = Klein()

@app.route('/brew')
def defaultBrew(request):
    """
    Raise a custom HTTPException class.  Pass a message as data to this endpoint.
    """
    msg = request.content.read()
    if not msg:
        raise BrewTea()
    raise BrewTea(msg.decode('utf-8'))


if __name__ == '__main__':
    app.run('localhost', 9000)

