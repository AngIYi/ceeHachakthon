import sqlite3

db_path = "databases/hospital_data.db"


def fetch_patient_by_id(patient_id):
  connection = sqlite3.connect(db_path)

  cursor = connection.cursor()

  query = "SELECT * FROM patients WHERE patient_id = ?"

  cursor.execute(query, (patient_id,))

  row = cursor.fetchone()

  if row : 
    column_names = [description[0] for description in cursor.description]
    patient_data = dict(zip(column_names, row))
    print(row)

  else:
    print(f"No patient found with patient_id {patient_id}")

  # Close the cursor and connection
  cursor.close()
  connection.close()

  return patient_data


def fetch_all_patients() : 
  patients = []
  
  connection = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
  cursor = connection.cursor()

# Define your SQL query to retrieve data (e.g., all patients)
  query = "SELECT * FROM patients"  # Adjust based on your actual query and table

# Execute the query
  cursor.execute(query)

  # Fetch all the results
  rows = cursor.fetchall()
  column_names = [description[0] for description in cursor.description]

  # Loop through the rows and print them
  for row in rows:
    print(row)  
    patient_data = dict(zip(column_names, row))
    patients.append(patient_data)


  # Close the cursor and connection to free up resources
  cursor.close()
  connection.close()

  return patients

def fetch_app_user_data(user_id=None, patient_id=None,username=None):

  connection = sqlite3.connect(db_path)

  cursor = connection.cursor()

  if username:
    print(f"Fetching data for username: {username}")

    query = f"SELECT * FROM app_user_profiles WHERE username = {username}"

    cursor.execute(query)

    row = cursor.fetchone()
    if row : 
      column_names = [description[0] for description in cursor.description]
      patient_data = dict(zip(column_names, row))
      print(row)

    else:
      print(f"No patient found with username {username}")
  
  elif user_id : 

    print(f"Fetching data for user_id: {user_id}")

    query = f"SELECT * FROM app_user_profiles WHERE user_id = {user_id}"

    cursor.execute(query)

    row = cursor.fetchone()
    if row : 
      column_names = [description[0] for description in cursor.description]
      patient_data = dict(zip(column_names, row))
      print(row)

    else:
      print(f"No patient found with user_id {user_id}")
  
  elif patient_id : 
    print(f"Fetching data for patient_id: {patient_id}")

    query = f"SELECT * FROM app_user_profiles WHERE patient_id = {patient_id}"

    cursor.execute(query)

    row = cursor.fetchone()
    if row : 
      column_names = [description[0] for description in cursor.description]
      patient_data = dict(zip(column_names, row))
      print(row)

    else:
      print(f"No patient found with patient_id {patient_id}")
    
  return patient_data

# TEST

"""
keys:


patient_id
first_name
last_name
age
height
weight
bmi
entry_date
avg_glucose
basal_insulin
basal_metabolic_rate
daily_insulin_dose
cgm_device
glucose_monitoring_index
std_dev_glucose
variation_coefficient
time_active
time_in_range_high
time_in_range_very_high
time_in_range_low
time_in_range_very_low
time_in_range_normal
time_in_range
weight_category
app_user_id
"""
test_patient = fetch_patient_by_id(1)
print(f"[TEST] Patient name : {test_patient["first_name"]}")
print(f"[TEST] Patient's daily insulin dose : {test_patient["daily_insulin_dose"]}")

all_patients = fetch_all_patients()
print(f"[TEST] All patients data : {all_patients}")


"""
keys:

user_id
patient_id
username
password
points
"""
test_user = fetch_app_user_data(patient_id=3)
print(f"[TEST] Patient username : {test_user["username"]}")
print(f"[TEST] Patient password : {test_user["password"]}")
print(f"[TEST] Points/Score for ths patient : {test_user["points"]}")