# 🎯 EXACT TESTING STEPS - Copy & Paste Ready

## Before You Start
1. Ensure Flutter is installed: `flutter --version`
2. Ensure you have internet connection (Firebase required)
3. Have the credentials ready (provided below)

---

## 📱 TEST 1: Doctor Login & Dashboard

### Step 1: Run Flutter App
```bash
flutter run
```

### Step 2: Doctor Login Screen Appears
You'll see the doctor login screen with:
- Email field
- Password field
- "Sign In" button

### Step 3: Enter Credentials
**Copy & Paste This:**
```
Email:    test.doctor@test.com
Password: Test123456!
```

### Step 4: Click Sign In
**Expected**: Doctor dashboard loads with:
- ✅ Doctor info card (name, department)
- ✅ Queue statistics (Total, High, Medium, Low counts)
- ✅ Next Patient Card (with risk level badge)
- ✅ "Call Next Patient" button
- ✅ Waiting Patients list

### Step 5: Test Queue Features
**Click on different sections:**
- Next Patient Card → Shows highest priority patient
- Waiting Patients List → Shows all patients with risk levels
- "Call Next Patient" → Calls highest priority patient
- Menu → "Priority Queue" → See full queue sorted by risk

---

## 🏥 TEST 2: Hospital Finder (Patient Side)

### Prerequisites
First, you need a patient account:

1. **Go back to login**
   - Click logout button

2. **Register as Patient**
   - Email: `testpatient@example.com`
   - Password: `Patient123456!`
   - Click Register

3. **Complete Triage**
   - Select any symptoms (e.g., Fever, Headache)
   - Input vitals: BP 120/80, HR 80, Temp 98.6
   - Click Submit

### Step 1: Complete Triage
You'll get a risk level (HIGH/MEDIUM/LOW)

### Step 2: Find Hospitals
**In patient app menu:**
- Click "Find Hospitals"

**Expected:**
- ✅ Hospital list loads
- ✅ Each hospital shows:
  - Name
  - Location (District, State)
  - Distance (if location enabled)
- ✅ Tap hospital → Details modal shows

### Step 3: View Hospital Details
**When you tap a hospital:**
- ✅ Hospital name
- ✅ Hospital type
- ✅ Address
- ✅ Total beds & Emergency beds
- ✅ Contact phone
- ✅ List of departments (as chips)

### Step 4: Optional - Enable Location
**For distance display:**
- Allow location permission when prompted
- Hospitals will be sorted by distance (nearest first)

---

## 📄 TEST 3: Medical Documents Upload

### Step 1: Go to Patient Profile
**In patient app:**
- Click menu → "My Profile"

**Expected:**
- ✅ Patient info card (name, age, gender)
- ✅ Pre-existing conditions (if any)
- ✅ Medical Documents section

### Step 2: Upload Document
**Click:** "Upload Medical Document (PDF)"

**Expected:**
- ✅ File picker opens
- ✅ Can only select PDF files
- ✅ Can browse device for files

### Step 3: Select PDF File
1. Find any PDF file on your device
2. Select it
3. Wait for upload

**Expected:**
- ✅ Success message shows
- ✅ File appears in list

### Step 4: View Document List
**In medical documents section:**
- ✅ File name shown
- ✅ Upload date shown
- ✅ File size shown
- ✅ Delete button available

---

## ⏱️ TEST 4: Queue Status & Live Timer

### Step 1: Patient Gets Token
**After completing triage:**
- ✅ Token screen shows automatically
- ✅ Or go to "Queue Status" in menu

**You'll see:**
- ✅ Risk level badge (color-coded)
- ✅ Token number
- ✅ Queue position
- ✅ **Live countdown timer**

### Step 2: Watch Timer Count Down
**Expected:**
- Timer shows: `5:00 min` (for example)
- After 1 second: `4:59 min`
- After 2 seconds: `4:58 min`
- Continues to count down...

### Step 3: Verify Risk-Based Wait Time
**Different patients see different waits:**

**If HIGH risk at position 1:**
- Timer shows: 5 minutes (5 min × 1 position)

**If MEDIUM risk at position 1:**
- Timer shows: 10 minutes (10 min × 1 position)

**If LOW risk at position 1:**
- Timer shows: 15 minutes (15 min × 1 position)

---

## 👨‍⚕️ TEST 5: Doctor Priority Queue

### Step 1: Doctor Login (Again)
```
Email:    test.doctor@test.com
Password: Test123456!
```

### Step 2: View Priority Queue Screen
**In doctor menu:**
- Click "Priority Queue"

**Expected:**
- ✅ List of all waiting patients
- ✅ Sorted by risk level:
  - Top: 🔴 RED (HIGH risk)
  - Middle: 🟡 YELLOW (MEDIUM risk)
  - Bottom: 🟢 GREEN (LOW risk)

