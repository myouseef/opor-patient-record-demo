// OPOR Patient Record Demo - Frontend JavaScript

class OPORApp {
    constructor() {
        this.patients = [];
        this.currentPatient = null;
        this.init();
    }

    init() {
        this.loadStats();
        this.loadPatients();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Search functionality
        document.getElementById('searchBtn').addEventListener('click', () => this.searchPatients());
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchPatients();
        });

        // Generate data button
        document.getElementById('generateDataBtn').addEventListener('click', () => this.generateData());

        // Modal close
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('patientModal').addEventListener('click', (e) => {
            if (e.target.id === 'patientModal') this.closeModal();
        });
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();

            if (data.success) {
                document.getElementById('totalPatients').textContent = data.stats.total_patients;
                document.getElementById('totalRecords').textContent = data.stats.total_records;
                document.getElementById('uniqueCards').textContent = data.stats.unique_health_cards;
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async loadPatients() {
        try {
            const response = await fetch('/api/patients');
            const data = await response.json();

            if (data.success) {
                this.patients = data.patients;
                this.displayPatients(this.patients);
            }
        } catch (error) {
            console.error('Error loading patients:', error);
            this.showEmptyState();
        }
    }

    async searchPatients() {
        const query = document.getElementById('searchInput').value.trim();

        if (!query) {
            this.displayPatients(this.patients);
            document.getElementById('resultsTitle').textContent = 'All Patients';
            return;
        }

        try {
            const response = await fetch(`/api/patients/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (data.success) {
                this.displayPatients(data.patients);
                document.getElementById('resultsTitle').textContent = `Search Results for "${query}"`;
            }
        } catch (error) {
            console.error('Error searching patients:', error);
        }
    }

    displayPatients(patients) {
        const grid = document.getElementById('patientsGrid');
        const emptyState = document.getElementById('emptyState');
        const resultsCount = document.getElementById('resultsCount');

        if (patients.length === 0) {
            this.showEmptyState();
            return;
        }

        emptyState.classList.remove('active');
        resultsCount.textContent = `${patients.length} patient${patients.length !== 1 ? 's' : ''}`;

        grid.innerHTML = patients.map(patient => this.createPatientCard(patient)).join('');

        // Add click listeners to cards
        document.querySelectorAll('.patient-card').forEach((card, index) => {
            card.addEventListener('click', () => this.showPatientDetails(patients[index]));
        });
    }

    createPatientCard(patient) {
        const initials = `${patient.first_name[0]}${patient.last_name[0]}`;
        const age = this.calculateAge(patient.date_of_birth);

        return `
            <div class="patient-card" data-patient-id="${patient.patient_id}">
                <div class="patient-header">
                    <div class="patient-avatar">${initials}</div>
                    <div class="patient-info">
                        <h4>${patient.first_name} ${patient.last_name}</h4>
                        <div class="patient-id">${patient.patient_id}</div>
                    </div>
                </div>
                <div class="patient-details">
                    <div class="detail-row">
                        <span class="detail-label">Health Card</span>
                        <span class="detail-value">${patient.health_card_number}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Age</span>
                        <span class="detail-value">${age} years</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Gender</span>
                        <span class="detail-value">${patient.gender}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Phone</span>
                        <span class="detail-value">${patient.phone}</span>
                    </div>
                </div>
            </div>
        `;
    }

    async showPatientDetails(patient) {
        this.currentPatient = patient;

        try {
            const response = await fetch(`/api/records/${patient.patient_id}`);
            const data = await response.json();

            if (data.success) {
                this.displayPatientModal(patient, data.record);
            }
        } catch (error) {
            console.error('Error loading patient records:', error);
        }
    }

    displayPatientModal(patient, record) {
        const modal = document.getElementById('patientModal');
        const modalBody = document.getElementById('modalBody');
        const modalTitle = document.getElementById('modalPatientName');

        modalTitle.textContent = `${patient.first_name} ${patient.last_name}`;

        let html = `
            <div class="info-section">
                <h3>📋 Patient Information</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <label>Patient ID</label>
                        <value>${patient.patient_id}</value>
                    </div>
                    <div class="info-item">
                        <label>Health Card</label>
                        <value>${patient.health_card_number}</value>
                    </div>
                    <div class="info-item">
                        <label>Date of Birth</label>
                        <value>${patient.date_of_birth}</value>
                    </div>
                    <div class="info-item">
                        <label>Gender</label>
                        <value>${patient.gender}</value>
                    </div>
                    <div class="info-item">
                        <label>Phone</label>
                        <value>${patient.phone}</value>
                    </div>
                    <div class="info-item">
                        <label>Email</label>
                        <value>${patient.email}</value>
                    </div>
                </div>
                <div class="info-item" style="margin-top: 1rem;">
                    <label>Address</label>
                    <value>${patient.address}</value>
                </div>
            </div>
        `;

        // Allergies
        if (record.allergies && record.allergies.length > 0) {
            html += `
                <div class="info-section">
                    <h3>⚠️ Allergies</h3>
                    <div class="info-grid">
                        ${record.allergies.map(allergy => `
                            <div class="info-item">
                                <label>${allergy.allergen}</label>
                                <value><span class="badge badge-warning">${allergy.severity}</span></value>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        // Medications
        if (record.medications && record.medications.length > 0) {
            html += `
                <div class="info-section">
                    <h3>💊 Current Medications</h3>
                    ${record.medications.map(med => `
                        <div class="record-item">
                            <div class="record-header">
                                <div>
                                    <strong>${med.name}</strong>
                                    <div class="record-date">Prescribed: ${new Date(med.prescribed_date).toLocaleDateString()}</div>
                                </div>
                                <span class="badge badge-primary">Active</span>
                            </div>
                            <div>Prescriber: ${med.prescriber}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        // Immunizations
        if (record.immunizations && record.immunizations.length > 0) {
            html += `
                <div class="info-section">
                    <h3>💉 Immunizations</h3>
                    <div class="info-grid">
                        ${record.immunizations.map(imm => `
                            <div class="info-item">
                                <label>${imm.vaccine}</label>
                                <value>${new Date(imm.date).toLocaleDateString()}</value>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        // Clinical Records
        if (record.clinical_records && record.clinical_records.length > 0) {
            html += `
                <div class="info-section">
                    <h3>🏥 Clinical Records</h3>
                    ${record.clinical_records.map(cr => `
                        <div class="record-item">
                            <div class="record-header">
                                <div>
                                    <strong>${cr.facility}</strong>
                                    <div class="record-date">${new Date(cr.visit_date).toLocaleDateString()}</div>
                                </div>
                                <span class="badge badge-success">${cr.specialty}</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <strong>Provider:</strong> ${cr.provider}<br>
                                <strong>Chief Complaint:</strong> ${cr.chief_complaint}<br>
                                <strong>Diagnosis:</strong> ${cr.diagnosis}
                            </div>
                            <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid var(--card-border);">
                                <strong>Vital Signs:</strong><br>
                                BP: ${cr.vital_signs.blood_pressure} | 
                                HR: ${cr.vital_signs.heart_rate} bpm | 
                                Temp: ${cr.vital_signs.temperature}°C
                            </div>
                            <div style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-muted);">
                                ${cr.notes}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        // Lab Results
        if (record.lab_results && record.lab_results.length > 0) {
            html += `
                <div class="info-section">
                    <h3>🔬 Lab Results</h3>
                    ${record.lab_results.map(lab => `
                        <div class="record-item">
                            <div class="record-header">
                                <div>
                                    <strong>${lab.test_name}</strong>
                                    <div class="record-date">${new Date(lab.test_date).toLocaleDateString()}</div>
                                </div>
                                <span class="badge badge-success">${lab.result}</span>
                            </div>
                            <div>Facility: ${lab.facility}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        modalBody.innerHTML = html;
        modal.classList.add('active');
    }

    closeModal() {
        document.getElementById('patientModal').classList.remove('active');
    }

    async generateData() {
        const btn = document.getElementById('generateDataBtn');
        const originalText = btn.innerHTML;

        btn.innerHTML = '<span class="loading"></span> Generating...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/generate-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ count: 10 })
            });

            const data = await response.json();

            if (data.success) {
                await this.loadStats();
                await this.loadPatients();
                this.showNotification('✅ Successfully generated 10 patients with clinical records!');
            }
        } catch (error) {
            console.error('Error generating data:', error);
            this.showNotification('❌ Error generating data. Please try again.');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    showEmptyState() {
        document.getElementById('patientsGrid').innerHTML = '';
        document.getElementById('emptyState').classList.add('active');
        document.getElementById('resultsCount').textContent = '0 patients';
    }

    calculateAge(dateOfBirth) {
        const today = new Date();
        const birthDate = new Date(dateOfBirth);
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        return age;
    }

    showNotification(message) {
        // Simple notification - could be enhanced with a toast library
        alert(message);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new OPORApp();
});
