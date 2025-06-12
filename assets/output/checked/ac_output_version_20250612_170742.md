# ACTOR_OUTPUT

Generated on: 2025-06-12 17:07:42

## ACTOR

### Students

- **ID**: student
- **Role**: Primary users of the virtual agent.

#### Responsibilities

- Interact with the virtual agent to get information about study abroad programs and other university services.

#### Permissions

- Ask questions in multiple languages
- Receive information about study abroad programs
- Interact on mobile devices
- Receive text notifications
- Be transferred to a human agent

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Ask the virtual agent questions in multiple languages.
- **Target**: Virtual Agent
  - **Type**: receives from
  - **Description**: Receive information about study abroad programs.
- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Interact with the virtual agent on mobile devices.
- **Target**: Notification System
  - **Type**: receives from
  - **Description**: Receive mass or small group text notifications.
- **Target**: Human Agent
  - **Type**: transferred to
  - **Description**: Be seamlessly transferred to a human agent if the virtual agent cannot resolve their query.

### Families

- **ID**: family
- **Role**: Users of the virtual agent, often on behalf of students.

#### Responsibilities

- Interact with the virtual agent to get information about study abroad programs.

#### Permissions

- Ask questions
- Receive information
- Interact on mobile devices

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Ask the virtual agent questions.
- **Target**: Virtual Agent
  - **Type**: receives from
  - **Description**: Receive information about study abroad programs.
- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Interact on mobile devices.

### International Partners

- **ID**: international_partner
- **Role**: Users of the virtual agent, related to university partnerships.

#### Responsibilities

- Interact with the virtual agent to get information about study abroad programs.

#### Permissions

- Ask questions
- Receive information

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Ask the virtual agent questions.
- **Target**: Virtual Agent
  - **Type**: receives from
  - **Description**: Receive information about study abroad programs.

### External Clients

- **ID**: external_client
- **Role**: A broad category of users seeking information from UC San Diego.

#### Responsibilities

- Interact with the virtual agent to get responses to their inquiries.

#### Permissions

- Receive AI-generated responses

#### Interactions

- **Target**: Virtual Agent
  - **Type**: receives from
  - **Description**: Receive AI-generated responses based on scraped documents.

### Vendors (of UC San Diego)

- **ID**: ucsd_vendor
- **Role**: Users of the virtual agent seeking information about payments and procurement.

#### Responsibilities

- Interact with the virtual agent to get status updates.

#### Permissions

- Receive status updates

#### Interactions

- **Target**: Virtual Agent
  - **Type**: receives from
  - **Description**: Receive status updates from systems like Oracle, PaymentWorks, and Concur via the virtual agent.

### Visiting Scholars

- **ID**: visiting_scholar
- **Role**: Users of the virtual agent.

#### Responsibilities

- Interact with the virtual agent to get information.

#### Permissions

- Make inquiries

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Use the virtual agent for inquiries.

### UC San Diego Staff (as users)

- **ID**: ucsd_staff_user
- **Role**: Users of the virtual agent, possibly for internal queries.

#### Responsibilities

- Interact with the virtual agent for information.

#### Permissions

- Make inquiries

#### Interactions

- **Target**: Virtual Agent
  - **Type**: uses
  - **Description**: Use the virtual agent for inquiries.

### Human Agents (UC San Diego Staff)

- **ID**: human_agent
- **Role**: Support staff who handle escalated queries from the virtual agent.

#### Responsibilities

- Take over conversations from the virtual agent.
- Provide assistance for complex issues that the virtual agent cannot handle.

#### Permissions

- Take over conversations
- View conversation history and user information

#### Interactions

- **Target**: Virtual Agent
  - **Type**: receives from
  - **Description**: Receive collected information and conversation history from the virtual agent for a smooth transition.

### UC San Diego Administrators/Analysts

- **ID**: administrator_analyst
- **Role**: Staff responsible for managing and improving the virtual agent.

#### Responsibilities

- Monitor the performance of the virtual agent.
- Analyze data to identify common questions and areas for improvement.
- Update the virtual agent's knowledge base and capabilities.

#### Permissions

- Access data metrics and analysis features
- Export and filter data
- Manage and update the virtual agent

#### Interactions

- **Target**: Virtual Agent System
  - **Type**: uses
  - **Description**: Use the data metrics and analysis features.
- **Target**: Virtual Agent System
  - **Type**: exports from
  - **Description**: Export and filter data.
- **Target**: Virtual Agent System
  - **Type**: manages
  - **Description**: Manage and update the virtual agent.

### Actor Hierarchy

The actors are organized into three tiers: 1) End-users (Students, Families, Partners, etc.) who interact directly with the virtual agent for information. 2) Support staff (Human Agents) who handle queries escalated by the virtual agent. 3) Administrative staff (Administrators/Analysts) who manage, monitor, and improve the overall system.

### Stakeholder Summary

The primary stakeholder is UC San Diego, the organization procuring the virtual agent. Other key stakeholders are the vendor providing the agent solution and various third-party systems (e.g., Oracle, PaymentWorks, Concur, ServiceNow) that must be integrated with the agent. The successful integration with these backend systems is a critical project dependency.

