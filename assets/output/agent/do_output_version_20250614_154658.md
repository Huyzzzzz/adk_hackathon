# DATA_OBJECT_OUTPUT

Generated on: 2025-06-14 15:46:58

## DATA_OBJECT

### User

- **ID**: User
- **Description**: Represents an individual interacting with the Virtual Agent. This entity captures user details such as their role (student, staff, vendor) and authentication status, which helps in personalizing the conversation and managing access control.

### Inquiry/Case

- **ID**: InquiryCase
- **Description**: Represents a user's question, issue, or request submitted to the Virtual Agent. It tracks the entire lifecycle of an inquiry from submission to resolution, including details like status, priority, category, and assignment to human agents if necessary.

### External System

- **ID**: ExternalSystem
- **Description**: Represents external information systems that the Virtual Agent integrates with, such as Oracle for financial data or Concur for travel and expense management. This entity stores connection details and API specifications for seamless data exchange.

### Knowledge Base Article

- **ID**: KnowledgeBaseArticle
- **Description**: Represents a single piece of information or article sourced from an external knowledge base. The Virtual Agent uses these articles to provide accurate and consistent answers to user inquiries. It includes the article's content, keywords, and source.

### Notification

- **ID**: Notification
- **Description**: Represents a message or alert sent to users to provide updates, reminders, or important information. Notifications can be triggered by system events or scheduled, and delivered through various channels.

### Study Abroad Program

- **ID**: StudyAbroadProgram
- **Description**: Represents a specific study abroad program offered by the institution. This entity holds detailed information about programs, including location, duration, eligibility criteria, costs, and application deadlines, which the Virtual Agent can provide to interested students.

