"""
Patient Identity Management System
Implements OPOR principle: One unique identity per person
"""

import json
import os
from datetime import datetime


class PatientIdentityManager:
    """Manages patient identities ensuring uniqueness"""
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.patients_file = os.path.join(data_dir, 'patients.json')
        self.patients = self._load_patients()
    
    def _load_patients(self):
        """Load patients from JSON file"""
        if os.path.exists(self.patients_file):
            with open(self.patients_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_patients(self):
        """Save patients to JSON file"""
        with open(self.patients_file, 'w', encoding='utf-8') as f:
            json.dump(self.patients, f, indent=2, ensure_ascii=False)
    
    def register_patient(self, patient_data):
        """
        Register a new patient with unique identity
        Returns patient_id if successful
        """
        # Check for duplicate health card number
        health_card = patient_data.get('health_card_number')
        if self._find_by_health_card(health_card):
            raise ValueError(f"Patient with health card {health_card} already exists")
        
        # Generate unique patient ID
        patient_id = f"OPOR-{len(self.patients) + 1:05d}"
        
        patient = {
            'patient_id': patient_id,
            'health_card_number': health_card,
            'first_name': patient_data.get('first_name'),
            'last_name': patient_data.get('last_name'),
            'date_of_birth': patient_data.get('date_of_birth'),
            'gender': patient_data.get('gender'),
            'address': patient_data.get('address'),
            'phone': patient_data.get('phone'),
            'email': patient_data.get('email'),
            'registered_at': datetime.now().isoformat()
        }
        
        self.patients.append(patient)
        self._save_patients()
        
        return patient_id
    
    def get_patient(self, patient_id):
        """Get patient by ID"""
        for patient in self.patients:
            if patient['patient_id'] == patient_id:
                return patient
        return None
    
    def _find_by_health_card(self, health_card_number):
        """Find patient by health card number"""
        for patient in self.patients:
            if patient['health_card_number'] == health_card_number:
                return patient
        return None
    
    def get_all_patients(self):
        """Get all registered patients"""
        return self.patients
    
    def search_patients(self, query):
        """Search patients by name or health card number"""
        query = query.lower()
        results = []
        
        for patient in self.patients:
            if (query in patient['first_name'].lower() or
                query in patient['last_name'].lower() or
                query in patient['health_card_number'].lower()):
                results.append(patient)
        
        return results
    
    def update_patient(self, patient_id, updates):
        """Update patient information"""
        patient = self.get_patient(patient_id)
        if not patient:
            raise ValueError(f"Patient {patient_id} not found")
        
        # Don't allow changing patient_id or health_card_number
        protected_fields = ['patient_id', 'health_card_number', 'registered_at']
        
        for key, value in updates.items():
            if key not in protected_fields:
                patient[key] = value
        
        self._save_patients()
        return patient
