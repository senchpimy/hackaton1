import MySQLdb

# MySQL configuration
config = {}
config["MYSQL_HOST"] = "localhost"
config["MYSQL_USER"] = "plof"
config["MYSQL_PASSWORD"] = "pass"
config["MYSQL_DB"] = "fraud_detection"

# Connect to the MySQL database
db = MySQLdb.connect(
    config["MYSQL_HOST"],
    config["MYSQL_USER"],
    config["MYSQL_PASSWORD"],
    config["MYSQL_DB"],
)


def check_fraud(num_cliente):
    cursor = db.cursor()

    # Query to check if there are any fraudulent transactions for the given account number
    query = """
        SELECT COUNT(*) 
        FROM transactions
        WHERE num_cliente = %s AND fraude = TRUE
    """

    cursor.execute(query, (num_cliente,))
    result = cursor.fetchone()  # Get the first row of the result

    cursor.close()

    if result[0] > 0:
        return True  # Fraud detected
    else:
        return False  # No fraud detected
