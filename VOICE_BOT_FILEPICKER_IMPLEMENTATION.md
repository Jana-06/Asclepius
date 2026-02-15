# Voice Bot & File Picker Implementation Guide

## Overview
This document describes the implementation of voice recording and PDF file picker features for the patient profile in the Asclepius healthcare application.

## Features Added

### 1. **Voice Recording (Voice Bot)**
- Patients can record audio messages directly from their profile
- Audio files are stored in Firebase Storage
- Recording metadata is saved in both PostgreSQL database and Firestore
- Supports pause/resume functionality
- Records duration automatically
- Optional notes can be added to recordings

### 2. **PDF File Picker**
- Allows patients to upload medical documents (PDFs)
- Files are stored in Firebase Storage
- Metadata is synchronized with Firestore
- User-friendly confirmation dialog before upload
- Shows upload progress indicator

---

## Backend Implementation

### Database Models

#### AudioRecording Model
```python
class AudioRecording(Base):
    """Patient voice recording metadata"""
    __tablename__ = "audio_recordings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    patient_id = Column(String(128), ForeignKey("patients.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(20), default="audio/wav")
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String(500), nullable=False)
    duration_seconds = Column(Integer, nullable=True)
    transcription = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
```

### API Endpoints

#### Audio Recording Endpoints

1. **Upload Audio Recording**
   ```
   POST /api/v1/patients/{patient_id}/audio-upload
   ```
   - Parameters:
     - `file`: Audio file (WAV, MP3, M4A)
     - `duration_seconds`: Optional duration
     - `notes`: Optional notes about recording
   - Returns: `AudioRecordingResponse`

2. **Get All Audio Recordings**
   ```
   GET /api/v1/patients/{patient_id}/audio-recordings
   ```
   - Returns: List of `AudioRecordingResponse`

3. **Get Specific Recording**
   ```
   GET /api/v1/patients/{patient_id}/audio-recordings/{recording_id}
   ```
   - Returns: `AudioRecordingResponse`

4. **Delete Recording**
   ```
   DELETE /api/v1/patients/{patient_id}/audio-recordings/{recording_id}
   ```
   - Returns: `MessageResponse`

5. **Update Transcription**
   ```
   PUT /api/v1/patients/{patient_id}/audio-recordings/{recording_id}/transcription
   ```
   - Body: `{"transcription": "transcribed text"}`
   - Returns: `MessageResponse`

### Schema (Pydantic)

```python
class AudioRecordingCreate(BaseModel):
    file_name: str
    duration_seconds: Optional[int] = None
    notes: Optional[str] = None

class AudioRecordingResponse(BaseModel):
    id: str
    patient_id: str
    file_name: str
    file_type: str
    file_size: int
    duration_seconds: Optional[int]
    storage_path: str
    transcription: Optional[str] = None
    notes: Optional[str] = None
    recorded_at: datetime
```

---

## Frontend Implementation

### New Dependencies Added

Add to `pubspec.yaml`:
```yaml
  # Audio recording
  record: ^5.0.0
  audio_waveforms: ^1.0.0
```

### Services

#### AudioRecordingService
**Location:** `lib/data/services/audio_recording_service.dart`

Key Methods:
- `startRecording()` - Start audio recording
- `stopRecording()` - Stop and return file path
- `pauseRecording()` - Pause recording
- `resumeRecording()` - Resume recording
- `cancelRecording()` - Cancel and delete temporary file
- `uploadAudioRecording()` - Upload to backend
- `getAudioRecordings()` - Fetch patient's recordings
- `deleteAudioRecording()` - Delete specific recording
- `updateTranscription()` - Update transcription

### Widgets

#### 1. AudioRecorderWidget
**Location:** `lib/shared/widgets/audio_recorder_widget.dart`

Features:
- Dialog-based recording interface
- Real-time duration display
- Animated recording indicator (pulsing red dot)
- Play/Pause/Stop/Cancel controls
- Optional notes field before upload
- Upload functionality with progress indication

```dart
showDialog(
  context: context,
  builder: (context) => AudioRecorderWidget(
    patientId: patientId,
    onRecordingComplete: (filePath, duration) {
      // Handle completion
    },
    onRecordingCancelled: () {
      // Handle cancellation
    },
  ),
);
```

#### 2. PDFFilePickerWidget
**Location:** `lib/shared/widgets/pdf_file_picker_widget.dart`

Features:
- File picker for PDF documents
- Confirmation dialog before upload
- Upload progress indicator
- Success/error feedback via SnackBar
- Callback on upload completion

```dart
PDFFilePickerWidget(
  patientId: patientId,
  onUploadComplete: () {
    // Refresh documents list
  },
  onError: () {
    // Handle error
  },
)
```

### Updated Screens

