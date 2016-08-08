import json

from klein import Klein
from twisted.enterprise import adbapi
from twisted.internet import reactor


class Database(object):

    dbpool = adbapi.ConnectionPool('sqlite3', 'AsyncDB.sqlite', check_same_thread=False)
    table = 'People'


    def _createDB(self, cursor):
        """
        Execute the CREATE TABLE statement.

        :param cursor: sqlite3.cursor
        """
        create_stmt = 'CREATE TABLE %s (' \
            '_id_ INTEGER PRIMARY KEY,' \
            'first_name TEXT,' \
            'last_name TEXT,' \
            'age INTEGER' \
            ')' % (self.table)
        cursor.execute(create_stmt)

    def createDB(self):
        """
        Create a table using Twisted.

        :return: Deferred
        """
        return self.dbpool.runInteraction(self._createDB)

    def _insert(self, cursor, first, last, age):
        """
        Execute INSERT statement.

        :param cursor: sqlite3.cursor
        :param first: str. First name
        :param last: str. Last name
        :param age: int.
        """
        insert_stmt = 'INSERT INTO %s (first_name, last_name, age) VALUES ("%s", "%s", %d)' % (self.table, first, last, age)
        cursor.execute(insert_stmt)

    def insert(self, first, last, age):
        """
        Insert data into the database using Twisted.

        :return: Deferred
        """
        return self.dbpool.runInteraction(self._insert, first, last, age)

    def queryAll(self):
        """
        Query the database using Twisted.

        :return: Deferred
        """
        select_stmt = 'SELECT * FROM %s' % (self.table)
        return self.dbpool.runQuery(select_stmt)


class WebApp(object):

    app = Klein()
    db = Database()


    #--------- Routes ---------#
    @app.route('/create')
    def createDB(self, request):
        """
        Create a sqlite async database with a People table.
        It's usually a bad idea to expose this kind of feature.
        """
        d = self.db.createDB()
        d.addCallback(self.onSuccess, request, 'Successfully created db')
        d.addErrback(self.onFail, request, 'Failed to create db')
        return d

    @app.route('/insert', methods=['POST'])
    def insert(self, request):
        """
        Insert first name, last name, and age into the db asynchronously.
        Pass the following arguments fname (str), lname (str), age (int).
        """
        first_name = request.args.get('fname', [None])[0]
        last_name = request.args.get('lname', [None])[0]
        age = int(request.args.get('age', [0])[0])

        d = self.db.insert(first_name, last_name, age)
        d.addCallback(self.onSuccess, request, 'Insert success')
        d.addErrback(self.onFail, request, 'Insert failed')
        return d

    @app.route('/query', methods=['GET'])
    def queryAll(self, request):
        """
        Query the database asynchronously and display the results as JSON.
        """
        d = self.db.queryAll()
        d.addCallback(self.toJSON, request)
        d.addErrback(self.onFail, request, 'Failed to query db')
        return d


    #---------- Callbacks -----------#
    def onSuccess(self, result, request, msg):
        request.setResponseCode(201)
        response = {'message': msg}
        return json.dumps(response)

    def onFail(self, failure, request, msg):
        request.setResponseCode(417)
        response = {'message': msg}
        return json.dumps(response)

    def toJSON(self, results, request):
        """
        Set the Content-Type and return a JSON representation of the Person table.

        :return: JSON containing records from db.
        """
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


if __name__ == '__main__':
    webapp = WebApp()
    webapp.app.run('localhost', 9000)

