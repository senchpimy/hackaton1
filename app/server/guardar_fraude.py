import csv
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


# Function to insert fraud data into the database
def insert_fraud_data(csv_file):
    cursor = db.cursor()

    # Open the CSV file
    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)

        # SQL query to insert the fraud data
        insert_query = """
            INSERT INTO transactions (num_cliente, num_tarjeta, fecha, establecimiento, importe, fraude)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Iterate over the rows in the CSV file
        for row in csv_reader:
            # Only insert rows where 'Fraude' is True
            if row["Fraude"].lower() == "true":
                data = (
                    row["num_cliente"],
                    row["NUM_TARJETA"],
                    row["Fecha"],
                    row["Establecimiento"],
                    row["Importe"],
                    True,
                )
                cursor.execute(insert_query, data)

        db.commit()  # Commit the transaction
        print("Fraud data inserted successfully!")

    cursor.close()


insert_fraud_data("./fraude.csv")

db.close()
