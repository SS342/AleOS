class Connect:
    def __init__(self, path : str):
        import sqlite3
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def return_conn_cur(self):
        return [self.connection, self.cursor]