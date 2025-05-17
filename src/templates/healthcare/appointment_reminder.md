# Patient Appointment Reminder Template

## Overview
This template is designed for healthcare providers to automatically remind patients of upcoming appointments, reducing no-shows and improving scheduling efficiency.

## Script Flow

### Introduction
```
Hello, this is [CLINIC_NAME] calling to remind [PATIENT_NAME] about an upcoming appointment. Am I speaking with [PATIENT_NAME] or their caregiver?
```

### Appointment Details
```
Your appointment is scheduled for [APPOINTMENT_DATE] at [APPOINTMENT_TIME] with [PROVIDER_NAME] at [LOCATION]. 

Would you like me to repeat this information?
```

### Confirmation Request
```
Can you confirm that you will be attending this appointment?
```

### If Confirmed
```
Great! We look forward to seeing you. Please remember to bring your insurance card and arrive 15 minutes early to complete any necessary paperwork.

Do you have any questions about your upcoming appointment?
```

### If Rescheduling Needed
```
I understand. Would you like to reschedule your appointment now?

[If yes] I can help you with that. Let me check the available times.
[Provider-specific scheduling options would be presented here]

[If no] No problem. Please call our scheduling line at [SCHEDULING_PHONE] at your earliest convenience to reschedule.
```

### Closing
```
Thank you for your time. If you need to reach us before your appointment, please call [CLINIC_PHONE]. Have a great day!
```

## Integration Points
- Electronic Health Record (EHR) system for appointment data
- Scheduling system for real-time availability
- Patient portal for appointment confirmation updates

## Customization Options
- Appointment type-specific instructions
- Insurance verification reminders
- COVID-19 screening questions
- Telehealth vs. in-person appointment instructions

## Compliance Notes
- This template is designed with HIPAA compliance in mind
- Ensure patient identity verification before sharing PHI
- Call recording settings should be configured according to state laws
- Document all scheduling changes in the patient's EHR
