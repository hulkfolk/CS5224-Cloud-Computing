import mysql.connector


def get_schools():
    connection = mysql.connector.connect(host='wordpress.cg0ilhgquv7x.us-east-1.rds.amazonaws.com',
                                         database='wordpress',
                                         user='wordpress',
                                         password='cloud12345')
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("select * from school;")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        return record


if __name__ == "__main__":
    get_schools()