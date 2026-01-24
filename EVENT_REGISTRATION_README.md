# Event Registration XML Documentation

## Overview

This document describes the structure and enhancements made to the `event_registration.xml` file for the Scaters UK Roadshow 2026 event registration system.

## Recent Enhancements (January 2026)

### 1. Critical Data Fields Added

#### Payment & Billing Information
- **`paymentMethod`**: Payment method used (Credit Card, Bank Transfer, PayPal)
- **`amountPaid`**: Amount paid with currency attribute (e.g., `<amountPaid currency="GBP">75.00</amountPaid>`)
- **`paymentDate`**: ISO 8601 timestamp of when payment was processed
- **`lastUpdated`**: Timestamp tracking last modification to registration

#### Emergency Contact Enhancement
- **`email`**: Emergency contact email addresses added to all registrations
  - Previously only phone numbers were stored
  - Critical for multiple communication channels during emergencies

#### Google Forms Integration Fields
- **`phoneHome`**: Home phone number (aligns with GOOGLE_FORMS_SETUP.md)
- **`preferredContactMethod`**: Preferred communication method (Mobile/Email)
- **`boardTypes`**: Types of skateboards owned (comma-separated list)
- **`favoritePros`**: Favorite professional skateboarders
- **`dataSource`**: Indicates origin of registration (Google Forms, Website, etc.)

#### Operational & Compliance Fields
- **`dietaryRequirements`**: Dietary restrictions (None, Vegetarian, Vegan, etc.)
- **`tShirtSize`**: T-shirt size for merchandise (XS, S, M, L, XL, XXL)
- **`waiverSigned`**: Boolean indicating liability waiver acceptance
- **`waiverDate`**: Timestamp of waiver signature

### 2. Structural Improvements

#### Preferences Section
Added new `<preferences>` block to all registrations containing:
```xml
<preferences>
    <dietaryRequirements>Vegetarian</dietaryRequirements>
    <tShirtSize>S</tShirtSize>
    <waiverSigned>true</waiverSigned>
    <waiverDate>2026-01-21T11:00:00Z</waiverDate>
</preferences>
```

#### Enhanced Skateboarding Information
Extended skateboarding data for better participant profiling:
```xml
<skateboarding>
    <experienceLevel>Advanced</experienceLevel>
    <preferredDeck>The Bull</preferredDeck>
    <boardTypes>Street, Cruiser</boardTypes>
    <favoritePros>Leticia Bufoni, Lucien Clarke</favoritePros>
    <specialRequirements>Requires vegetarian meal options</specialRequirements>
</skateboarding>
```

### 3. XML Schema Definition (XSD)

Created `event_registration.xsd` to provide:
- **Formal validation** of XML structure
- **Type constraints** (e.g., payment status must be: Pending, Paid, Refunded, Cancelled)
- **Required fields enforcement**
- **Consistent data types** (dates, decimals, booleans)
- **Documentation** for integration systems

#### Schema Location
The XML now references the schema:
```xml
xsi:schemaLocation="https://scaters.com/roadshow-2026 event_registration.xsd"
```

## Data Structure

### Registration Types

| Ticket Type | Description | Price (GBP) |
|-------------|-------------|-------------|
| Competitor | Adult participant in skateboarding competition | £75.00 |
| Youth Competitor | Participant under 18 (requires guardian consent) | £50.00 |
| Pro Competitor | Professional-level participant | £100.00 |
| Spectator | Non-competing attendee | Free |

### Event Locations

1. **London** - March 12, 2026
   - Venue: Southbank Undercroft ("The Concrete Heart")
   
2. **Manchester** - March 19, 2026
   - Venue: Projekt MCR ("The Industrial Abyss")
   
3. **Glasgow** - March 26, 2026
   - Venue: Kelvingrove ("The Northern Peak")

## Integration with Google Forms

The XML structure is now aligned with the Google Forms setup documented in `GOOGLE_FORMS_SETUP.md`:

### Mapped Fields

| XML Field | Google Forms Entry | Purpose |
|-----------|-------------------|---------|
| `personalInfo/firstName` | `entry.fullname` (first part) | Participant name |
| `personalInfo/dateOfBirth` | `entry.dob` | Age verification |
| `contactInfo/email` | `entry.email` | Primary contact |
| `contactInfo/phone` | `entry.phone_mobile` | Mobile contact |
| `contactInfo/phoneHome` | `entry.phone_home` | Home phone |
| `contactInfo/preferredContactMethod` | `entry.contact_method` | Communication preference |
| `skateboarding/experienceLevel` | `entry.exp_level` | Skill level |
| `skateboarding/boardTypes` | `entry.board_types` | Equipment owned |
| `skateboarding/favoritePros` | `entry.fav_pros` | Interest profiling |
| `preferences/dietaryRequirements` | Extracted from notes | Catering needs |

### Data Synchronization

- **`dataSource`** field tracks whether data originated from Google Forms or direct website entry
- Enables bidirectional sync and duplicate detection
- Future enhancement: Add `googleFormSubmissionId` for direct linking

## Validation

### XML Validation

```bash
# Using Python with lxml
python3 -c "
from lxml import etree
schema = etree.XMLSchema(file='event_registration.xsd')
doc = etree.parse('event_registration.xml')
print('Valid!' if schema.validate(doc) else 'Invalid!')
"
```

### Data Integrity Checks

All registrations include:
- ✓ Unique registration ID
- ✓ Valid payment information
- ✓ Complete contact details (email + phone)
- ✓ Emergency contact with email
- ✓ Waiver acceptance (for compliance)
- ✓ Timestamp audit trail

## Best Practices

### Adding New Registrations

1. **Follow the schema** - Validate against `event_registration.xsd`
2. **Include all required fields** - Payment info, contact details, waiver
3. **Use consistent date formats** - ISO 8601 (e.g., `2026-01-24T10:30:00Z`)
4. **Track data source** - Set `dataSource` to indicate origin
5. **Update `lastUpdated`** - Timestamp when modifying existing records

### Guardian/Minor Requirements

For participants under 18:
- **Required**: `<parentGuardian required="true">` section
- **Required**: Guardian consent with signature and date
- **Required**: Guardian contact information
- **Best Practice**: Include guardian in guests list for event access

### Payment Tracking

- `paymentStatus`: Must be Pending, Paid, Refunded, or Cancelled
- `amountPaid`: Must include currency attribute
- `paymentDate`: Required when status is "Paid"
- `paymentMethod`: Track for reconciliation

## File Locations

```
/
├── event_registration.xml     # Main registration data
├── event_registration.xsd     # XML Schema Definition
├── GOOGLE_FORMS_SETUP.md     # Google Forms integration guide
└── EVENT_REGISTRATION_README.md  # This file
```

## Compliance & Privacy

- All personal data complies with UK GDPR requirements
- Emergency contacts now include email for redundancy
- Waiver acceptance tracked with timestamps
- Data source tracking enables audit trails

## Support

For questions or issues:
- **Schema Validation Errors**: Check field types and required elements against XSD
- **Google Forms Sync**: See `GOOGLE_FORMS_SETUP.md`
- **General Questions**: Contact event coordination team

---

**Last Updated**: January 24, 2026  
**Schema Version**: 1.0  
**Namespace**: `https://scaters.com/roadshow-2026`