#### PatientProfileScreen
**Location:** `lib/features/patient/patient_profile_screen.dart`

Changes:
1. Added imports for new services and widgets
2. Integrated `AudioRecorderWidget` for voice recording
3. Integrated `PDFFilePickerWidget` for document upload
4. Added `dispose()` method for audio service cleanup
5. Organized UI sections:
   - Patient Info Card
   - Voice Recording Section (NEW)
   - Medical Documents Section (UPDATED)

---

## Firebase Integration

### Storage Structure

```
firebase-storage/
├── audio_recordings/
│   └── {patient_id}/
│       ├── recording_1707986400000.wav
│       └── recording_1707986500000.wav
└── ehr_documents/
    └── {patient_id}/
        ├── report_1707986300000.pdf
        └── report_1707986400000.pdf
```

### Firestore Structure

```
patients/
├── {patient_id}/
│   ├── audio_recordings/
│   │   └── {recording_id}
│   │       ├── file_name: string
│   │       ├── file_type: string
│   │       ├── file_size: number
│   │       ├── duration_seconds: number
│   │       ├── storage_path: string
│   │       ├── notes: string
│   │       ├── transcription: string
│   │       └── recorded_at: timestamp
│   └── ehr_documents/
│       └── {document_id}
│           ├── file_name: string
│           ├── file_type: string
│           ├── file_size: number
│           ├── storage_path: string
│           └── uploaded_at: timestamp
```

---

## Usage Instructions

### For Patients

#### Recording Voice Message
1. Go to Patient Profile
2. Tap "Record Voice Message" button
3. In the dialog:
   - Tap the microphone icon to start recording
   - Tap pause (orange) to pause recording
   - Tap resume (play) to continue
   - Tap stop (red) to finish recording
4. (Optional) Add notes about the recording
5. Tap "Upload Recording" to submit

#### Uploading Medical Documents
1. Go to Patient Profile
2. Under "Medical Documents" section
3. Tap "Upload Medical Document (PDF)"
4. Select a PDF file from your device
5. Confirm the upload
6. Wait for upload to complete
7. Document appears in the list below

---

## Technical Details

### Audio File Formats Supported
- WAV (audio/wav)
- MP3 (audio/mpeg)
- M4A (audio/m4a)

### File Size Limits
- Audio recordings: 50MB max
- PDF documents: 10MB max

### Permissions Required

**Android** (`android/app/src/main/AndroidManifest.xml`):
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

**iOS** (`ios/Runner/Info.plist`):
```xml
<key>NSMicrophoneUsageDescription</key>
<string>This app needs microphone access to record voice messages</string>
```

---

## Error Handling

### Common Issues & Solutions

1. **Microphone Permission Denied**
   - User must grant microphone permission in device settings
   - App displays alert: "Microphone permission denied"

2. **File Too Large**
   - Audio: 50MB limit for recordings
   - PDF: 10MB limit for documents
   - App displays: "File size exceeds limit"

3. **Network Issues**
   - Automatic retry mechanisms in place
   - User sees error message with retry option

4. **Firebase Storage Not Available**
   - Ensure Firebase is properly configured
   - Check Firebase rules allow uploads
   - Check network connectivity

---

## Future Enhancements

1. **Audio Transcription**
   - Integrate Google Speech-to-Text API
   - Auto-transcribe recordings
   - Store transcription in database

2. **Audio Playback**
   - Add playback functionality in profile
   - Volume controls and seek bar
   - Download recordings

3. **Document Processing**
   - OCR for PDF text extraction
   - Medical data extraction from documents
   - Document classification

4. **Voice Analysis**
   - Analyze emotional tone
   - Extract keywords
   - Auto-summarization

5. **Batch Operations**
   - Select and delete multiple recordings
   - Export all documents as ZIP
   - Archive old recordings

---

## Testing

### Manual Testing Checklist

- [ ] Can start recording with microphone
- [ ] Duration updates correctly during recording
- [ ] Can pause and resume recording
- [ ] Can cancel recording (file deleted)
- [ ] Can add notes before upload
- [ ] Recording uploads successfully
- [ ] Recording appears in list after upload
- [ ] Can delete recording from list
- [ ] PDF file picker opens
- [ ] PDF upload shows confirmation dialog
- [ ] PDF uploads successfully
- [ ] PDF appears in medical documents list
- [ ] Can delete PDF from list
- [ ] Error messages display correctly
- [ ] App handles network disconnection

---

## Database Migration

To apply the new AudioRecording model, run:

```bash
# Backend directory
alembic revision --autogenerate -m "Add AudioRecording model"
alembic upgrade head
```

---

## Support & Documentation

For more information:
- Backend API docs: `/api/v1/docs`
- Flutter documentation: `README.md`
- Firebase setup: `firebase.json`

