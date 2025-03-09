import sqlite3

# Function to connect to the database
import sqlite3

# Function to create and connect to the SQLite database
def create_and_connect_to_db():
  try:
    # Connect to SQLite database (it will create the file if it doesn't exist)
    connection = sqlite3.connect('patient_data.db')  # Creates a local file `patient_data.db`
    print("Successfully connected to the SQLite database")

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
          patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          birth_date TEXT,
          gender TEXT,
          contact_number TEXT
        )
    """)
    print("Table 'patients' created (or already exists)")

    # Insert example data (if the table is empty)
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, birth_date, gender, contact_number)
        VALUES ('John', 'Doe', '1985-06-15', 'Male', '123-456-7890')
    """)
    connection.commit()  # Commit the changes to the database
    print("Example data inserted into the 'patients' table")

    # Query the table and retrieve data
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    # Print the results
    for row in rows:
        print(row)

  except sqlite3.Error as e:
    print(f"Error: {e}")
  
  finally:
    # Close the connection
    if connection:
      cursor.close()
      connection.close()
      print("SQLite connection is closed")

# Run the function to create and connect to the database
create_and_connect_to_db()