import sys

import pymysql

print(sys.path)
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Table, MetaData
import matplotlib.pyplot as plt
import seaborn as sns


pymysql.install_as_MySQLdb()

# Load environment variables from .env
load_dotenv("private.env")

# Retrieve MySQL credentials from environment variables
mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")

# Construct the connection string with the new user credentials
connection_string = f"mysql+mysqlconnector://{mysql_username}:{mysql_password}@localhost:3306/HealthcareDB"

# Connect to the MySQL database
engine = create_engine(connection_string)

# Read data from the CSV file into a DataFrame
csv_file_path = "data/Healthcare-Diabetes.csv"

df = pd.read_csv(csv_file_path)

# Print the first few rows of the DataFrame to verify the data
print(df.head())

metadata = MetaData()
diabetes_data_table = Table("DiabetesData", metadata, autoload_with=engine)
metadata.create_all(engine, checkfirst=True)

# Insert data into the MySQL table
df.to_sql("DiabetesData", con=engine, if_exists="replace", index=False)

# Close the database connection
engine.dispose()

# Continue data analysis with Pandas, Matplotlib, and Seaborn
# Example: Display a pairplot
sns.pairplot(
    df[["Pregnancies", "Glucose"]]
)  # , """'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
#           'DiabetesPedigreeFunction', 'Age', 'Outcome']])
plt.show()
