from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import psycopg2
import random
import os


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

NUM_OF_USERS = 10
USER_NAMES = ['Armin', 'Mike', 'Terminator', 'Predator']
MAIL_DOMAINS = ['google.com', 'outlook.com', 'amazon.com']
SQL_ = ['DROP TABLE IF EXISTS users CASCADE;',
        """
            CREATE TABLE users(
                id SERIAL PRIMARY KEY, 
                username VARCHAR (100) NOT NULL, 
                password VARCHAR (100) NOT NULL, 
                email VARCHAR (70) NOT NULL UNIQUE, 
                created_on TIMESTAMP NOT NULL, 
                updated_on TIMESTAMP NOT NULL, 
                deleted BOOLEAN,
                is_admin BOOLEAN
            );
        """,
        'DROP TABLE IF EXISTS url_data_store;',
        """
            CREATE TABLE url_data_store(
                 id SERIAL PRIMARY KEY,
                 url_hash VARCHAR (20) NOT NULL,
                 url VARCHAR (300) NOT NULL,
                 created_on TIMESTAMP NOT NULL,
                 viewed INT NOT NULL CHECK (viewed >= 0),
                 "user" INT references users(ID),
                 ip_address INET,
                 deleted BOOLEAN
            );
        """]


def connect(host=None, database=None, user=None, password=None, **kwargs):

    host = host or os.environ['POSTGRESQL_HOST']
    database = database or os.environ['POSTGRESQL_DB']
    user = user or os.environ['POSTGRESQL_USER']
    password = password or os.environ['POSTGRESQL_PASSWORD']

    return psycopg2.connect(host=host, database=database, user=user, password=password, **kwargs)


def generate_birth_date():
    year = random.randint(1930, 2001)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)


def generate_email():
    name = random.choice(USER_NAMES)
    year = random.randint(1930, 2001)
    number = random.randint(1, 999999999)
    domain = random.choice(MAIL_DOMAINS)
    return '{0}{1}{2}@{3}'.format(name, year, number, domain)


def generate_password(policy):
    """
    TODO: Write generate_password code
     use https://github.com/pyca/bcrypt
    :param policy:
    :return:
    """
    return 'FakePasswordWithoutSalt'


def generate_users(user_count):
    for i in range(0, user_count):
        user = {
            'username': random.choice(USER_NAMES),
            'password': generate_password(policy=None),
            'email': generate_email(),
            'created_on': datetime.now(),
            'updated_on': datetime.now(),
            'deleted': False,
            'is_admin': True
        }
        yield user


def create_db_table(sql):
    """
    :return:
    """
    con = None
    try:
        con = connect()
        cur = con.cursor()
        for statement in sql:
            cur.execute(statement)
            con.commit()
    finally:
        if con:
            con.close()


def fill_users_table(user_count=NUM_OF_USERS):
    """
    :return:
    """
    con = None

    try:
        con = connect()
        cur = con.cursor()
        user_data = ("""
            INSERT INTO users (username, password, email, created_on, updated_on, deleted, is_admin) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """)

        for user in generate_users(user_count):
            cur.execute(
                user_data, [
                    user['username'],
                    user['password'],
                    user['email'],
                    user['created_on'],
                    user['updated_on'],
                    user['deleted'],
                    user['is_admin']
                ]
            )
            con.commit()
    finally:
        if con:
            con.close()


def main():
    print('Create tables structure')
    create_db_table(SQL_)
    print('Fill tables')
    fill_users_table()


if __name__ == '__main__':
    main()
