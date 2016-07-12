from jinja2 import Template
from klein import Klein
from twisted.web.resource import NoResource


app = Klein()
template = Template('<h1>Hello {{ name }}! (Jinja)</h1>')

with app.subroute('/template') as subroute:
    @subroute.route('/basic/<name>')
    def basicTemplate(request, name='World'):
        return '<h1>Hello %s!</h1>' % (name)

    @subroute.route('/jinja/<name>')
    def jinjaTemplate(request, name='World'):
        request.setResponseCode(201)
        return template.render(name=name)


if __name__ == '__main__':
    app.run('localhost', 9000)
