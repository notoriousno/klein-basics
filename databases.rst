Database Usage
===============

.. note::

    As of Twisted 16.3, ``adbapi`` is only supported on Python 2.x, so the following code will not work on Python 3.x.  On the bright side, v16.4 will mostly likly include the package for Python 3.x.

twisted.enterprise.adbapi
-------------------------

Twisted, and subsequently Klein, allows asynchronous interaction with databases using blocking/sequential interfaces using `adbapi <http://twistedmatrix.com/documents/current/core/howto/rdbms.html>`_.  The only caveat is that the database interface must be `DBAPI 2.0 <https://www.python.org/dev/peps/pep-0249/>`_ compliant.  For instance, if a PostgreSQL database needs to be accessed, then a typical interaction would be something like:

.. code-block:: python

   import psycopg2

   connection = psycopg2.connect(database='Tutorial', user='admin', host='10.10.10.10')
   cursor = connection.cursor()

   cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
   cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "mydata"))
   cursor.execute("SELECT * FROM test;")

   connection.commit()
   cursor.close()
   connection.close()


Depending on environment settings, connecting to the database server, inserting data, or even querying for records can take an unpredictable amount of time, which can cause your application to slow down considerably.  These unknown variables can be mitigated by using asynchronous functionality in the ``adbapi`` module.  The asynchronous method is similar to the sequential code above, albeit using deferreds and callbacks:

.. code-block:: python

   from twisted.internet import defer, reactor
   from twisted.enterprise.adbapi import ConnectionPool

   def createDB(cursor):
       cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

   def insert(cursor, num, data):
       cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (num, data))

   @defer.inlineCallbacks
   def main():
       connection = ConnectionPool('psycopg2', database='Tutorial', user='admin', host='10.10.10.10')
       yield connection.runInteraction(createDB)
       yield connection.runInteraction(insert, 100, 'mydata')
       results = yield connection.runQuery('SELECT * FROM test')
       print(results)


   main()
   reactor.run()


``ConnectionPool`` manages database connections.  It takes the name of the database module as the first parameter, followed by all arguments that would get passed into the ``connect()`` function.  Then when the database connection is required, it will be created in a separate thread so that the main thread isn't being blocked.  So for the examples above, ``psycopg2.connect(database, user, host)`` is the equivalent to ``ConnectionPool('psycopg2', database, user, host)``.  After running each database interaction, the transaction will be committed, therefore explicit ``commit()`` calls aren't required.


Other Modules
-------------

The base ``adbapi`` module is great for quick results, but many desire a bit more functionality.  Luckily there's a vibrant array of database modules which support Twisted.  This includes standard relational databases, as well as popular NoSQL options.  There's even a good ORM available!  I'll provide a list of popular modules at the bottom, but unfortunately it's not very practical to discuss all the various options in such a general post.  Perhaps in a future post, I'll elaborate on specific modules.


Combine ``adbapi`` with Klein
-----------------------------

Let's create an object that houses core database functionality required for a simple web app.  The database of choice will be ``sqlite3`` with a table called ``People``.

.. code-block:: python

   class Database(object):

       dbpool = adbapi.ConnectionPool('sqlite3', 'AsyncDB.sqlite', check_same_thread=False)
       table = 'People'

       def _createDB(self, cursor):
           create_stmt = 'CREATE TABLE %s (' \
               '_id_ INTEGER PRIMARY KEY,' \
               'first_name TEXT,' \
               'last_name TEXT,' \
               'age INTEGER' \
               ')' % (self.table)
           cursor.execute(create_stmt)

       def createDB(self):
           return self.dbpool.runInteraction(self._createDB)

       def _insert(self, cursor, first, last, age):
           insert_stmt = 'INSERT INTO %s (first_name, last_name, age) VALUES ("%s", "%s", %d)' % (self.table, first, last, age)
           cursor.execute(insert_stmt)

       def insert(self, first, last, age):
           return self.dbpool.runInteraction(self._insert, first, last, age)

       def queryAll(self):
           select_stmt = 'SELECT * FROM %s' % (self.table)
           return self.dbpool.runQuery(select_stmt)

Next, let's create an object that holds the routes ``/create``, ``/insert``, ``/query`` along with the ``Database`` class created previously.

.. code-block:: python

   class WebApp(object):

       app = Klein()
       db = Database()

       #--------- Routes ---------#
       @app.route('/create')
       def createDB(self, request):
           d = self.db.createDB()
           d.addCallback(self.onSuccess, request, 'Successfully created db')
           d.addErrback(self.onFail, request, 'Failed to create db')
           return d

       @app.route('/insert', methods=['POST'])
       def insert(self, request):
           first_name = request.args.get('fname', [None])[0]
           last_name = request.args.get('lname', [None])[0]
           age = int(request.args.get('age', [0])[0])

           d = self.db.insert(first_name, last_name, age)
           d.addCallback(self.onSuccess, request, 'Insert success')
           d.addErrback(self.onFail, request, 'Insert failed')
           return d

       @app.route('/query', methods=['GET'])
       def queryAll(self, request):
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


The ``/create`` endpoint needs to be accessed first so that a database can be created.  A person's first name, last name, and age need to be passed in as form data to the ``/insert`` endpoint.  Finally the results can be queried and represented in JSON from the ``/query`` endpoint.

.. code-block:: bash

   curl -v localhost:9000/create
   curl -v -X POST -d fname=Tom\&lname=Brady\&age=39 localhost:9000/insert
   curl -X GET localhost:9000/query | python -m json.tool | less


Examples
--------

* dbwebapp.py


References
----------

* `Twisted RDBMS support <http://twistedmatrix.com/documents/current/core/howto/rdbms.html>`_ - Official Twisted doc
* `adbapi.ConnectionPool API <https://twistedmatrix.com/documents/current/api/twisted.enterprise.adbapi.ConnectionPool.html>`_
* `Twistar ORM <http://findingscience.com/twistar/>`_ - An ORM "similar" to SQLAlchemy and Django's ORM
* `txpostgres <http://txpostgres.readthedocs.io/en/latest/>`_ - Twisted version of ``psycopg2``.
* `txmongo <https://github.com/twisted/txmongo>`_ - Async module for MongoDB
* `RethinkDB <https://www.rethinkdb.com/docs/async-connections/#python-with-tornado-or-twisted>`_ - Realtime db
