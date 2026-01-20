"""
OPOR Patient Record Demo - Flask Application
One Person One Record (OPOR) demonstration system
"""

from flask import Flask, render_template, jsonify, request
from src.patient_identity import PatientIdentityManager
from src.unified_record import UnifiedRecordSystem
from src.data_generator import DataGenerator
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'opor-demo-secret-key-2026'

# Initialize data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize systems
patient_manager = PatientIdentityManager(DATA_DIR)
record_system = UnifiedRecordSystem(DATA_DIR)
data_generator = DataGenerator()


@app.route('/')
def index():
    """Dashboard homepage"""
    return render_template('index.html')


@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    patients = patient_manager.get_all_patients()
    return jsonify({
        'success': True,
        'count': len(patients),
        'patients': patients
    })


@app.route('/api/patients/search', methods=['GET'])
def search_patients():
    """Search patients by name or health card number"""
    query = request.args.get('q', '')
    patients = patient_manager.search_patients(query)
    return jsonify({
        'success': True,
        'count': len(patients),
        'patients': patients
    })


@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID"""
    patient = patient_manager.get_patient(patient_id)
    if patient:
        return jsonify({
            'success': True,
            'patient': patient
        })
    return jsonify({
        'success': False,
        'error': 'Patient not found'
    }), 404


@app.route('/api/records/<patient_id>', methods=['GET'])
def get_unified_record(patient_id):
    """Get unified record for a patient"""
    record = record_system.get_unified_record(patient_id)
    if record:
        return jsonify({
            'success': True,
            'record': record
        })
    return jsonify({
        'success': False,
        'error': 'Record not found'
    }), 404


@app.route('/api/generate-data', methods=['POST'])
def generate_sample_data():
    """Generate sample patient data"""
    count = request.json.get('count', 10)
    
    # Generate patients
    patients = []
    for _ in range(count):
        patient_data = data_generator.generate_patient()
        patient_id = patient_manager.register_patient(patient_data)
        
        # Generate clinical records
        records = data_generator.generate_clinical_records(patient_id)
        record_system.add_records(patient_id, records)
        
        patients.append(patient_id)
    
    return jsonify({
        'success': True,
        'message': f'Generated {count} patients with clinical records',
        'patient_ids': patients
    })


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    patients = patient_manager.get_all_patients()
    total_records = sum(
        len(record_system.get_unified_record(p['patient_id'])['clinical_records'])
        for p in patients
        if record_system.get_unified_record(p['patient_id'])
    )
    
    return jsonify({
        'success': True,
        'stats': {
            'total_patients': len(patients),
            'total_records': total_records,
            'unique_health_cards': len(set(p['health_card_number'] for p in patients))
        }
    })


if __name__ == '__main__':
    print("=" * 60)
    print("OPOR Patient Record Demo System")
    print("=" * 60)
    print("Starting Flask application on http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
