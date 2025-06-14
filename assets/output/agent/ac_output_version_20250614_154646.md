# ACTOR_OUTPUT

Generated on: 2025-06-14 15:46:46

## ACTOR

### Student

- **ID**: student
- **Role**: Primary user seeking information and services.

#### Responsibilities

- Seeking 24/7 answers to questions about admissions, enrollment, financial aid, and campus services.
- Accessing personal information such as grades, account balances, and application status.
- Navigating university websites and resources efficiently.

#### Permissions

- Access public university information.
- Authenticate to view and manage personal data.
- Initiate support requests or escalations to human agents.

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Interacts with the virtual agent through web or mobile interfaces to get answers and perform tasks.
- **Target**: Human Agent
  - **Type**: escalates to
  - **Description**: Is seamlessly handed off to a human agent when the virtual agent cannot resolve the query.

### Human Agent

- **ID**: human_agent
- **Role**: University support staff managing virtual agent interactions.

#### Responsibilities

- Handling complex queries escalated from the virtual agent.
- Monitoring conversation logs for quality assurance.
- Updating the knowledge base to improve virtual agent accuracy.
- Analyzing user interaction data to identify service gaps.

#### Permissions

- Access agent dashboard with conversation history and user data.
- Take over live chats from the virtual agent.
- Create, edit, and manage knowledge base articles.
- View performance analytics and reports.

#### Interactions

- **Target**: Virtual Agent Solution
  - **Type**: manages
  - **Description**: Uses the backend system to configure, train, and monitor the virtual agent.
- **Target**: Student
  - **Type**: supports
  - **Description**: Provides direct, in-depth support to students and other users whose issues are escalated.

### Parent/Guardian

- **ID**: parent_guardian
- **Role**: User seeking information on behalf of a student.

#### Responsibilities

- Inquiring about tuition fees, payment deadlines, campus safety, and housing.
- Understanding university policies and procedures relevant to their student.

#### Permissions

- Access public information.
- Access student-specific information if granted delegate/proxy access by the student.

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Asks the virtual agent general questions about the university or specific questions if they have appropriate proxy access.

### Staff

- **ID**: staff
- **Role**: University employee using the system for information.

#### Responsibilities

- Finding information related to HR, payroll, benefits, and internal policies.
- Getting support for internal IT and administrative systems.

#### Permissions

- Access public information.
- Authenticate to access internal, staff-only knowledge bases and services.

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Interacts with the virtual agent to find answers to work-related questions.

### External Client / Visiting Scholar

- **ID**: external_user
- **Role**: External party seeking information about the university.

#### Responsibilities

- Asking about public events, campus tours, research collaboration opportunities, and community programs.
- Finding contact information for specific departments or individuals.

#### Permissions

- Access to all public-facing information and knowledge bases.

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Utilizes the public-facing virtual agent to get general information about UC San Diego.

### Actor Hierarchy

Human Agents are system administrators who manage the virtual agent and handle escalated support cases from all other user groups. The other actors (Students, Parents/Guardians, Staff, External Clients) are end-users who consume the information and services provided by the virtual agent. Students are the primary and largest user group, but there is no formal hierarchy among the different end-user types.

### Stakeholder Summary

The stakeholders for the Virtual Agent Solution include all direct actors (Students, Staff, Parents/Guardians, Human Agents, External Clients) as well as several non-user groups with a vested interest in the project's success. These additional stakeholders are: the multiple university departments whose services will be supported by the agent; the UC San Diego evaluation team responsible for selecting the solution; the RFI administrator managing the procurement; international partners who rely on university communications; and the vendors who are proposing solutions. The project must balance the needs of direct users for effective service with the strategic and operational goals of the administrative and departmental stakeholders.

