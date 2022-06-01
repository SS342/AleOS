
def create(connection, cursor, data):
    table_name = data['name']
    sql = f"CREATE TABLE IF NOT EXISTS {table_name}("
    for key, value in data['fields'].items():

        sql += f"{key} {value},"

    sql = sql[:-1] + ");"

    cursor.execute(sql)
    connection.commit()
