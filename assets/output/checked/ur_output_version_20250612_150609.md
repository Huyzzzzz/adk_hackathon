# USER_REQUIREMENTS_OUTPUT

Generated on: 2025-06-12 15:06:09

## Requirements

### Online Petition Filing

- **ID**: FR-001
- **Source**: RFP Section 3.1.a
- **Type**: Functional
- **Detail**: The system must provide a secure web portal for landlords and tenants to file petitions and related forms electronically. Acceptance Criteria: 1. Users can create and manage their accounts. 2. The system provides intuitive, multi-step forms for different petition types. 3. Users can save draft applications and return later. 4. Users can upload supporting documents in specified formats (e.g., PDF, DOCX, JPG). 5. Upon successful submission, the user receives a confirmation number and an email notification.
- **Covered USR**: USR-101, USR-201

### Case Management System (CMS)

- **ID**: FR-002
- **Source**: RFP Section 3.1.b
- **Type**: Functional
- **Detail**: The system must provide an internal portal for Rent Board staff to manage cases from intake to closure. Acceptance Criteria: 1. Staff can view, edit, and update case details. 2. The system shall track case statuses, deadlines, and assigned staff. 3. Staff can generate and send official notices and decisions from templates within the system. 4. A complete history of all actions, communications, and documents for a case is maintained and auditable.
- **Covered USR**: USR-301, USR-302

### Public Information Portal

- **ID**: FR-003
- **Source**: RFP Section 3.1.d
- **Type**: Functional
- **Detail**: The system must provide a public-facing, searchable portal for accessing non-confidential case information, decisions, and hearing schedules. Acceptance Criteria: 1. Users can search for cases by case number, address, or party name. 2. Search results display key information while redacting PII. 3. Users can view and download public documents associated with a case. 4. The portal must be mobile-responsive.
- **Covered USR**: USR-102, USR-202, USR-401

### Reporting and Analytics Dashboard

- **ID**: FR-004
- **Source**: RFP Section 3.1.f
- **Type**: Functional
- **Detail**: The system must include a dashboard for authorized staff to generate reports on key metrics. Acceptance Criteria: 1. The dashboard provides visualizations for case volumes, processing times, and outcomes. 2. Staff can generate pre-defined reports (e.g., monthly, quarterly, annual). 3. Authorized users can create custom reports by selecting data fields, filters, and date ranges. 4. Reports can be exported in standard formats like CSV and PDF.
- **Covered USR**: USR-303

### System Security

- **ID**: NFR-001
- **Source**: RFP Section 4.2
- **Type**: Constraint
- **Detail**: The system must comply with the City of San Francisco's data security policies, including encryption of all Personally Identifiable Information (PII) both at rest and in transit. Acceptance Criteria: 1. The system must pass a third-party security audit and penetration test before launch. 2. Access to the system is controlled by role-based access control (RBAC). 3. All user activity is logged for auditing purposes.
- **Covered USR**: All User Stories

### Accessibility Compliance

- **ID**: NFR-002
- **Source**: RFP Section 4.5
- **Type**: Constraint
- **Detail**: All public-facing components of the system must be compliant with Web Content Accessibility Guidelines (WCAG) 2.1 Level AA. Acceptance Criteria: 1. The system is fully navigable using a keyboard. 2. It is compatible with modern screen readers. 3. All forms, controls, and content are accessible and meet color contrast requirements.
- **Covered USR**: USR-101, USR-102, USR-201, USR-202, USR-401

### System Availability

- **ID**: NFR-003
- **Source**: RFP Section 4.1
- **Type**: Non-Functional
- **Detail**: The system must be available to users 99.9% of the time, excluding scheduled maintenance windows. Acceptance Criteria: 1. Uptime is monitored and reported on a monthly basis. 2. Scheduled maintenance is communicated to users at least 48 hours in advance and performed during off-peak hours.
- **Covered USR**: All User Stories

### Rent Ordinance Calculations

- **ID**: BR-001
- **Source**: RFP Section 3.2.a
- **Type**: Business Rule
- **Detail**: The system must accurately calculate allowable annual rent increases and other amounts based on the rules defined in the San Francisco Rent Ordinance. Acceptance Criteria: 1. The calculation engine correctly applies the official annual allowable increase percentage. 2. The system correctly factors in any banked increases or passthroughs as per the ordinance rules. 3. All calculation logic must be documented and testable.
- **Covered USR**: USR-103, USR-304

