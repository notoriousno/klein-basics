from klein import Klein
from twisted.web.resource import Resource


app = Klein()

@app.route('/write')
def gradualWrite(request):
    """
    Gradually create the content body
    """
    for x in range(5):
        request.write(b'<h1>Header</h1>')

@app.route('/args')
def getA(request):
    """
    Display all the key/value pairs from either form data or query string.
    """
    return '{0}'.format(request.args)

@app.route('/setHeader')
def setHeader(request):
    """
    This will do a bit more than just set the header...

    * Set the Content-Type to application/xml.
    * Set status code to 418.
    * Retrieve request arguments, such as form data. Notice that the values are always in lists.
    """
    request.setHeader('Content-Type', 'application/xml')    # set the content-type to xml
    request.setResponseCode(418)        # set status code as 418 (I'm a teapot)

    request.write(b'<ol>\r\n')          # use write() to gradually create the response body
    for key, value in request.args.items():
        item = '<li>{0}:  {1}</li>\r\n'.format(key, value)      # get the key value pairs from form data
        request.write(item.encode('utf-8'))
    request.write(b'</ol>')

@app.route('/cookies')
def cookiesAndSessions(request):
    """
    """
    value = request.args.get(b'cookie', [b'default'])
    request.addCookie('cookie', value[0])
    sess = request.getSession()

@app.route('/redirect')
def redirect(request):
    """
    """
    request.redirect('https://www.yahoo.com')


if __name__ == '__main__':
    app.run('localhost', 9000)
