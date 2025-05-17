# Fraud Alert Verification Template

## Overview
This template is designed for financial institutions to verify potential fraudulent activities with customers, ensuring quick response to suspicious transactions while maintaining customer trust.

## Script Flow

### Introduction
```
Hello, this is [BANK_NAME] fraud prevention department calling for [CUSTOMER_NAME]. This is an important call regarding recent activity on your account. Am I speaking with [CUSTOMER_NAME]?
```

### Identity Verification
```
For your security, I need to verify your identity. Please confirm the last 4 digits of your Social Security Number.

[After verification]
Thank you for verifying your identity.
```

### Alert Description
```
We've detected some activity on your [ACCOUNT_TYPE] ending in [LAST_4_DIGITS] that appears unusual based on your normal spending patterns. I'm calling to verify whether you authorized these transactions.
```

### Transaction Details
```
Did you make a purchase of [AMOUNT] at [MERCHANT] on [DATE] at approximately [TIME]?

[If additional transactions]
There was also a transaction of [AMOUNT] at [MERCHANT] on [DATE]. Did you authorize this transaction as well?
```

### If Confirmed Legitimate
```
Thank you for confirming these transactions. We appreciate your patience as we work to keep your account secure. Your account will remain active and no further action is needed.

Is there anything else I can assist you with regarding your account today?
```

### If Fraud Confirmed
```
I understand that you did not authorize these transactions. I'll help you secure your account immediately.

I'll be placing a temporary hold on your card to prevent any further unauthorized transactions. We'll issue you a new card which should arrive within 5-7 business days.

Would you like to review any other recent transactions to check for additional unauthorized activity?
```

### Closing
```
Thank you for your time today. If you notice any other suspicious activity, please call the number on the back of your card immediately. Is there anything else I can assist you with?
```

## Integration Points
- Core banking system for transaction data
- Fraud detection system for alert triggers
- Customer relationship management (CRM) system for case tracking
- Card management system for card replacement

## Customization Options
- Transaction type-specific questions
- Additional security verification steps
- Different handling for credit vs. debit cards
- Branch location information for emergency card replacement

## Compliance Notes
- This template follows financial regulatory guidelines
- All calls should be recorded and stored according to retention policies
- Customer identity must be verified before discussing account details
- Ensure agents are trained on Regulation E requirements for fraud claims
