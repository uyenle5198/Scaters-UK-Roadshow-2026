# Google Form Setup Mapping

This document provides a comprehensive mapping between XML elements in `event_registration.xml` and corresponding Google Form fields. This ensures consistency between the data collection form and the stored XML data structure.

## Overview

The Scaters Raptor Roadshow 2026 event registration system uses an XML-based data structure to store participant information. To maintain data integrity and streamline form creation, each XML element must be mapped to its corresponding Google Form field.

## Benefits

- **Simplifies form creation and management** - Clear guidelines for setting up the Google Form
- **Maintains data integrity** - Ensures submissions match the expected XML structure
- **Facilitates updates** - Easy reference for future form modifications
- **Supports validation** - Documents required fields and data formats

---

## XML to Google Form Mapping

### 1. Event Preferences

These fields capture the participant's event preferences and activities.

| XML Element | Description | Google Form Field Type | Validation | Required |
|------------|-------------|----------------------|------------|----------|
| `<pref_date>` | Preferred event date | **Date** | Must be one of the roadshow dates (2026-03-12, 2026-03-19, or 2026-03-26) | Yes |
| `<pref_loc>` | Preferred event location | **Dropdown** or **Multiple Choice** | Options: "London", "Manchester", "Glasgow" | Yes |
| `<hunting_grounds>` | Participate in Hunting Grounds Challenge | **Multiple Choice** | Options: "Yes", "No" | Yes |
| `<evening_type>` | Evening event preference | **Multiple Choice** or **Dropdown** | Options: "Dinner with free drinks", "Talk with Skateboard England representative", "Meet an England Skateboarding Team rider" | Yes |

**Google Form Setup Notes:**
- The date field should allow selection from a predefined list or use validation to ensure only valid dates are accepted
- Location should match exactly the city names as stored in XML
- Hunting Grounds question should be clear about the challenge and prizes
- Evening type should present all available options

---

### 2. Personal Information

Core participant details required for registration.

| XML Element | Description | Google Form Field Type | Validation | Required |
|------------|-------------|----------------------|------------|----------|
| `<fullname>` | Full name of participant | **Short Answer** | Must contain first and last name | Yes |
| `<dob>` | Date of birth | **Date** | Format: YYYY-MM-DD; Must be a valid past date | Yes |
| `<age>` | Participant's age | **Short Answer** (Number) | Auto-calculated from DOB or manually entered; Positive integer | Yes |
| `<gender>` | Gender/Sex | **Multiple Choice** or **Dropdown** | Options: "Male", "Female", "Non-binary", "Prefer not to say" | Yes |

**Google Form Setup Notes:**
- Age can be auto-calculated from DOB using form logic if your form platform supports it
- DOB should use date picker for consistency
- Gender options should be inclusive while matching XML expectations

---

### 3. Contact Details

Contact information for reaching the participant.

| XML Element | Description | Google Form Field Type | Validation | Required |
|------------|-------------|----------------------|------------|----------|
| `<email>` | Email address | **Short Answer** | Must be valid email format (contains @ and domain) | Yes |
| `<address>` | Full home address | **Paragraph Text** | Complete address including postcode | Yes |
| `<phone_mobile>` | Mobile phone number | **Short Answer** | UK phone format (+44 or 0); Numbers only with optional spaces/dashes | Yes |
| `<phone_home>` | Home phone number | **Short Answer** | UK phone format; Optional field | No |
| `<phone_work>` | Work phone number | **Short Answer** | UK phone format; Optional field | No |
| `<contact_method>` | Preferred contact method | **Multiple Choice** | Options: "mobile", "email", "home", "work" | Yes |

**Google Form Setup Notes:**
- Email field should use built-in email validation
- At least one phone number (mobile) is required
- Contact method should match the available contact channels
- Phone numbers should accept various UK formats (+44 7700 900123 or 07700 900123)

---

### 4. Parent/Guardian Details (Conditional - Under 18 Only)

**IMPORTANT**: These fields are **MANDATORY** when the participant is under 18 years old.

| XML Element | Description | Google Form Field Type | Validation | Required |
|------------|-------------|----------------------|------------|----------|
| `<parent_name>` | Parent/Guardian full name | **Short Answer** | Must contain first and last name | **Yes (if age < 18)** |
| `<parent_rel>` | Relationship to participant | **Short Answer** or **Dropdown** | E.g., "Mother", "Father", "Guardian", "Grandparent" | **Yes (if age < 18)** |
| `<parent_contact>` | Parent/Guardian contact details | **Paragraph Text** | Should include phone and/or email | **Yes (if age < 18)** |

