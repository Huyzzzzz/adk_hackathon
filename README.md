# 🧠 ADK Hackathon - Multi-Agent AI Assistant Platform

This is a multi-agent system that processes documents and generates business requirements, data objects, actions, and use cases through coordinated AI agents. The system features a React frontend, FastAPI backend, and specialized agents that work together to analyze and extract insights from uploaded documents.

## 📁 Project Structure

```
adk-hackathon/
├── README.md                                       # Main project documentation and setup instructions
├── docker-compose.yml                              # Docker services orchestration for local development
├── .env.example                                    # Template for environment variables
├── .gitignore                                      # Git ignore patterns for the entire project
└── requirements.txt                                # Python dependencies for the entire project

├── frontend/                                       # React Application - User Interface Layer
│   ├── package.json                                # NPM dependencies and scripts for React app
│   ├── package-lock.json                           # Locked versions of NPM dependencies
│   ├── public/                                     # Static assets served directly by the web server
│   │   ├── index.html                              # Main HTML template for React app
│   │   └── favicon.ico                             # Website icon displayed in browser tabs
│   ├── src/                                        # React source code directory
│   │   ├── components/                             # Reusable React components organized by feature
│   │   │   ├── Auth/                               # Authentication-related components
│   │   │   ├── Dashboard/                          # Main dashboard interface components
│   │   │   ├── Chat/                               # Chat interface for user-agent interaction
│   │   │   └── FileUpload/                         # Document upload and management interface
│   │   ├── services/                               # API communication and external service integrations
│   │   ├── hooks/                                  # Custom React hooks for shared logic
│   │   ├── context/                                # React Context providers for global state
│   │   ├── utils/                                  # Utility functions and helpers
│   │   ├── App.tsx                                 # Main React application component and routing
│   │   ├── App.css                                 # Global application styles
│   └── .env                                        # Frontend environment variables (API URLs, keys)

├── backend/                                        # FastAPI Backend System - Core Application Logic
│   ├── app/                                        # Main application package
│   │   ├── main.py                                 # FastAPI application entry point, startup/shutdown events
│   │   ├── config/                                 # Application configuration management
│   │   │   ├── settings.py                         # Application settings, environment variables, constants
│   │   ├── core/                                   # Core application functionality
│   │   │   ├── security.py                         # JWT token handling, password hashing, authentication logic
│   │   │   ├── dependencies.py                     # FastAPI dependency injection functions
│   │   │   └── middleware.py                       # Custom middleware for CORS, logging, request processing
│   │   ├── models/                                 # Database models (ORM layer)
│   │   ├── schemas/                                # Pydantic schemas for request/response validation
│   │   ├── api/                                    # FastAPI route handlers (REST endpoints)
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── auth.py                             # Authentication endpoints (login, register, refresh token)
│   │   │   ├── users.py                            # User management endpoints (profile, preferences)
│   │   │   ├── documents.py                        # Document upload, list, delete, download endpoints
│   │   │   ├── agents.py                           # Agent management and status endpoints
│   │   │   └── chat.py                             # Chat and conversation management endpoints
│   │   ├── services/                               # Business logic layer (service classes)
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── auth_service.py                     # Authentication business logic and user validation
│   │   │   ├── user_service.py                     # User management and profile operations
│   │   │   ├── document_service.py                 # Document processing, storage, and retrieval logic
│   │   │   ├── preprocessing_service.py            # Document content extraction and cleaning
│   │   │   └── orchestrator_service.py             # Multi-agent coordination and task management
│   │   └── utils/                                  # Utility functions and helpers
│   │       ├── __init__.py                         # Package initializer
│   │       ├── file_utils.py                       # File handling, validation, and storage utilities
│   │       ├── text_processing.py                  # Text extraction, cleaning, and preprocessing utilities
│   │       └── exceptions.py                       # Custom exception classes for error handling
│   ├── agents/                                     # Multi-Agent System - AI Agent Implementation
│   │   ├── __init__.py                             #  Package initializer
│   │   ├── base/                                   #  Base classes and shared agent functionality
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── agent.py                            # Abstract base agent class with common methods
│   │   │   ├── tools.py                            # Base tools interface and tool execution framework
│   │   │   └── memory.py                           # Agent memory management and context persistence
│   │   ├── orchestrator/                           # Central coordination agent
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── orchestrator_agent.py               # Main orchestrator agent that coordinates all other agents
│   │   │   ├── coordinator.py                      # Agent coordination and communication logic
│   │   │   └── task_dispatcher.py                  # Task assignment and workflow management
│   │   ├── ur_agent/                               # HR Agent - Handles User Requirements
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── ur_agent.py                         # Main HR agent implementation
│   │   │   ├── tools/                              # HR agent specific tools
│   │   │   │   ├── __init__.py                     # Package initializer
│   │   │   │   ├── extract_information.py          # Tool to extract information from documents
│   │   │   │   ├── get_user_requirementpy          # Tool to retrieve user requirements
│   │   │   │   └── update_user_requirement.py      # Tool to update user requirements
│   │   │   └── prompts/                            # HR agent prompts and templates
│   │   │       └── hr_prompts.py                   # Prompt templates for HR agent interactions
│   │   ├── do_agent/                               # DO Agent - Handles Data Objects
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── do_agent.py                         # Main DO agent implementation
│   │   │   ├── tools/                              # DO agent specific tools
│   │   │   │   ├── __init__.py                     # Package initializer
│   │   │   │   ├── get_user_requirement.py         # Tool to get user requirements from HR agent
│   │   │   │   ├── generate_data_object.py         # Tool to generate data objects
│   │   │   │   └── update_data_objects.py          # Tool to update and manage data objects
│   │   │   └── prompts/                            # DO agent prompts and templates
│   │   │       └── do_prompts.py                   # Prompt templates for DO agent interactions
│   │   ├── ac_agent/                               # AC Agent - Handles Actions
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── ac_agent.py                         # Main AC agent implementation
│   │   │   ├── tools/                              # AC agent specific tools
│   │   │   │   ├── __init__.py                     # Package initializer
│   │   │   │   ├── get_user_requirement.py         # Tool to get user requirements
│   │   │   │   ├── get_data_object.py              # Tool to get data objects from DO agent
│   │   │   │   └── update_actions.py               # Tool to update and manage actions
│   │   │   └── prompts/                            # AC agent prompts and templates
│   │   │       └── ac_prompts.py                   # Prompt templates for AC agent interactions
│   │   └── uc_agent/                               # UC Agent - Handles Use Cases
│       │   ├── __init__.py                         # Package initializer
│       │   ├── uc_agent.py                         # Main UC agent implementation
│       │   ├── tools/                              # UC agent specific tools
│       │   │   ├── __init__.py                     # Package initializer
│       │   │   ├── get_data_object.py              # Tool to get data objects from DO agent
│       │   │   ├── get_actors.py                   # Tool to get actions from AC agent
│       │   │   └── generate_use_case.py            # Tool to generate comprehensive use cases
│       │   └── prompts/                            # UC agent prompts and templates
│       │       └── uc_prompts.py                   # Prompt templates for UC agent interactions
│   ├── data_sources/                               # External Data Source Integrations
│   │   ├── __init__.py                             # Package initializer
│   │   ├── google_cloud/                           # Google Cloud Platform integration
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── storage_client.py                   # Google Cloud Storage operations (upload, download, list)
│   │   │   └── auth.py                             # Google Cloud authentication and credential management
│   │   ├── knowledge_base/                         # Vector database and knowledge management
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── vector_store.py                     # Vector database operations (store, search, retrieve)
│   │   │   └── embeddings.py                       # Text embeddings generation and management
│   ├── database/                                   # Database Management Layer
│   │   ├── __init__.py                             # Package initializer
│   │   ├── connection.py                           # Database connection pool and session management
│   │   ├── migrations/                             # Database schema migrations
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   └── versions/                           # Individual migration files (auto-generated)
│   │   └── repositories/                           # Data Access Layer (Repository Pattern)
│   │       ├── __init__.py                         # Package initializer
│   │       ├── user_repository.py                  # User data access operations
│   │       ├── document_repository.py              # Document metadata and storage operations
│   │       ├── agent_repository.py                 # Agent configuration and state persistence
│   │       └── conversation_repository.py          # Chat conversation data operations
│   ├── memory_store/                               # In-Memory State Management
│   │   ├── __init__.py                             # Package initializer
│   │   ├── firestore_client.py                     # Google Firestore client for persistent state
│   │   ├── redis_client.py                         # Redis client for caching and session management
│   │   └── memory_manager.py                       # Memory state coordination and management
│   ├── tests/                                      # Test Suite
│   │   ├── __init__.py                             # Package initializer
│   │   ├── conftest.py                             # Pytest configuration and shared fixtures
│   │   ├── test_auth.py                            # Authentication system tests
│   │   ├── test_agents/                            # Agent system tests
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── test_orchestrator.py                # Orchestrator agent tests
│   │   │   ├── test_hr_agent.py                    # HR agent functionality tests
│   │   │   ├── test_do_agent.py                    # DO agent functionality tests
│   │   │   ├── test_ac_agent.py                    # AC agent functionality tests
│   │   │   └── test_uc_agent.py                    # UC agent functionality tests
│   │   ├── test_services/                          # Service layer tests
│   │   │   ├── __init__.py                         # Package initializer
│   │   │   ├── test_document_service.py            # Document processing service tests
│   │   │   └── test_preprocessing_service.py       # Preprocessing service tests
│   │   └── test_api/                               # API endpoint tests
│   │       ├── __init__.py                         # Package initializer
│   │       ├── test_auth_endpoints.py              # Authentication endpoint tests
│   │       ├── test_document_endpoints.py          # Document management endpoint tests
│   │       └── test_agent_endpoints.py             # Agent management endpoint tests
│   ├── requirements.txt                            # Python package dependencies for backend
│   ├── Dockerfile                                  # Docker container configuration for backend
│   └── .env                                        # Backend environment variables

├── docs/                                           # Documentation
│   ├── api/
│   ├── architecture/
│   └── user_guides/

└── config/                                         # Configuration Files
    ├── logging.yaml
    ├── agent_config.yaml
    ├── database_config.yaml
    └── environment/
```
