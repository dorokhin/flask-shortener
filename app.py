import os
import psycopg2
from flask import Flask, jsonify
from pathlib import Path
from dotenv import load_dotenv
from flask import render_template
from psycopg2.extras import NamedTupleCursor

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)


def connect(host=None, database=None, user=None, password=None, **kwargs):

    host = host or os.environ['POSTGRESQL_HOST']
    database = database or os.environ['POSTGRESQL_DB']
    user = user or os.environ['POSTGRESQL_USER']
    password = password or os.environ['POSTGRESQL_PASSWORD']

    return psycopg2.connect(host=host, database=database, user=user, password=password, **kwargs)


def select(conn, query: str, params=None, name=None, itersize=5000):
    """Return a select statement's results as a namedtuple.
    Parameters
    ----------
    conn : database connection
    query : select query string
    params : query parameters.
    name : server side cursor name. defaults to client side.
    itersize : number of records fetched by server.
    """

    with conn.cursor(name, cursor_factory=NamedTupleCursor) as cursor:
        cursor.itersize = itersize
        cursor.execute(query, params)

        for result in cursor:
            yield result


@app.route('/')
def index():
    con = None

    try:
        con = connect()
        cur = con.cursor()
        query = 'select * from url_data_store WHERE NOT deleted ORDER BY id ' \
                'ASC LIMIT {limit} OFFSET {offset};'.format(limit=100, offset=0)
        cur.execute(query)
        data = cur.fetchall()
    finally:
        if con:
            con.close()

    return render_template('index.html', value='variable test', url_data=data)


if __name__ == '__main__':
    app.run()