**Dynamic Form Logic:**
- These fields should only appear when the participant's age is under 18
- Use conditional logic based on the DOB or age field
- Mark these fields as required only when visible
- For participants 18 and over, these fields remain empty in the XML structure

**Google Form Setup Instructions:**
1. Create three questions for parent/guardian information
2. Set up a conditional rule: "Show these questions if Age < 18" or "Show these questions if DOB indicates under 18"
3. Mark all three parent/guardian fields as required when the condition is met
4. Consider adding helper text: "Required for participants under 18 years old"

---

### 5. Skateboarding Experience

Information about the participant's skateboarding background and preferences.

| XML Element | Description | Google Form Field Type | Validation | Required |
|------------|-------------|----------------------|------------|----------|
| `<exp_level>` | Skateboarding experience level | **Multiple Choice** or **Dropdown** | Options: "Beginner", "Intermediate", "Advanced" | Yes |
| `<board_types>` | Types of skateboards owned | **Checkboxes** (Multiple Selection) | Options: "Street Deck", "Cruiser", "Longboard", "Park Deck", "Mini Cruiser", "Electric" | No |
| `<fav_pros>` | Favorite professional skateboarder(s) | **Short Answer** or **Paragraph Text** | Text field; Can be single name or multiple names | No |

**Google Form Setup Notes:**
- Experience level helps organizers plan appropriate activities
- Board types should allow multiple selections (checkboxes)
- In XML, board types are stored as child elements within `<board_types>` parent element
- Multiple board selections are stored as separate `<board>` elements
- Favorite pros field is optional and flexible

**XML Structure for Board Types:**
```xml
<board_types>
  <board>Street Deck</board>
  <board>Cruiser</board>
  <board>Longboard</board>
</board_types>
```

---

### 6. Additional Information

Optional guest information.

| XML Element | Description | Google Form Field Type | Validation | Required |
|------------|-------------|----------------------|------------|----------|
| `<guest1>` | Full name of Guest 1 | **Short Answer** | Text field; First and last name preferred | No |
| `<guest2>` | Full name of Guest 2 | **Short Answer** | Text field; First and last name preferred | No |

**Google Form Setup Notes:**
- Guest fields are optional
- Consider adding context: "Bring up to 2 guests to the event"
- Store as empty elements in XML if no guests are registered

---

## Form Structure and Order

### Recommended Google Form Section Organization

To provide the best user experience, organize the form into logical sections:

#### **Section 1: Event Selection**
- Preferred Event Date
- Preferred Event Location
- Participate in Hunting Grounds Challenge
- Evening Event Type

#### **Section 2: Personal Information**
- Full Name
- Date of Birth
- Age
- Gender
- Email Address
- Home Address

#### **Section 3: Contact Details**
- Mobile Phone Number
- Home Phone Number (optional)
- Work Phone Number (optional)
- Preferred Contact Method

#### **Section 4: Parent/Guardian Information** (Conditional)
- Parent/Guardian Name
- Relationship to Participant
- Parent/Guardian Contact Details

*Note: This section appears only when age < 18*

#### **Section 5: Skateboarding Background**
- Experience Level
- Types of Skateboards Owned
- Favorite Professional Skateboarder(s)

#### **Section 6: Guest Information** (Optional)
- Guest 1 Full Name
- Guest 2 Full Name

---

## Validation Rules and Constraints

### Required Fields
All fields marked as "Yes" in the Required column must be completed before form submission.

**Always Required:**
- Event preferences (all 4 fields)
- Personal information (all 4 fields)
- Primary contact details (email, address, mobile phone, contact method)
- Experience level

**Conditionally Required (Under 18 only):**
- Parent/Guardian name
- Parent/Guardian relationship
- Parent/Guardian contact details

### Data Format Validation

| Field Type | Validation Rule | Example |
|-----------|----------------|---------|
| Date fields | YYYY-MM-DD format | 2026-03-12 |
| Email | Valid email format | example@domain.com |
| Phone numbers | UK format with country code or without | +44 7700 900123 or 07700 900123 |
| Age | Positive integer | 25 |

