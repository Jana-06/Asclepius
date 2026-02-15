# Setup Instructions - Voice Bot & File Picker Features

## Summary of Changes

This implementation adds two major features to the patient profile:

1. **Voice Recording (Voice Bot)** - Records audio messages and stores them in Firebase
2. **PDF File Picker** - Allows patients to upload medical documents

---

## Backend Setup

### 1. Update Database Models
The `AudioRecording` model has been added to:
- **File:** `backend/app/models/models.py`
- Stores metadata for voice recordings (file path, duration, transcription, notes)

### 2. Update Database Schemas
The `AudioRecordingResponse` schema has been added to:
- **File:** `backend/app/schemas/schemas.py`
- Used for API responses

### 3. Add API Endpoints
New endpoints added to `backend/app/api/v1/patients.py`:
- `POST /{patient_id}/audio-upload` - Upload recording
- `GET /{patient_id}/audio-recordings` - List all recordings
- `GET /{patient_id}/audio-recordings/{recording_id}` - Get specific recording
- `DELETE /{patient_id}/audio-recordings/{recording_id}` - Delete recording
- `PUT /{patient_id}/audio-recordings/{recording_id}/transcription` - Update transcription

### 4. Database Migration (Optional)
To add the new AudioRecording table to your database:

```bash
cd backend
alembic revision --autogenerate -m "Add AudioRecording model for voice messages"
alembic upgrade head
```

### 5. Verify Imports
Ensure the backend `app/api/v1/patients.py` file has correct imports:
```python
from app.models import Patient, Gender, EHRDocument, AudioRecording
from app.schemas import PatientCreate, PatientResponse, MessageResponse, AudioRecordingResponse
```

---

## Frontend Setup

### 1. Add Dependencies
Update `pubspec.yaml` with new packages:

```yaml
dependencies:
  # ... existing dependencies ...
  
  # Audio recording
  record: ^5.0.0
  audio_waveforms: ^1.0.0
```

### 2. Install Packages
```bash
flutter pub get
```

### 3. Platform-Specific Configuration

#### Android Configuration
Add to `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

#### iOS Configuration
Add to `ios/Runner/Info.plist`:
```xml
<key>NSMicrophoneUsageDescription</key>
<string>We need access to your microphone to record health-related voice messages</string>
<key>NSLocalNetworkUsageDescription</key>
<string>We need access to your local network for healthcare services</string>
```

### 4. Create New Files
The following files have been created:

**Services:**
- `lib/data/services/audio_recording_service.dart` - Handle audio recording/upload logic

**Widgets:**
- `lib/shared/widgets/audio_recorder_widget.dart` - UI for recording dialog
- `lib/shared/widgets/pdf_file_picker_widget.dart` - UI for PDF upload

**Updated Files:**
- `lib/features/patient/patient_profile_screen.dart` - Integrated new features

---

## Testing the Features

### Test Voice Recording

1. **Start the app and navigate to patient profile**
2. **Click "Record Voice Message" button**
   - Dialog should appear with recording controls
3. **Tap the microphone icon to start**
   - Should see animated red circle
   - Duration should start counting up
4. **Test pause/resume**
   - Tap orange pause button
   - Duration should stop updating
   - Tap play button to resume
5. **Stop recording**
   - Tap red stop button
   - Recording should stop
   - Notes field should appear
6. **Add optional notes and upload**
   - Type some notes
   - Tap "Upload Recording"
   - Should see upload progress
   - Success message should appear
   - Dialog should close

### Test PDF Upload

1. **Click "Upload Medical Document (PDF)" button**
2. **Select a PDF file**
   - File picker dialog should open
   - Select a PDF from your device
3. **Confirm upload**
   - Confirmation dialog should appear
   - Confirm by tapping "Upload"
4. **Wait for upload**
   - Progress indicator should appear
   - Success message should show
5. **Verify document appears**
   - Document should appear in list below
   - Should show file name, date, and size
6. **Delete document** (Optional)
   - Tap delete icon (trash)
   - Confirm deletion
   - Document should disappear from list

---

## API Testing with cURL

### Upload Audio Recording
```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_id}/audio-upload \
  -F "file=@recording.wav" \
  -F "duration_seconds=30" \
  -F "notes=Test recording"
