import psycopg2


class UsersDB:
    def __init__(self):
        self.__connection()
        # self.__drop_table()
        self.__create_table()

    def __connection(self):
        self._conn = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="192.168.0.158",
                                      port="5432",
                                      database="users")
        self._cur = self._conn.cursor()

    def __drop_table(self):
        self._cur.execute("DROP TABLE IF EXISTS users")
        self._conn.commit()

    def __create_table(self):
        self._cur.execute("""CREATE TABLE IF NOT EXISTS users (
                          id SERIAL PRIMARY KEY, 
                          username TEXT, password TEXT, 
                          telephone_number TEXT,
                          ip_address TEXT)""")
        self._conn.commit()

    def _execute_query(self, query, params=None):
        try:
            if params:
                self._cur.execute(query, params)
            else:
                self._cur.execute(query)

            self._conn.commit()
            return self._cur
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def set_user(self, username: str, password: str, telephone_number: str, ip_address: str) -> None:
        query = "INSERT INTO users (username, password, telephone_number, ip_address) VALUES (%s, %s, %s, %s)"
        self._execute_query(query, (username, password, telephone_number, ip_address))

    def find_username(self, username: str) -> tuple:
        query = "SELECT username FROM users WHERE username = %s"
        db_username = self._execute_query(query, (username,))
        return db_username

    def find_telephone_number(self, telephone_number: str) -> tuple:
        query = "SELECT telephone_number FROM users WHERE telephone_number = %s"
        db_telephone_number = self._execute_query(query, (telephone_number,))
        return db_telephone_number

    def find_password(self, username: str) -> tuple:
        query = "SELECT password FROM users WHERE username = %s"
        db_password = self._execute_query(query, (username,))
        return db_password.fetchone()
