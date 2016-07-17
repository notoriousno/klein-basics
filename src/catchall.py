from klein import Klein


app = Klein()

@app.route('/<path:others>')
def catchAll(request, others):
    request.redirect('/')

@app.route('/')
def home(request):
    return 'Home'

@app.route('/hello')
def hello(request):
    return 'Hello'


if __name__ == '__main__':
    app.run('localhost', 9000)