```

### Get All Recordings
```bash
curl http://localhost:8000/api/v1/patients/{patient_id}/audio-recordings
```

### Delete Recording
```bash
curl -X DELETE http://localhost:8000/api/v1/patients/{patient_id}/audio-recordings/{recording_id}
```

### Update Transcription
```bash
curl -X PUT http://localhost:8000/api/v1/patients/{patient_id}/audio-recordings/{recording_id}/transcription \
  -H "Content-Type: application/json" \
  -d '{"transcription": "Transcribed text here"}'
```

---

## Troubleshooting

### Issue: "Microphone permission denied"
**Solution:** 
- Android: Go to app settings > Permissions > Microphone, enable it
- iOS: Go to Settings > Privacy > Microphone, enable for the app

### Issue: "Failed to upload recording"
**Solution:**
- Check internet connection
- Verify backend API is running
- Check Firebase Storage is configured
- Check file size doesn't exceed 50MB

### Issue: Audio widget doesn't appear
**Solution:**
- Ensure `audio_recorder_widget.dart` is in correct location
- Verify imports are correct in patient profile screen
- Check for any Dart compilation errors

### Issue: PDF upload fails silently
**Solution:**
- Ensure file is valid PDF
- Check file size (max 10MB)
- Verify Firebase Storage credentials
- Check network connectivity

---

## File Structure

```
asclepius/
├── lib/
│   ├── data/
│   │   └── services/
│   │       ├── audio_recording_service.dart      [NEW]
│   │       ├── medical_document_service.dart     [EXISTING]
│   │       └── ...
│   ├── features/
│   │   └── patient/
│   │       └── patient_profile_screen.dart       [UPDATED]
│   └── shared/
│       └── widgets/
│           ├── audio_recorder_widget.dart        [NEW]
│           ├── pdf_file_picker_widget.dart       [NEW]
│           └── ...
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── models.py                         [UPDATED - AudioRecording]
│   │   ├── schemas/
│   │   │   └── schemas.py                        [UPDATED - AudioRecordingResponse]
│   │   └── api/
│   │       └── v1/
│   │           └── patients.py                   [UPDATED - audio endpoints]
│   └── ...
├── pubspec.yaml                                  [UPDATED - dependencies]
└── VOICE_BOT_FILEPICKER_IMPLEMENTATION.md        [NEW - detailed docs]
```

---

## Key Features

### Voice Recording
- ✅ Start/Stop/Pause/Resume recording
- ✅ Real-time duration display
- ✅ Optional notes before upload
- ✅ Upload to Firebase Storage
- ✅ Store metadata in database
- ✅ Delete recordings
- ✅ Support for WAV, MP3, M4A formats
- ✅ 50MB max file size

### PDF File Picker
- ✅ Select PDF files from device
- ✅ Upload confirmation dialog
- ✅ Progress indicator
- ✅ Upload to Firebase Storage
- ✅ Store metadata in database
- ✅ Display in documents list
- ✅ Delete documents
- ✅ 10MB max file size

---

## Next Steps

### Optional Enhancements
1. **Audio Transcription**
   - Integrate Google Cloud Speech-to-Text
   - Auto-transcribe recordings on upload

2. **Document OCR**
   - Extract text from PDFs
   - Enable document search

3. **Audio Playback**
   - Add playback widget
   - Volume controls

4. **Analytics**
   - Track recording duration
   - Monitor upload speeds
   - Document type statistics

---

## Support

For issues or questions:
1. Check the `VOICE_BOT_FILEPICKER_IMPLEMENTATION.md` for detailed documentation
2. Review error messages in console
3. Verify Firebase configuration
4. Check backend logs: `docker logs asclepius-backend` (if using Docker)

---

## Checklist for Deployment

- [ ] Backend models migrated (`alembic upgrade head`)
- [ ] Dependencies added to `pubspec.yaml`
- [ ] Android manifest updated with permissions
- [ ] iOS Info.plist updated with permissions
- [ ] Flutter packages installed (`flutter pub get`)
- [ ] All new files created in correct locations
- [ ] Firebase Storage configured and accessible
- [ ] Backend API endpoints tested
- [ ] Audio recording tested on device
- [ ] PDF upload tested on device
- [ ] Error handling verified

