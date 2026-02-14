/// API Configuration Constants
class ApiConstants {
  static const String baseUrl = 'https://asclepius-300388107814.europe-west1.run.app'; // Cloud Run public URL
  static const String apiVersion = '/api/v1';

  // Endpoints
  static const String patients = '$apiVersion/patients';
  static const String triage = '$apiVersion/triage';
  static const String hospitals = '$apiVersion/hospitals';
  static const String outbreak = '$apiVersion/outbreak';
  static const String admin = '$apiVersion/admin';

  // Timeout
  static const int connectionTimeout = 30000;
  static const int receiveTimeout = 30000;
}

/// Symptom Constants
class SymptomConstants {
  static const List<Map<String, dynamic>> symptoms = [
    // General
    {'code': 'fever', 'name': 'Fever', 'icon': '🌡️', 'category': 'general'},
    {'code': 'headache', 'name': 'Headache', 'icon': '🤕', 'category': 'general'},
    {'code': 'fatigue', 'name': 'Fatigue', 'icon': '😴', 'category': 'general'},
    {'code': 'body_ache', 'name': 'Body Ache', 'icon': '💪', 'category': 'general'},
    {'code': 'nausea', 'name': 'Nausea', 'icon': '🤢', 'category': 'general'},
    {'code': 'vomiting', 'name': 'Vomiting', 'icon': '🤮', 'category': 'general'},
    {'code': 'diarrhea', 'name': 'Diarrhea', 'icon': '🚽', 'category': 'gastro'},

    // Respiratory
    {'code': 'cough', 'name': 'Cough', 'icon': '😷', 'category': 'respiratory'},
    {'code': 'breathlessness', 'name': 'Breathlessness', 'icon': '😮‍💨', 'category': 'respiratory'},
    {'code': 'chest_congestion', 'name': 'Chest Congestion', 'icon': '🫁', 'category': 'respiratory'},
    {'code': 'sore_throat', 'name': 'Sore Throat', 'icon': '🗣️', 'category': 'respiratory'},
    {'code': 'runny_nose', 'name': 'Runny Nose', 'icon': '🤧', 'category': 'respiratory'},
    {'code': 'wheezing', 'name': 'Wheezing', 'icon': '🌬️', 'category': 'respiratory'},

    // Cardiac
    {'code': 'chest_pain', 'name': 'Chest Pain', 'icon': '💔', 'category': 'cardiac'},
    {'code': 'palpitations', 'name': 'Palpitations', 'icon': '💓', 'category': 'cardiac'},
    {'code': 'dizziness', 'name': 'Dizziness', 'icon': '😵', 'category': 'cardiac'},
    {'code': 'fainting', 'name': 'Fainting', 'icon': '😵‍💫', 'category': 'cardiac'},

    // Neurological
    {'code': 'confusion', 'name': 'Confusion', 'icon': '🤔', 'category': 'neuro'},
    {'code': 'seizures', 'name': 'Seizures', 'icon': '⚡', 'category': 'neuro'},
    {'code': 'numbness', 'name': 'Numbness', 'icon': '✋', 'category': 'neuro'},
    {'code': 'vision_changes', 'name': 'Vision Changes', 'icon': '👁️', 'category': 'neuro'},
    {'code': 'speech_difficulty', 'name': 'Speech Difficulty', 'icon': '🗣️', 'category': 'neuro'},

    // Abdominal
    {'code': 'abdominal_pain', 'name': 'Abdominal Pain', 'icon': '🤰', 'category': 'gastro'},
    {'code': 'bloating', 'name': 'Bloating', 'icon': '🎈', 'category': 'gastro'},
    {'code': 'loss_of_appetite', 'name': 'Loss of Appetite', 'icon': '🍽️', 'category': 'gastro'},

    // Skin
    {'code': 'rash', 'name': 'Rash', 'icon': '🔴', 'category': 'skin'},
    {'code': 'itching', 'name': 'Itching', 'icon': '🤚', 'category': 'skin'},

    // Musculoskeletal
    {'code': 'joint_pain', 'name': 'Joint Pain', 'icon': '🦴', 'category': 'musculo'},
    {'code': 'back_pain', 'name': 'Back Pain', 'icon': '🔙', 'category': 'musculo'},
    {'code': 'swelling', 'name': 'Swelling', 'icon': '🎈', 'category': 'musculo'},
  ];

  static List<String> get categories => [
    'general', 'respiratory', 'cardiac', 'neuro', 'gastro', 'skin', 'musculo'
  ];

  static String getCategoryName(String code) {
    const names = {
      'general': 'General',
      'respiratory': 'Respiratory',
      'cardiac': 'Cardiac',
      'neuro': 'Neurological',
      'gastro': 'Gastrointestinal',
      'skin': 'Skin',
      'musculo': 'Musculoskeletal',
    };
    return names[code] ?? code;
  }
}

/// Pre-existing Conditions
class ConditionConstants {
  static const List<String> conditions = [
    'Diabetes',
    'Hypertension',
    'Heart Disease',
    'Asthma',
    'COPD',
    'Kidney Disease',
    'Liver Disease',
    'Cancer',
    'HIV',
    'Tuberculosis',
    'Thyroid Disorder',
    'Anemia',
    'Obesity',
    'Arthritis',
    'Epilepsy',
  ];
}

/// Department Constants
class DepartmentConstants {
  static const List<Map<String, String>> departments = [
    {'code': 'general_medicine', 'name': 'General Medicine', 'icon': '🏥'},
    {'code': 'emergency', 'name': 'Emergency', 'icon': '🚨'},
    {'code': 'cardiology', 'name': 'Cardiology', 'icon': '❤️'},
    {'code': 'pulmonology', 'name': 'Pulmonology', 'icon': '🫁'},
    {'code': 'neurology', 'name': 'Neurology', 'icon': '🧠'},
    {'code': 'gastroenterology', 'name': 'Gastroenterology', 'icon': '🍽️'},
    {'code': 'orthopedics', 'name': 'Orthopedics', 'icon': '🦴'},
    {'code': 'surgery', 'name': 'Surgery', 'icon': '⚕️'},
    {'code': 'dermatology', 'name': 'Dermatology', 'icon': '🔬'},
    {'code': 'ent', 'name': 'ENT', 'icon': '👂'},
    {'code': 'ophthalmology', 'name': 'Ophthalmology', 'icon': '👁️'},
    {'code': 'urology', 'name': 'Urology', 'icon': '💧'},
    {'code': 'pediatrics', 'name': 'Pediatrics', 'icon': '👶'},
    {'code': 'obgyn', 'name': 'Obstetrics & Gynecology', 'icon': '🤰'},
  ];
}
