# Google Forms Integration Setup Guide

This guide explains how to configure the Event Registration form to submit data to your Google Form.

## Overview

The custom event registration form in `index.html` has been updated to submit user data directly to a Google Form using POST requests. The form fields are mapped to Google Form entry IDs, which you need to configure.

## Step-by-Step Setup Instructions

### 1. Access Your Google Form

Open your Google Form in edit mode:
- URL: `https://docs.google.com/forms/d/e/1FAIpQLSfWMYaxTSSyaVzIx6_VWpEZsVqJfxa8cKW6NvbOoPxqxRi8Qg/viewform`

### 2. Find Entry IDs for Each Field

For each field in your Google Form, you need to find its entry ID:

1. **Open the Google Form** in your browser
2. **Right-click** on the first input field
3. Select **"Inspect"** or **"Inspect Element"** (opens Developer Tools)
4. Look for an attribute like `name="entry.XXXXXXXXX"` where XXXXXXXXX is a number
5. Copy this entry ID (including the "entry." part)
6. Repeat for all fields

**Example:**
```html
<input type="text" name="entry.123456789" ...>
```
The entry ID would be: `entry.123456789`

### 3. Update the Configuration in index.html

Open `index.html` and find the `GOOGLE_FORM_CONFIG` section (around line 3127).

Update each entry ID in the `fields` object:

```javascript
const GOOGLE_FORM_CONFIG = {
    formUrl: 'https://docs.google.com/forms/d/e/1FAIpQLSfWMYaxTSSyaVzIx6_VWpEZsVqJfxa8cKW6NvbOoPxqxRi8Qg/formResponse',
    
    fields: {
        pref_date: 'entry.123456789',        // Replace with actual entry ID
        pref_loc: 'entry.234567890',         // Replace with actual entry ID
        hunting_grounds: 'entry.XXXXXXXXX',  // Replace with actual entry ID
        // ... update all other fields
    }
};
```

### 4. Field Mapping Reference

Here's a complete list of form fields that need to be mapped:

| Form Field ID | Description | Google Form Entry ID |
|--------------|-------------|---------------------|
| `pref_date` | Preferred Event Date | `entry.XXXXXXXXX` |
| `pref_loc` | Preferred Event Location | `entry.XXXXXXXXX` |
| `hunting_grounds` | Participate in Hunting Grounds Challenge | `entry.XXXXXXXXX` |
| `evening_type` | Evening Event Type | `entry.XXXXXXXXX` |
| `fullname` | Full Name of Main Entrant | `entry.XXXXXXXXX` |
| `dob` | Date of Birth | `entry.XXXXXXXXX` |
| `age` | Age | `entry.XXXXXXXXX` |
| `gender` | Sex / Gender | `entry.XXXXXXXXX` |
| `email` | Email Address | `entry.XXXXXXXXX` |
| `address` | Home Address | `entry.XXXXXXXXX` |
| `parent_name` | Parent/Guardian Name | `entry.XXXXXXXXX` |
| `parent_rel` | Relationship to Main Entrant | `entry.XXXXXXXXX` |
| `parent_contact` | Guardian Contact Details | `entry.XXXXXXXXX` |
| `phone_mobile` | Phone Number (Mobile) | `entry.XXXXXXXXX` |
| `phone_home` | Phone Number (Home) | `entry.XXXXXXXXX` |
| `phone_work` | Phone Number (Work) | `entry.XXXXXXXXX` |
| `contact_method` | Preferred Contact Method | `entry.XXXXXXXXX` |
| `exp_level` | Skateboarding Experience Level | `entry.XXXXXXXXX` |
| `board_types` | Types of Skateboards Owned | `entry.XXXXXXXXX` |
| `fav_pros` | Favourite Professional Skateboarders | `entry.XXXXXXXXX` |
| `guest1` | Guest 1 Full Name | `entry.XXXXXXXXX` |
| `guest2` | Guest 2 Full Name | `entry.XXXXXXXXX` |

### 5. Google Form Field Order

Make sure your Google Form has fields in a corresponding order or at least has fields that match the data being sent. The field types should be:

- **Date fields**: Use "Date" question type
- **Dropdown fields**: Use "Multiple choice" or "Dropdown" question type
- **Text fields**: Use "Short answer" question type
- **Checkbox field** (board_types): Use "Checkboxes" question type
- **Hunting Grounds Challenge** (hunting_grounds): Use "Multiple choice" question type with "Yes" and "No" options

#### Hunting Grounds Challenge Question

The form includes a question asking participants if they want to participate in the Hunting Grounds Challenge and win prizes. This question appears after the "Preferred Event Location" field.

**Setup Instructions:**
1. In your Google Form, add a **Multiple choice** question after the "Preferred Event Location" field
2. Set the question text to: "Do you want to participate in the Hunting Grounds challenge and win prizes?"
3. Add two options: "Yes" and "No"
4. Mark this question as **Required**
5. Inspect the form to find the entry ID (e.g., `entry.987654321`)
6. Update the `hunting_grounds` field in the `GOOGLE_FORM_CONFIG` with the correct entry ID

**Note:** The form uses custom checkboxes styled for the UI, but the value sent to Google Forms will be either "Yes" or "No" based on the user's selection.

### 6. Test the Integration

1. Open `index.html` in a browser
2. Navigate to the Event Registration section
3. Fill out the form completely
4. Click "CONFIRM REGISTRATION"
5. Check your Google Form responses to verify the data was submitted

### 7. CORS and Submission Notes

- The form uses `mode: 'no-cors'` which means you won't receive a response from Google
- Even if the browser console shows an error, the form submission likely succeeded
- Check your Google Form responses spreadsheet to confirm submissions
- The form will show "TRANSMISSION COMPLETE" regardless of the actual submission status

## Troubleshooting

### Data Not Appearing in Google Form

1. **Verify Entry IDs**: Double-check that all entry IDs are correct
2. **Check Form URL**: Ensure the `formUrl` ends with `/formResponse` not `/viewform`
3. **Field Types Match**: Make sure Google Form field types match the data being sent
4. **Form is Accepting Responses**: Verify your Google Form is set to accept responses

### Browser Console Errors

- Errors related to CORS are expected and don't indicate failure
- The form submission may still be successful despite console errors
- Always verify by checking the Google Form responses

### Optional Fields

If you want to make some fields optional:
- In Google Form: Uncheck "Required" for those questions
- The code already handles optional fields by checking for empty values

## Additional Configuration

### Conditional Fields (Under 18)

The parent/guardian fields are automatically shown when age < 18:
- `parent_name`
- `parent_rel`
- `parent_contact`

These fields are only required when visible.

### Checkbox Handling

The skateboard types checkboxes are collected and sent as a comma-separated string:
- Example: "Street, Cruiser, Longboard"

Make sure your Google Form has a "Checkboxes" question type with matching options:
- Street
- Cruiser
- Longboard
- Park/Vert
- Electric

## Support

For issues or questions:
1. Check that all entry IDs are correctly mapped
2. Test with a minimal form submission first
3. Verify Google Form is accepting responses
4. Check browser console for any unexpected errors

---

**Last Updated**: January 2026  
**Form Version**: 1.0  
**Google Form URL**: https://docs.google.com/forms/d/e/1FAIpQLSfWMYaxTSSyaVzIx6_VWpEZsVqJfxa8cKW6NvbOoPxqxRi8Qg/viewform
