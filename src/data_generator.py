"""
OPOR Patient Record Demo - Data Generator
Generates fake patient identities and encounters for demonstration purposes.
"""

import json
import uuid
from datetime import datetime, timedelta
from faker import Faker
import random
import os

fake = Faker('en_CA')  # Canadian locale for realistic data

class DataGenerator:
    """Generate fake patient and encounter data following OPOR principles."""
    
    def __init__(self):
        self.patients = []
        self.encounters = []
        
    def generate_patient(self):
        """Generate a single fake patient with Canadian demographics."""
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        
        patient = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": dob.strftime("%Y-%m-%d"),
            "gender": random.choice(["Male", "Female", "Other"]),
            "health_card_number": self._generate_health_card(),
            "address": f"{fake.street_address()}, {fake.city()}, {fake.province_abbr()} {fake.postalcode()}",
            "phone": fake.phone_number(),
            "email": fake.email()
        }
        
        return patient
    
    def _generate_health_card(self):
        """Generate a fake Ontario health card number format."""
        return f"{random.randint(1000, 9999)}-{random.randint(100, 999)}-{random.randint(100, 999)}"
    
    def generate_clinical_records(self, patient_id):
        """Generate clinical records for a patient compatible with UnifiedRecordSystem."""
        
        diagnoses = [
            "Hypertension",
            "Type 2 Diabetes",
            "Acute Bronchitis",
            "Osteoarthritis",
            "Anxiety Disorder",
            "Migraine",
            "Gastroesophageal Reflux Disease"
        ]
        
        medications = [
            "Metformin 500mg",
            "Lisinopril 10mg",
            "Atorvastatin 20mg",
            "Omeprazole 20mg",
            "Levothyroxine 50mcg"
        ]
        
        allergies = [
            "Penicillin",
            "Sulfa drugs",
            "Aspirin",
            "Latex",
            "Peanuts"
        ]
        
        immunizations = [
            "Influenza",
            "COVID-19",
            "Tetanus",
            "Pneumococcal",
            "Hepatitis B"
        ]
        
        facilities = [
            "Toronto General Hospital",
            "St. Michael's Hospital",
            "Sunnybrook Health Sciences Centre",
            "Mount Sinai Hospital",
            "Women's College Hospital"
        ]
        
        # Generate 2-5 clinical records
        num_records = random.randint(2, 5)
        clinical_records = []
        
        for _ in range(num_records):
            visit_date = fake.date_time_between(start_date='-2y', end_date='now')
            
            record = {
                "visit_id": str(uuid.uuid4()),
                "visit_date": visit_date.isoformat(),
                "facility": random.choice(facilities),
                "provider": f"Dr. {fake.last_name()}",
                "specialty": random.choice(["Family Medicine", "Internal Medicine", "Emergency Medicine"]),
                "chief_complaint": fake.sentence(nb_words=6),
                "diagnosis": random.choice(diagnoses),
                "vital_signs": {
                    "blood_pressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
                    "heart_rate": random.randint(60, 100),
                    "temperature": round(random.uniform(36.5, 37.5), 1)
                },
                "notes": fake.paragraph(nb_sentences=3)
            }
            clinical_records.append(record)
        
        # Generate medications
        num_meds = random.randint(0, 3)
        medication_list = []
        for _ in range(num_meds):
            medication_list.append({
                "name": random.choice(medications),
                "prescribed_date": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
                "prescriber": f"Dr. {fake.last_name()}"
            })
        
        # Generate allergies
        num_allergies = random.randint(0, 2)
        allergy_list = [{"allergen": random.choice(allergies), "severity": random.choice(["Mild", "Moderate", "Severe"])} 
                        for _ in range(num_allergies)]
        
        # Generate immunizations
        num_immunizations = random.randint(1, 3)
        immunization_list = [{"vaccine": random.choice(immunizations), 
                              "date": fake.date_time_between(start_date='-5y', end_date='now').isoformat()} 
                             for _ in range(num_immunizations)]
        
        # Generate lab results
        num_labs = random.randint(1, 3)
        lab_results = []
        for _ in range(num_labs):
            lab_results.append({
                "test_name": random.choice(["Complete Blood Count", "Lipid Panel", "HbA1c", "Thyroid Panel"]),
                "test_date": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
                "result": "Normal",
                "facility": random.choice(facilities)
            })
        
        return {
            "clinical_records": clinical_records,
            "medications": medication_list,
            "allergies": allergy_list,
            "immunizations": immunization_list,
            "lab_results": lab_results
        }
    
    def generate_dataset(self, num_patients=15):
        """Generate complete dataset with patients and encounters."""
        print(f"Generating {num_patients} patients with multiple encounters...")
        
        for i in range(num_patients):
            # Generate patient
            patient = self.generate_patient()
            self.patients.append(patient)
            
            # Generate 2-5 encounters per patient
            num_encounters = random.randint(2, 5)
            for _ in range(num_encounters):
                encounter = self.generate_encounter(patient["patient_uuid"])
                self.encounters.append(encounter)
            
            print(f"Generated patient {i+1}/{num_patients} with {num_encounters} encounters")
        
        print(f"\nTotal: {len(self.patients)} patients, {len(self.encounters)} encounters")
        
    def save_to_files(self, data_dir="data"):
        """Save generated data to JSON files."""
        os.makedirs(data_dir, exist_ok=True)
        
        patients_file = os.path.join(data_dir, "patients.json")
        encounters_file = os.path.join(data_dir, "encounters.json")
        
        with open(patients_file, 'w', encoding='utf-8') as f:
            json.dump(self.patients, f, indent=2, ensure_ascii=False)
        
        with open(encounters_file, 'w', encoding='utf-8') as f:
            json.dump(self.encounters, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to:")
        print(f"  - {patients_file}")
        print(f"  - {encounters_file}")

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_dataset(num_patients=15)
    generator.save_to_files()
