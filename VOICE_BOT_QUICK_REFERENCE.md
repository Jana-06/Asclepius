# Quick Reference - Voice Bot & File Picker Features

## What Was Added?

### 1. Voice Recording Feature
Patients can now record voice messages directly from their profile and upload them to Firebase Storage with metadata stored in the database.

### 2. PDF File Picker
Patients can select and upload medical documents (PDFs) from their device with confirmation dialogs and progress indicators.

---

## Files Modified/Created

### Backend Files

**Modified:**
- `backend/app/models/models.py` - Added `AudioRecording` model
- `backend/app/schemas/schemas.py` - Added `AudioRecordingCreate` and `AudioRecordingResponse` schemas
- `backend/app/api/v1/patients.py` - Added 5 new API endpoints for audio management

**What They Do:**
- Audio model stores: file metadata, duration, transcription, notes
- Schemas define request/response formats for API
- Endpoints handle upload, retrieval, deletion, and transcription update

### Frontend Files

**Created:**
- `lib/data/services/audio_recording_service.dart` - Service for audio recording/upload
- `lib/shared/widgets/audio_recorder_widget.dart` - UI dialog for recording
- `lib/shared/widgets/pdf_file_picker_widget.dart` - UI widget for PDF upload

**Modified:**
- `lib/features/patient/patient_profile_screen.dart` - Integrated new widgets
- `pubspec.yaml` - Added `record` and `audio_waveforms` packages

---

## Key API Endpoints

```
POST   /api/v1/patients/{patient_id}/audio-upload
GET    /api/v1/patients/{patient_id}/audio-recordings
GET    /api/v1/patients/{patient_id}/audio-recordings/{recording_id}
DELETE /api/v1/patients/{patient_id}/audio-recordings/{recording_id}
PUT    /api/v1/patients/{patient_id}/audio-recordings/{recording_id}/transcription
```

---

## Quick Start for Developers

### Setup Backend
```bash
# 1. Update database with new model
cd backend
alembic revision --autogenerate -m "Add AudioRecording"
alembic upgrade head

# 2. Restart backend
python run_local.py
```

### Setup Frontend
```bash
# 1. Get dependencies
flutter pub get

# 2. Build and run
flutter run
```

### Test Features
1. Navigate to Patient Profile
2. Click "Record Voice Message" to test audio
3. Click "Upload Medical Document (PDF)" to test file picker

---

## Component Communication Flow

```
Patient Profile Screen
├── Voice Recording Section
│   └── AudioRecorderWidget
│       └── AudioRecordingService
│           ├── record package (local recording)
│           ├── API call to backend
│           └── Firebase Storage upload
│
└── Medical Documents Section
    └── PDFFilePickerWidget
        └── MedicalDocumentService
            ├── file_picker package
            ├── API call to backend
            └── Firebase Storage upload
```

---

## Database Schema (AudioRecording)

```sql
CREATE TABLE audio_recordings (
    id VARCHAR(36) PRIMARY KEY,
    patient_id VARCHAR(128) NOT NULL FOREIGN KEY REFERENCES patients(id),
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) DEFAULT 'audio/wav',
    file_size INTEGER NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    duration_seconds INTEGER,
    transcription TEXT,
    notes TEXT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Firebase Storage Structure

```
audio_recordings/
├── patient_id_1/
│   ├── recording_timestamp_1.wav
│   ├── recording_timestamp_2.wav
│   └── ...
├── patient_id_2/
│   └── ...
```

---

## Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Permission denied | No microphone access | Request permission in app |
| File too large | Exceeds 50MB limit | Reduce recording length |
| Upload failed | Network issues | Check internet connection |
| Not found 404 | Patient ID incorrect | Verify patient exists |
| Firebase error | Storage not configured | Setup Firebase credentials |

---

## Testing Checklist

- [ ] Record audio for 30+ seconds
- [ ] Pause and resume recording
- [ ] Cancel recording (should delete temp file)
- [ ] Upload recording with notes
- [ ] Verify recording in list
- [ ] Delete recording from list
- [ ] Select PDF from file picker
- [ ] Confirm upload dialog
- [ ] Upload PDF successfully
- [ ] See PDF in documents list
- [ ] Delete PDF from list
- [ ] Test on iOS (microphone permissions)
- [ ] Test on Android (microphone permissions)

---

## Performance Notes

- Audio recordings are saved to temp directory before upload
- Files are deleted after successful upload
- Firebase Storage handles large files efficiently
- Maximum file size: 50MB (audio), 10MB (PDF)
- Metadata stored in both PostgreSQL and Firestore for redundancy

---

## Security Considerations

- All files uploaded to Firebase Storage (encrypted at rest)
- Audio/PDF files stored per patient (patient_id in path)
- API endpoints require patient authentication
- File type validation on backend
- File size limits prevent abuse
- Temporary files cleaned up after upload

---

## Future Enhancements

### High Priority
- [ ] Audio playback in profile
- [ ] Transcription via Google Speech-to-Text
- [ ] Document OCR for PDFs

### Medium Priority
- [ ] Audio compression before upload
- [ ] Batch delete operations
- [ ] Search documents by name
- [ ] Audio analytics

### Low Priority
- [ ] Voice command processing
- [ ] Audio effect filters
- [ ] Document annotation
- [ ] Advanced analytics dashboard

---

## Useful Commands

### Test Audio Upload
```bash
curl -X POST http://localhost:8000/api/v1/patients/{id}/audio-upload \
  -F "file=@test.wav" \
  -F "duration_seconds=30" \
  -F "notes=test"
```

### Get Patient's Recordings
```bash
curl http://localhost:8000/api/v1/patients/{id}/audio-recordings
```

### Rebuild Flutter
```bash
flutter clean
flutter pub get
flutter run
```

---

## Documentation Files

1. **VOICE_BOT_FILEPICKER_IMPLEMENTATION.md** - Detailed technical documentation
2. **SETUP_VOICE_BOT_FILEPICKER.md** - Complete setup instructions
3. **This file** - Quick reference guide

---

## Dependencies Added

```yaml
record: ^5.0.0              # Audio recording library
audio_waveforms: ^1.0.0     # Audio visualization (optional)
```

---

## File Locations Summary

```
Backend:
  - Models: backend/app/models/models.py (added AudioRecording class)
  - Schemas: backend/app/schemas/schemas.py (added AudioRecordingResponse)
  - Endpoints: backend/app/api/v1/patients.py (added 5 endpoints)

Frontend:
  - Service: lib/data/services/audio_recording_service.dart
  - Widgets: lib/shared/widgets/audio_recorder_widget.dart
  - Widgets: lib/shared/widgets/pdf_file_picker_widget.dart
  - Screen: lib/features/patient/patient_profile_screen.dart (modified)
  - Config: pubspec.yaml (modified)
```

---

## Contact & Support

For detailed questions, refer to:
1. VOICE_BOT_FILEPICKER_IMPLEMENTATION.md (technical details)
2. SETUP_VOICE_BOT_FILEPICKER.md (setup & troubleshooting)
3. Code comments in source files

