import json

from klein import Klein
from twisted.enterprise import adbapi
from twisted.internet import reactor


class Database(object):

    dbpool = adbapi.ConnectionPool('sqlite3', 'TEST.sqlite')

    def _createDB(self, dbObj):
        """
        """
        createTable = 'CREATE TABLE async_table (' \
            '_id_ INTEGER PRIMARY KEY,' \
            'first_name TEXT,' \
            'last_name TEXT,' \
            'age INTEGER' \
            ')'
        dbObj.execute(createTable)

    def createDB(self):
        """
        """
        return self.dbpool.runInteraction(self._createDB)

    def _insert(self, dbObj, first, last, age):
        """
        """
        dbObj.execute(\
            'INSERT INTO async_table ('\
            'first_name, last_name, age)'\
            'VALUES ("%s", "%s", %d)' % (first, last, age))

    def insert(self, first, last, age):
        """
        """
        return self.dbpool.runInteraction(self._insert, first, last, age)

    def queryAll(self):
        """
        """
        return self.dbpool.runQuery('SELECT * FROM async_table')


class WebApp(object):

    app = Klein()
    db = Database()

    #---------- Callbacks -----------#
    def onSuccess(self, result, msg):
        # print(result)
        return msg

    def onFail(self, failure, msg):
        # print(failure)
        return msg

    def getResults(self, results, request):
        request.setHeader('Content-Type', 'application/json')
        responseJSON = []
        for record in results:
            mapper = {}
            mapper['id'] = record[0]
            mapper['first_name'] = record[1].encode('utf-8')
            mapper['last_name'] = record[2].encode('utf-8')
            mapper['age'] = record[3]
            responseJSON.append(mapper)
        return json.dumps(responseJSON)


    #--------- Routes ---------#
    @app.route('/create')
    def createDB(self, request):
        d = self.db.createDB()
        d.addCallback(self.onSuccess, 'Successfully created db')
        d.addErrback(self.onFail, 'Failed to create db')
        return d

    @app.route('/insert', methods=['POST'])
    def insert(self, request):
        first_name = request.args.get('fname', [None])[0]
        last_name = request.args.get('lname', [None])[0]
        age = int(request.args.get('age', [0])[0])

        d = self.db.insert(first_name, last_name, age)
        d.addCallback(self.onSuccess, 'Insert success')
        d.addErrback(self.onFail, 'Insert failed')
        return d

    @app.route('/query', methods=['GET'])
    def queryAll(self, request):
        d = self.db.queryAll()
        d.addCallback(self.getResults, request)
        return d


if __name__ == '__main__':
    webapp = WebApp()
    webapp.app.run('localhost', 9000)

