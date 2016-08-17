from klein import Klein
from werkzeug.exceptions import HTTPException


class BrewTea(HTTPException):
    """
    Set status code and brief message. Overloading functions like ``get_
    """
    code = 418
    # description = 'DEFAULT: Someone is brewing tea'

    def __init__(self, request, description):
        super(BrewTea, self).__init__()
        self.request = request
        self.description = description

    def get_body(self, environ=None):
        self.request.setResponseCode(422)
        return self.description


app = Klein()

@app.route('/brew')
def defaultBrew(request):
    """
    Raise a custom HTTPException class.  Pass a message as data to this endpoint.
    """
    msg = request.content.read()
    if not msg:
        raise BrewTea(request)
    raise BrewTea(request, msg.decode('utf-8'))


if __name__ == '__main__':
    app.run('localhost', 9000)