### Business Rules

1. **Age Verification**: If DOB indicates age < 18, parent/guardian section becomes mandatory
2. **Event Dates**: Must be one of the three roadshow dates:
   - March 12, 2026 (London)
   - March 19, 2026 (Manchester)
   - March 26, 2026 (Glasgow)
3. **Contact Method**: Should correspond to a provided contact detail (e.g., can't select "mobile" if no mobile number provided)

---

## Implementation Checklist

When creating the Google Form, use this checklist to ensure completeness:

- [ ] Create form with clear title and description
- [ ] Add all required fields from Event Preferences section
- [ ] Add all required fields from Personal Information section
- [ ] Add all fields from Contact Details section
- [ ] Set up conditional logic for Parent/Guardian section (age < 18)
- [ ] Add skateboarding experience fields
- [ ] Add optional guest fields
- [ ] Configure all field types correctly (dropdown, checkboxes, date, etc.)
- [ ] Set validation rules for email, phone, and date fields
- [ ] Mark all mandatory fields as required
- [ ] Test conditional logic for under-18 participants
- [ ] Verify all dropdown/multiple choice options match XML values exactly
- [ ] Test form submission and verify data format matches XML structure
- [ ] Document entry IDs for integration (see `GOOGLE_FORMS_SETUP.md`)

---

## Integration with XML Storage

### Data Flow

1. **User fills out Google Form** → Data collected with proper validation
2. **Form submission** → Data sent to backend system
3. **Backend processing** → Converts form data to XML structure
4. **XML storage** → Data stored in `event_registration.xml` with proper element structure

### Entry ID Mapping

After creating the Google Form, you'll need to map each field to its entry ID for programmatic submission. See `GOOGLE_FORMS_SETUP.md` for detailed instructions on:

- Finding entry IDs for each field
- Updating the configuration in `index.html`
- Testing the integration
- Troubleshooting common issues

### XML Entry Structure

Each registration creates an `<Entry>` element with a unique ID:

```xml
<Entry id="REG-2026-LON-001">
  <!-- All mapped fields -->
</Entry>
```

The ID format: `REG-YYYY-LOC-NNN` where:
- `YYYY` = Year (2026)
- `LOC` = Location code (LON, MAN, GLA)
- `NNN` = Sequential number
- Additional suffix `-U18` for under-18 participants

---

## Testing Recommendations

### Test Scenarios

1. **Adult Participant (18+)**
   - Fill all required fields
   - Verify parent/guardian section does NOT appear
   - Submit and check XML output

2. **Minor Participant (<18)**
   - Fill all required fields
   - Verify parent/guardian section DOES appear
   - Verify parent/guardian fields are required
   - Submit and check XML output

3. **Optional Fields**
   - Submit without home/work phone numbers
   - Submit without guests
   - Submit without favorite skateboarders
   - Verify empty elements in XML

4. **Multiple Board Types**
   - Select multiple skateboard types
   - Verify all selections stored as separate `<board>` elements in XML

5. **Validation Testing**
   - Test invalid email format
   - Test invalid date format
   - Test invalid phone number format
   - Verify all validations work correctly

---

## Maintenance and Updates

### Updating the Form

If you need to modify the Google Form:

1. **Document changes** in this file
2. **Update XML schema** if structure changes
3. **Update entry ID mappings** in `GOOGLE_FORMS_SETUP.md`
4. **Test integration** thoroughly
5. **Communicate changes** to all stakeholders

### Version Control

Keep track of changes to maintain consistency:

- Document version number and date of updates
- Note any changes to field names, types, or validations
- Archive old versions if structure changes significantly

---

## Reference Documents

- **XML Data File**: `event_registration.xml` - Contains sample entries and complete XML structure
- **Google Forms Integration Guide**: `GOOGLE_FORMS_SETUP.md` - Technical setup instructions
- **Main Documentation**: `README.md` - Project overview and general information

---

## Support and Questions

For questions or issues related to the Google Form setup:

1. Review this mapping document for field requirements
2. Check `GOOGLE_FORMS_SETUP.md` for technical integration steps
3. Validate against `event_registration.xml` for data structure
4. Test thoroughly with different scenarios before deployment

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Maintained By**: Scaters Worldwide Development Team  
**Related Files**: `event_registration.xml`, `GOOGLE_FORMS_SETUP.md`, `index.html`
