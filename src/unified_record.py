"""
Unified Record System
Implements OPOR principle: One comprehensive record per person
"""

import json
import os
from datetime import datetime


class UnifiedRecordSystem:
    """Manages unified clinical records for patients"""
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.records_file = os.path.join(data_dir, 'clinical_records.json')
        self.records = self._load_records()
    
    def _load_records(self):
        """Load clinical records from JSON file"""
        if os.path.exists(self.records_file):
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_records(self):
        """Save clinical records to JSON file"""
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, indent=2, ensure_ascii=False)
    
    def get_unified_record(self, patient_id):
        """
        Get unified record for a patient
        Returns all clinical data consolidated in one record
        """
        if patient_id not in self.records:
            return None
        
        record_data = self.records[patient_id]
        
        # Build unified record
        unified_record = {
            'patient_id': patient_id,
            'clinical_records': record_data.get('clinical_records', []),
            'medications': record_data.get('medications', []),
            'allergies': record_data.get('allergies', []),
            'immunizations': record_data.get('immunizations', []),
            'lab_results': record_data.get('lab_results', []),
            'last_updated': record_data.get('last_updated')
        }
        
        return unified_record
    
    def add_records(self, patient_id, records_data):
        """Add clinical records for a patient"""
        if patient_id not in self.records:
            self.records[patient_id] = {
                'clinical_records': [],
                'medications': [],
                'allergies': [],
                'immunizations': [],
                'lab_results': [],
                'last_updated': datetime.now().isoformat()
            }
        
        # Add clinical records
        if 'clinical_records' in records_data:
            self.records[patient_id]['clinical_records'].extend(
                records_data['clinical_records']
            )
        
        # Add medications
        if 'medications' in records_data:
            self.records[patient_id]['medications'].extend(
                records_data['medications']
            )
        
        # Add allergies
        if 'allergies' in records_data:
            self.records[patient_id]['allergies'].extend(
                records_data['allergies']
            )
        
        # Add immunizations
        if 'immunizations' in records_data:
            self.records[patient_id]['immunizations'].extend(
                records_data['immunizations']
            )
        
        # Add lab results
        if 'lab_results' in records_data:
            self.records[patient_id]['lab_results'].extend(
                records_data['lab_results']
            )
        
        self.records[patient_id]['last_updated'] = datetime.now().isoformat()
        self._save_records()
    
    def add_clinical_record(self, patient_id, record):
        """Add a single clinical record"""
        if patient_id not in self.records:
            self.records[patient_id] = {
                'clinical_records': [],
                'medications': [],
                'allergies': [],
                'immunizations': [],
                'lab_results': [],
                'last_updated': datetime.now().isoformat()
            }
        
        self.records[patient_id]['clinical_records'].append(record)
        self.records[patient_id]['last_updated'] = datetime.now().isoformat()
        self._save_records()
    
    def get_patient_timeline(self, patient_id):
        """Get chronological timeline of all patient events"""
        record = self.get_unified_record(patient_id)
        if not record:
            return []
        
        timeline = []
        
        # Add all events with timestamps
        for cr in record['clinical_records']:
            timeline.append({
                'type': 'clinical_record',
                'date': cr.get('visit_date'),
                'data': cr
            })
        
        for med in record['medications']:
            timeline.append({
                'type': 'medication',
                'date': med.get('prescribed_date'),
                'data': med
            })
        
        for lab in record['lab_results']:
            timeline.append({
                'type': 'lab_result',
                'date': lab.get('test_date'),
                'data': lab
            })
        
        # Sort by date
        timeline.sort(key=lambda x: x['date'], reverse=True)
        
        return timeline