### Step 3: Verify Sorting
**Check the order:**
- HIGH risk patients listed first
- MEDIUM risk patients second
- LOW risk patients last
- Within same risk: sorted by arrival time

### Step 4: View Patient Details
**Tap any patient:**
- ✅ Token number shows
- ✅ Department shows
- ✅ Wait time shows
- ✅ Risk level shows
- ✅ Conditions/symptoms show

### Step 5: Call Next Patient
**On dashboard:**
- Click "Call Next Patient"

**Expected:**
- ✅ Highest priority patient selected
- ✅ Patient status changes to "in_progress"
- ✅ Next patient card updates
- ✅ Remaining patients' positions update
- ✅ Queue recalculates automatically

---

## 🔐 TEST 6: Different Doctor Departments

### Test Multiple Doctors
**Try logging in with different doctors:**

```
1. Cardiology Doctor:
   Email:    dr.priya.cardiology@hospital.com
   Password: CardiologyDoc456!

2. Emergency Doctor:
   Email:    dr.rajesh.emergency@hospital.com
   Password: EmergencyDoctor123!

3. General Medicine Doctor:
   Email:    dr.arun.general@hospital.com
   Password: GeneralMed789!
```

### Expected Results
- ✅ Each doctor logs in successfully
- ✅ Shows their department
- ✅ Queue filters by their department
- ✅ Can see their assigned patients

---

## ✅ COMPLETE TEST CHECKLIST

### Risk Levels & Queue
- [ ] Risk level assigned (HIGH/MEDIUM/LOW)
- [ ] Risk level color-coded (RED/YELLOW/GREEN)
- [ ] Queue sorted by risk (HIGH first)
- [ ] Wait times calculated correctly
- [ ] Real-time updates when queue changes

### Patient Features
- [ ] Patient can login/register
- [ ] Triage assessment works
- [ ] Queue status screen shows
- [ ] Live timer counts down every second
- [ ] Medical document upload works
- [ ] Documents list displays
- [ ] Hospital finder shows all hospitals
- [ ] Distance calculated (if location enabled)
- [ ] Profile shows all info

### Doctor Features
- [ ] Doctor login works (multiple doctors)
- [ ] Dashboard loads correctly
- [ ] Next Patient Card shows
- [ ] Priority Queue sorts correctly
- [ ] Call Next Patient updates queue
- [ ] Queue statistics accurate
- [ ] Real-time updates working
- [ ] Availability toggle works

### Technical
- [ ] Zero compilation errors
- [ ] Smooth animations
- [ ] No lag in updates
- [ ] All buttons respond
- [ ] Error messages clear

---

## 🐛 Troubleshooting

### Doctor Login Fails
**Issue**: "Login failed. Please check your credentials."
**Solution**: 
- Copy exact email from above
- Copy exact password from above
- Check internet connection
- Try Test doctor first: test.doctor@test.com / Test123456!

### Medical Document Upload Fails
**Issue**: "Failed to upload document"
**Solution**:
- Ensure file is PDF (not DOC, DOCX, etc.)
- File size < 10MB
- Check internet connection
- Try with smaller PDF file

### Queue Not Updating
**Issue**: Timer or queue position not changing
**Solution**:
- Check Firestore is connected (look for "Getting data..." message)
- Try refreshing the screen (swipe down)
- Close and reopen the app
- Check internet connection

### Hospital Not Showing
**Issue**: Hospital finder shows empty list
**Solution**:
- Check Firestore hospitals collection has data
- Refresh the screen
- Check internet connection

### Timer Not Counting Down
**Issue**: Timer stays at same value
**Solution**:
- Ensure patient has valid token
- Check token has `createdAt` and `estimatedWaitMinutes`
- Close and reopen queue status screen
- Check Firebase is connected

---

## 📊 Expected Behavior Summary

| Feature | Expected | Status |
|---------|----------|--------|
| Doctor Login | Works with credentials | ✅ |
| Patient Registration | Creates account | ✅ |
| Risk Assignment | HIGH/MEDIUM/LOW | ✅ |
| Queue Sorting | By risk level | ✅ |
| Wait Time | Based on risk | ✅ |
| Live Timer | Counts down | ✅ |
| Medical Upload | Stores in Firebase | ✅ |
| Hospital Finder | Lists all | ✅ |
| Real-time Updates | Via Firestore | ✅ |

---

## 🎉 If Everything Passes

Congratulations! The system is working perfectly.

**You can now:**
- ✅ Submit to hackathon
- ✅ Demo to judges
- ✅ Test with multiple doctors
- ✅ Create test patients
- ✅ Show risk-based prioritization
- ✅ Demonstrate real-time queue updates

---

## 📞 Support

**Doctor Credentials**: See section "TEST 1" above
**Patient Test**: Register with any email/password
**Hospitals**: Automatically loaded from Firestore
**Documents**: Upload any PDF < 10MB

---

Generated: February 15, 2026
Ready to Test: ✅ YES

