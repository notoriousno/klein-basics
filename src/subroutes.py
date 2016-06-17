from klein import Klein

app = Klein()

@app.route('/hello')
def index(request):
    return 'Hello from the subroutes example'

with app.subroute('/base') as sub:
    @sub.route('/first')
    def first(request):
        return 'first'

    @sub.route('/second')
    def second(request):
        return 'second'

    @sub.route('/third')
    def third(request):
        return 'third'

