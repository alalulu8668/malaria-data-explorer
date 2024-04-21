import os 
import pandas as pd
import random
from datetime import datetime, timedelta


def load_data_info():# load data info from folder /mnt/disks/data/data/npy_v2
    data_folder = '/mnt/disks/data/data/npy_v2'
    data_files = os.listdir(data_folder)
    data_files = [f for f in data_files if f.endswith('.npy')]
    data_info_list = []

    # loop through the files and get the data info
    for f in data_files:
        # get the name of the file, remove the extension
        name = f.split('.npy')[0]
        # Split the filename by '-' to separate sections
        parts = name.split('_')
        # get timestamp, last two parts
        time_stamp = parts[-2] + '_' + parts[-1]
        # the rest of the parts are the patient id
        patient_id = '_'.join(parts[:-2])
        # store the data in the list
        data_info_list.append({'file_name': f, 'patient_id': patient_id, 'time_stamp': time_stamp})

    # create a DataFrame from the list of dictionaries
    data_info = pd.DataFrame(data_info_list)
    print(data_info.head())
    return data_info

# Helper function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

# Random generation of patient data
def generate_patient_info():
    age = random.randint(18, 100)
    gender = random.choice(['Male', 'Female', 'Other'])
    height = random.randint(140, 200)  # height in cm
    weight = random.randint(40, 150)  # weight in kg
    bmi = calculate_bmi(weight, height)
    ethnicity = random.choice(['Caucasian', 'African American', 'Hispanic', 'Asian', 'Other'])
    smoking_status = random.choice(['Non-smoker', 'Current smoker', 'Former smoker'])
    alcohol_consumption = random.choice(['None', 'Light', 'Moderate', 'Heavy'])
    diet_type = random.choice(['Omnivore', 'Vegetarian', 'Vegan', 'Keto', 'Pescatarian', 'Paleo'])
    chronic_conditions = random.choice(['None', 'Diabetes', 'Hypertension', 'Heart Disease', 'Asthma'])
    medication_use = random.choice(['Yes', 'No'])
    family_medical_history = random.choice(['None', 'Cancer', 'Diabetes', 'Heart Disease'])
    previous_surgeries = random.choice(['None', 'Appendectomy', 'Hip Replacement', 'CABG'])
    physical_activity_level = random.choice(['Sedentary', 'Lightly active', 'Moderately active', 'Very active'])
    insurance_status = random.choice(['Insured', 'Uninsured', 'Medicaid', 'Medicare'])
    socioeconomic_status = random.choice(['Low', 'Middle', 'High'])
    geographic_location = random.choice(['Urban', 'Suburban', 'Rural'])
    date_of_last_visit = datetime.now() - timedelta(days=random.randint(1, 365))
    clinical_trial_participant = random.choice(['Yes', 'No'])

    patient_info = {
        "Age": age,
        "Gender": gender,
        "Height": height,
        "Weight": weight,
        "BMI": bmi,
        "Ethnicity": ethnicity,
        "Smoking Status": smoking_status,
        "Alcohol Consumption": alcohol_consumption,
        "Diet Type": diet_type,
        "Chronic Conditions": chronic_conditions,
        "Medication Use": medication_use,
        "Family Medical History": family_medical_history,
        "Previous Surgeries": previous_surgeries,
        "Physical Activity Level": physical_activity_level,
        "Insurance Status": insurance_status,
        "Socioeconomic Status": socioeconomic_status,
        "Geographic Location": geographic_location,
        "Date of Last Visit": date_of_last_visit.strftime('%Y-%m-%d'),
        "Clinical Trial Participant": clinical_trial_participant
    }

    return patient_info

# Generate fake patient data for each unique patient in the dataset
def generate_complete_patient_data():
    data_info = load_data_info()
    grouped_data_info = data_info.groupby('patient_id')
    all_patient_data = []

    for patient_id, group in grouped_data_info:
        patient_info = generate_patient_info()
        for _, row in group.iterrows():
            # Combine patient_info with specific file information
            full_patient_record = {**patient_info, 
                                   'patient_id': patient_id, 
                                   'image_data': os.path.join('/mnt/disks/data/data/npy_v2', row['file_name'])}
            all_patient_data.append(full_patient_record)
    
    # Convert list of dictionaries into a DataFrame
    complete_patient_data = pd.DataFrame(all_patient_data)
    # save the data to a csv file
    complete_patient_data.to_csv('complete_patient_data.csv', index=False)
    return complete_patient_data

if __name__ == '__main__':
    complete_patient_data = generate_complete_patient_data()
    print(complete_patient_data.head())

