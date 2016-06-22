import json
from klein import Klein

app = Klein()

@app.route('/')
def root(request):
    return 'Welcome'

@app.route('/hello')
def hello(request):
    return 'Hello World'

@app.route('/hello/<name>')
def helloName(request, name):
    return 'Hello %s!' % name

@app.route('/hello/<name>/<int:age>')
def helloNameAge(request, name, age):
    if age <= 1:
        return '%s is just starting life.' % name
    elif age >= 2 and age <= 29:
        return '%s is %d years old. You are so young!' % (name, age)
    return '%s is %d years old! You are so old!' % (name, age)

@app.route('/methods', methods=['POST', 'delete', 'Google'])
def specificMethods(request):
    return json.dumps({
                       'boolean': True,
                       'int': 1,
                       'list': [1,2,3]
                     })

if __name__ == '__main__':
    app.run(host='localhost', port=9000)
