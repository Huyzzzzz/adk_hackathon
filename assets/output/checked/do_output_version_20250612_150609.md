# DATA_OBJECT_OUTPUT

Generated on: 2025-06-12 15:06:09

## DATA_OBJECT

### User Account

- **ID**: DO-001
- **Description**: Represents an individual who interacts with the system, including landlords, tenants, and Rent Board staff. It stores user credentials, contact information, role-based access permissions, and a history of their activities.

### Petition

- **ID**: DO-002
- **Description**: Represents an electronic application filed by a landlord or tenant. It includes all submitted form data, saved drafts, and associated supporting documents. Each successful submission initiates a case and is assigned a unique confirmation number.

### Case

- **ID**: DO-003
- **Description**: The central data object for the internal management of a dispute. It tracks the entire lifecycle from intake to closure, including status, assigned staff, deadlines, an audit trail of all actions, and links to all related petitions, documents, and communications.

### Document

- **ID**: DO-004
- **Description**: Represents any file that is uploaded, generated, or stored within the system. This includes user-uploaded supporting evidence, system-generated notices and decisions from templates, and other case-related files.

### Report

- **ID**: DO-005
- **Description**: Represents the output of the analytics and reporting engine. This can be a pre-defined or custom-generated report containing key metrics, data visualizations, and case statistics, exportable in formats like CSV and PDF.

### Audit Log

- **ID**: DO-006
- **Description**: A chronological record of events and actions performed by users and the system. It is used for security auditing, tracking case history, and ensuring compliance with data integrity requirements.

