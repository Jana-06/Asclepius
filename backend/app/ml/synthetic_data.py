"""
Synthetic Patient Data Generator for SwasthyaFlow AI
Generates realistic healthcare data for training and testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import json
import random
from typing import List, Dict, Tuple
import uuid

fake = Faker('en_IN')  # Indian locale

# Medical Constants
SYMPTOMS = {
    # General
    "fever": {"weight": 0.3, "departments": ["General Medicine", "Emergency"]},
    "headache": {"weight": 0.2, "departments": ["General Medicine", "Neurology"]},
    "fatigue": {"weight": 0.2, "departments": ["General Medicine"]},
    "body_ache": {"weight": 0.2, "departments": ["General Medicine", "Orthopedics"]},
    "nausea": {"weight": 0.2, "departments": ["General Medicine", "Gastroenterology"]},
    "vomiting": {"weight": 0.3, "departments": ["General Medicine", "Gastroenterology", "Emergency"]},
    "diarrhea": {"weight": 0.3, "departments": ["General Medicine", "Gastroenterology"]},

    # Respiratory
    "cough": {"weight": 0.3, "departments": ["General Medicine", "Pulmonology"]},
    "breathlessness": {"weight": 0.7, "departments": ["Emergency", "Pulmonology", "Cardiology"]},
    "chest_congestion": {"weight": 0.3, "departments": ["Pulmonology", "General Medicine"]},
    "sore_throat": {"weight": 0.2, "departments": ["ENT", "General Medicine"]},
    "runny_nose": {"weight": 0.1, "departments": ["ENT", "General Medicine"]},
    "wheezing": {"weight": 0.5, "departments": ["Pulmonology", "Emergency"]},

    # Cardiac
    "chest_pain": {"weight": 0.9, "departments": ["Emergency", "Cardiology"]},
    "palpitations": {"weight": 0.5, "departments": ["Cardiology", "General Medicine"]},
    "dizziness": {"weight": 0.4, "departments": ["General Medicine", "Cardiology", "Neurology"]},
    "fainting": {"weight": 0.8, "departments": ["Emergency", "Cardiology", "Neurology"]},

    # Neurological
    "confusion": {"weight": 0.7, "departments": ["Emergency", "Neurology"]},
    "seizures": {"weight": 0.9, "departments": ["Emergency", "Neurology"]},
    "numbness": {"weight": 0.4, "departments": ["Neurology", "General Medicine"]},
    "vision_changes": {"weight": 0.5, "departments": ["Ophthalmology", "Neurology", "Emergency"]},
    "speech_difficulty": {"weight": 0.8, "departments": ["Emergency", "Neurology"]},

    # Abdominal
    "abdominal_pain": {"weight": 0.4, "departments": ["General Medicine", "Gastroenterology", "Surgery"]},
    "bloating": {"weight": 0.2, "departments": ["Gastroenterology", "General Medicine"]},
    "loss_of_appetite": {"weight": 0.2, "departments": ["General Medicine", "Gastroenterology"]},
    "blood_in_stool": {"weight": 0.7, "departments": ["Emergency", "Gastroenterology", "Surgery"]},

    # Skin
    "rash": {"weight": 0.3, "departments": ["Dermatology", "General Medicine"]},
    "itching": {"weight": 0.2, "departments": ["Dermatology", "General Medicine"]},
    "skin_lesions": {"weight": 0.3, "departments": ["Dermatology"]},

    # Urinary
    "frequent_urination": {"weight": 0.2, "departments": ["Urology", "General Medicine"]},
    "painful_urination": {"weight": 0.3, "departments": ["Urology", "General Medicine"]},
    "blood_in_urine": {"weight": 0.6, "departments": ["Urology", "Emergency"]},

    # Musculoskeletal
    "joint_pain": {"weight": 0.3, "departments": ["Orthopedics", "Rheumatology"]},
    "back_pain": {"weight": 0.3, "departments": ["Orthopedics", "General Medicine"]},
    "swelling": {"weight": 0.3, "departments": ["General Medicine", "Orthopedics"]},
}

PRE_EXISTING_CONDITIONS = [
    "diabetes", "hypertension", "heart_disease", "asthma", "copd",
    "kidney_disease", "liver_disease", "cancer", "hiv", "tuberculosis",
    "thyroid_disorder", "anemia", "obesity", "arthritis", "epilepsy"
]

DEPARTMENTS = [
    "General Medicine", "Emergency", "Cardiology", "Pulmonology",
    "Neurology", "Gastroenterology", "Orthopedics", "Surgery",
    "Dermatology", "ENT", "Ophthalmology", "Urology", "Rheumatology",
    "Pediatrics", "Obstetrics & Gynecology", "Psychiatry"
]

INDIAN_STATES = [
    "Delhi", "Maharashtra", "Karnataka", "Tamil Nadu", "Kerala",
    "West Bengal", "Gujarat", "Rajasthan", "Uttar Pradesh", "Bihar"
]

DISTRICTS_BY_STATE = {
    "Delhi": ["North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
    "Karnataka": ["Bengaluru Urban", "Mysuru", "Mangaluru", "Hubli", "Belgaum"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
}


class SyntheticDataGenerator:
    """Generate synthetic patient data for ML training"""

    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        Faker.seed(seed)

    def generate_vitals(self, risk_level: str, age: int, conditions: List[str]) -> Dict:
        """Generate realistic vital signs based on risk level"""

        # Base vitals
        if risk_level == "LOW":
            bp_sys = np.random.normal(120, 10)
            bp_dia = np.random.normal(80, 5)
            hr = np.random.normal(72, 8)
            temp = np.random.normal(98.6, 0.3)
            spo2 = np.random.normal(98, 1)
        elif risk_level == "MEDIUM":
            bp_sys = np.random.normal(135, 15)
            bp_dia = np.random.normal(88, 8)
            hr = np.random.normal(85, 12)
            temp = np.random.normal(99.5, 0.8)
            spo2 = np.random.normal(95, 2)
        else:  # HIGH
            bp_sys = np.random.normal(155, 20)
            bp_dia = np.random.normal(95, 10)
            hr = np.random.normal(100, 15)
            temp = np.random.normal(101, 1.2)
            spo2 = np.random.normal(90, 4)

        # Age adjustments
        if age > 65:
            bp_sys += 10
            bp_dia += 5

        # Condition adjustments
        if "hypertension" in conditions:
            bp_sys += 15
            bp_dia += 10
        if "heart_disease" in conditions:
            hr += 10
        if "copd" in conditions or "asthma" in conditions:
            spo2 -= 3

        return {
            "bp_systolic": int(np.clip(bp_sys, 80, 220)),
            "bp_diastolic": int(np.clip(bp_dia, 50, 130)),
            "heart_rate": int(np.clip(hr, 40, 180)),
            "temperature": round(np.clip(temp, 95, 106), 1),
            "spo2": int(np.clip(spo2, 60, 100)),
            "respiratory_rate": int(np.clip(np.random.normal(16, 4), 8, 40))
        }

    def determine_risk_and_department(self, symptoms: List[str], vitals: Dict,
                                       age: int, conditions: List[str]) -> Tuple[str, str]:
        """Determine risk level and recommended department"""

        # Calculate symptom severity score
        severity_score = sum(SYMPTOMS.get(s, {}).get("weight", 0.1) for s in symptoms)

        # Vital sign risk factors
        vital_risk = 0
        if vitals["bp_systolic"] > 160 or vitals["bp_systolic"] < 90:
            vital_risk += 0.3
        if vitals["heart_rate"] > 100 or vitals["heart_rate"] < 50:
            vital_risk += 0.2
        if vitals["temperature"] > 102:
            vital_risk += 0.2
        if vitals["spo2"] < 92:
            vital_risk += 0.4

        # Age risk factor
        age_risk = 0.2 if age > 65 or age < 5 else 0

        # Pre-existing condition risk
        condition_risk = len(conditions) * 0.1

        # Total risk score
        total_risk = severity_score + vital_risk + age_risk + condition_risk

        # Determine risk level
        if total_risk >= 1.5 or any(s in symptoms for s in ["chest_pain", "seizures", "fainting", "speech_difficulty"]):
            risk_level = "HIGH"
        elif total_risk >= 0.8:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Determine department
        dept_scores = {}
        for symptom in symptoms:
            for dept in SYMPTOMS.get(symptom, {}).get("departments", ["General Medicine"]):
                dept_scores[dept] = dept_scores.get(dept, 0) + SYMPTOMS[symptom]["weight"]

        if risk_level == "HIGH":
            department = "Emergency"
        elif dept_scores:
            department = max(dept_scores, key=dept_scores.get)
        else:
            department = "General Medicine"

        return risk_level, department

    def generate_outbreak_cluster(self, region: str, cluster_type: str,
                                   size: int, base_date: datetime) -> List[Dict]:
        """Generate synthetic outbreak cluster data"""

        cluster_symptoms = {
            "dengue": ["fever", "headache", "body_ache", "rash", "fatigue", "joint_pain"],
            "respiratory": ["fever", "cough", "breathlessness", "sore_throat", "fatigue"],
            "gastro": ["diarrhea", "vomiting", "abdominal_pain", "fever", "nausea"],
        }

        records = []
        symptoms_pool = cluster_symptoms.get(cluster_type, cluster_symptoms["respiratory"])

        for i in range(size):
            # Cluster cases appear close in time
            case_date = base_date + timedelta(hours=np.random.exponential(12))

            # Select symptoms with high overlap
            num_symptoms = random.randint(3, 5)
            selected_symptoms = random.sample(symptoms_pool, min(num_symptoms, len(symptoms_pool)))

            # Add some random symptoms
            if random.random() < 0.3:
                extra = random.choice([s for s in SYMPTOMS if s not in symptoms_pool])
                selected_symptoms.append(extra)

            records.append({
                "symptoms": selected_symptoms,
                "region": region,
                "timestamp": case_date,
                "cluster_type": cluster_type
            })

        return records

    def generate_dataset(self, n_records: int = 10000,
                         include_outbreaks: bool = True,
                         outbreak_percentage: float = 0.05) -> pd.DataFrame:
        """Generate complete synthetic dataset"""

        records = []

        # Calculate outbreak records
        n_outbreak = int(n_records * outbreak_percentage) if include_outbreaks else 0
        n_regular = n_records - n_outbreak

        # Generate regular records
        for _ in range(n_regular):
            # Demographics
            age = int(np.clip(np.random.lognormal(3.5, 0.5), 1, 100))
            gender = random.choices(["M", "F", "OTHER"], weights=[0.48, 0.48, 0.04])[0]
            state = random.choice(INDIAN_STATES)
            district = random.choice(DISTRICTS_BY_STATE.get(state, [f"{state}_District"]))

            # Pre-existing conditions (more likely with age)
            n_conditions = np.random.poisson(0.5 + age/50)
            conditions = random.sample(PRE_EXISTING_CONDITIONS, min(n_conditions, 5))

            # Symptoms
            n_symptoms = random.randint(1, 6)
            symptoms = random.sample(list(SYMPTOMS.keys()), n_symptoms)

            # Risk and department
            vitals = self.generate_vitals("MEDIUM", age, conditions)  # Initial guess
            risk_level, department = self.determine_risk_and_department(
                symptoms, vitals, age, conditions
            )

            # Regenerate vitals based on actual risk
            vitals = self.generate_vitals(risk_level, age, conditions)

            # Timestamp (last 6 months)
            timestamp = datetime.now() - timedelta(days=random.randint(0, 180))

            records.append({
                "patient_id": str(uuid.uuid4()),
                "age": age,
                "gender": gender,
                "state": state,
                "district": district,
                "symptoms": json.dumps(symptoms),
                "pre_existing_conditions": json.dumps(conditions),
                "bp_systolic": vitals["bp_systolic"],
                "bp_diastolic": vitals["bp_diastolic"],
                "heart_rate": vitals["heart_rate"],
                "temperature": vitals["temperature"],
                "spo2": vitals["spo2"],
                "respiratory_rate": vitals["respiratory_rate"],
                "risk_level": risk_level,
                "department": department,
                "timestamp": timestamp.isoformat(),
                "is_outbreak_case": False
            })

        # Generate outbreak clusters
        if include_outbreaks and n_outbreak > 0:
            cluster_types = ["dengue", "respiratory", "gastro"]
            regions = ["Delhi_North", "Mumbai", "Chennai", "Bengaluru Urban", "Kolkata"]

            remaining = n_outbreak
            while remaining > 0:
                cluster_size = min(remaining, random.randint(10, 50))
                cluster_type = random.choice(cluster_types)
                region = random.choice(regions)
                base_date = datetime.now() - timedelta(days=random.randint(0, 60))

                cluster_records = self.generate_outbreak_cluster(
                    region, cluster_type, cluster_size, base_date
                )

                for cr in cluster_records:
                    age = int(np.clip(np.random.normal(35, 15), 5, 80))
                    gender = random.choice(["M", "F"])
                    conditions = random.sample(PRE_EXISTING_CONDITIONS, random.randint(0, 2))
                    vitals = self.generate_vitals("MEDIUM", age, conditions)
                    risk_level, department = self.determine_risk_and_department(
                        cr["symptoms"], vitals, age, conditions
                    )

                    records.append({
                        "patient_id": str(uuid.uuid4()),
                        "age": age,
                        "gender": gender,
                        "state": region.split("_")[0] if "_" in region else region,
                        "district": region,
                        "symptoms": json.dumps(cr["symptoms"]),
                        "pre_existing_conditions": json.dumps(conditions),
                        "bp_systolic": vitals["bp_systolic"],
                        "bp_diastolic": vitals["bp_diastolic"],
                        "heart_rate": vitals["heart_rate"],
                        "temperature": vitals["temperature"],
                        "spo2": vitals["spo2"],
                        "respiratory_rate": vitals["respiratory_rate"],
                        "risk_level": risk_level,
                        "department": department,
                        "timestamp": cr["timestamp"].isoformat(),
                        "is_outbreak_case": True,
                        "outbreak_type": cr["cluster_type"]
                    })

                remaining -= cluster_size

        df = pd.DataFrame(records)
        return df.sample(frac=1).reset_index(drop=True)  # Shuffle

    def generate_hospital_data(self, n_hospitals: int = 50) -> pd.DataFrame:
        """Generate synthetic hospital data"""

        hospital_types = ["PHC", "CHC", "District Hospital", "Tertiary Care"]

        records = []
        for i in range(n_hospitals):
            state = random.choice(INDIAN_STATES)
            district = random.choice(DISTRICTS_BY_STATE.get(state, [f"{state}_District"]))
            h_type = random.choice(hospital_types)

            # Beds based on hospital type
            bed_ranges = {"PHC": (10, 30), "CHC": (30, 100),
                         "District Hospital": (100, 500), "Tertiary Care": (500, 2000)}
            min_beds, max_beds = bed_ranges[h_type]
            total_beds = random.randint(min_beds, max_beds)

            # Departments based on hospital type
            if h_type == "PHC":
                depts = ["General Medicine", "Emergency"]
            elif h_type == "CHC":
                depts = random.sample(DEPARTMENTS[:8], random.randint(4, 6))
            else:
                depts = random.sample(DEPARTMENTS, random.randint(8, len(DEPARTMENTS)))

            records.append({
                "id": str(uuid.uuid4()),
                "name": f"{district} {h_type} {i+1}",
                "code": f"{state[:2].upper()}{district[:3].upper()}{i+1:03d}",
                "hospital_type": h_type,
                "state": state,
                "district": district,
                "total_beds": total_beds,
                "emergency_beds": int(total_beds * 0.1),
                "departments": json.dumps(depts),
                "latitude": round(random.uniform(8.0, 35.0), 6),
                "longitude": round(random.uniform(68.0, 97.0), 6),
                "is_active": True
            })

        return pd.DataFrame(records)


def main():
    """Generate and save synthetic datasets"""
    generator = SyntheticDataGenerator(seed=42)

    # Generate patient data
    print("Generating patient dataset...")
    patient_df = generator.generate_dataset(n_records=10000, include_outbreaks=True)
    patient_df.to_csv("data/synthetic/synthetic_patients.csv", index=False)
    print(f"Generated {len(patient_df)} patient records")
    print(f"Risk distribution:\n{patient_df['risk_level'].value_counts()}")

    # Generate hospital data
    print("\nGenerating hospital dataset...")
    hospital_df = generator.generate_hospital_data(n_hospitals=100)
    hospital_df.to_csv("data/synthetic/synthetic_hospitals.csv", index=False)
    print(f"Generated {len(hospital_df)} hospital records")

    print("\nDatasets saved to data/synthetic/")


if __name__ == "__main__":
    main()

