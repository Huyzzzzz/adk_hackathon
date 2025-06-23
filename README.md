# 🧠 ADK Hackathon - Multi-Agent AI Assistant Platform

This is a multi-agent system that processes documents and generates business requirements, data objects, actions, and use cases through coordinated AI agents. The system features a React frontend, FastAPI backend, and specialized agents that work together to analyze and extract insights from uploaded documents.

## 📁 Project Structure

```text
adk-hackathon/
├── README.md                                       # Main project documentation and setup instructions
├── .gitignore                                      # Git ignore patterns for the entire project
├── .env.example                                    # Template for environment variables configuration
├── requirements.txt                                # Python dependencies for the entire project
├── pyproject.toml                                  # Project configuration and dependencies (for uv)
├── uv.lock                                         # Locked dependencies (when using uv)
├── Dockerfile                                      # Docker container configuration
├── deploy.sh                                       # Google Cloud Run deployment script
├── main.py                                         # FastAPI application entry point
├── test.py                                         # Test script for the application
│
└── BA/                                             # Main Business Analyst Agent Module
    ├── __init__.py                                 # Package initializer
    ├── agent.py                                    # Main orchestrator agent implementation
    ├── prompt.py                                   # Orchestrator agent prompts
    │
    ├── config/                                     # Configuration management
    │   └── __init__.py                             # Configuration settings and constants
    │
    ├── sub_agents/                                 # Specialized Sub-Agents
    │   ├── __init__.py                             # Sub-agents package initializer
    │   │
    │   ├── ur_agent/                               # User Requirements (UR) Agent
    │   │   ├── __init__.py                         # UR agent package initializer
    │   │   ├── agent.py                            # UR agent implementation
    │   │   └── prompt.py                           # UR agent prompts
    │   │
    │   ├── do_agent/                               # Data Objects (DO) Agent
    │   │   ├── __init__.py                         # DO agent package initializer
    │   │   ├── agent.py                            # DO agent implementation
    │   │   └── prompt.py                           # DO agent prompts
    │   │
    │   ├── ac_agent/                               # Actions (AC) Agent
    │   │   ├── __init__.py                         # AC agent package initializer
    │   │   ├── agent.py                            # AC agent implementation
    │   │   └── prompt.py                           # AC agent prompts
    │   │
    │   └── uc_agent/                               # Use Cases (UC) Agent
    │       ├── __init__.py                         # UC agent package initializer
    │       ├── agent.py                            # UC agent implementation
    │       └── prompt.py                           # UC agent prompts
    │
    ├── tools/                                      # Shared Tools and Utilities
    │   ├── __init__.py                             # Tools package initializer
    │   ├── file.py                                 # File handling operations
    │   ├── parsing.py                              # Document parsing utilities
    │   ├── storage.py                              # Storage operations and management
    │   └── save_agent_ouput.py                     # Agent output saving utilities
    │
    └── utils/                                      # General Utilities
        ├── __init__.py                             # Utils package initializer
        └── utils.py                                # Helper functions and utilities
```

## 🏗️ Architecture Overview

This project uses the Google ADK (Agent Development Kit) framework to build a multi-agent system. The architecture consists of:

1. **Main Orchestrator Agent** (`BA/agent.py`) - Coordinates all sub-agents and manages the overall workflow
2. **Specialized Sub-Agents**:
   - **UR Agent** - Extracts and manages user requirements from documents
   - **DO Agent** - Identifies and structures data objects
   - **AC Agent** - Defines actions and operations
   - **UC Agent** - Generates comprehensive use cases

Each agent has its own:

- Implementation file (`agent.py`)
- Prompt templates (`prompt.py`)
- Specific tools and utilities

The system processes uploaded documents through these agents in a coordinated manner to produce structured business requirements and specifications.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI)
- Google Cloud Project with the following APIs enabled:
  - Vertex AI API
  - Cloud Run API
  - Cloud Storage API (if using GCS)
- Google API Key or Service Account credentials

### Environment Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd adk-hackathon
   ```

2. **Set up Python environment:**

   ```bash
   # Using venv
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Or using uv (if you have it installed)
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   # Or using uv
   uv sync
   ```

4. **Configure environment variables:**

   ```bash
   # Copy the env template
   cp .env.example .env

   # Edit .env with your values:
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"
   export GOOGLE_GENAI_USE_VERTEXAI=True
   export GOOGLE_API_KEY="your-api-key"
   export BA_VISTA_COORDINATOR_MODEL=gemini-2.5-pro
   export UR_AGENT_MODEL=gemini-2.5-pro
   export DO_AGENT_MODEL=gemini-2.5-pro
   export AC_AGENT_MODEL=gemini-2.5-pro
   export UC_AGENT_MODEL=gemini-2.5-pro

   # Load the environment variables
   source .env
   ```

## 💻 Running Locally

### Start the Backend Server

1. **Activate your virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Run the ADK Web UI or ADK in terminal:**

   ```bash
   adk web

   # or

   adk run BA
   ```

## ☁️ Google Cloud Run Deployment

### Prerequisites for Cloud Run

1. **Install and configure Google Cloud SDK:**

   ```bash
   # Install gcloud CLI (if not already installed)
   # Follow: https://cloud.google.com/sdk/docs/install

   # Authenticate
   gcloud auth login

   # Set your project
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable required APIs:**

   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   ```

### Deploy to Cloud Run

1. **Using the deployment script:**

   ```bash
   # Make sure environment variables are set
   source .env

   # Run the deployment script
   chmod +x deploy.sh
   ./deploy.sh
   ```

2. **Manual deployment:**

   ```bash
   gcloud run deploy business-analyst-service \
     --source . \
     --region us-central1 \
     --project YOUR_PROJECT_ID \
     --allow-unauthenticated \
     --set-env-vars="GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_API_KEY=YOUR_API_KEY,BA_VISTA_COORDINATOR_MODEL=gemini-2.5-pro,UR_AGENT_MODEL=gemini-2.5-pro,DO_AGENT_MODEL=gemini-2.5-pro,AC_AGENT_MODEL=gemini-2.5-pro,UC_AGENT_MODEL=gemini-2.5-pro" \
     --timeout 1200
   ```

3. **Access your deployed service:**
   - After deployment, you'll receive a service URL
   - Visit: `https://business-analyst-service-148093331204.us-central1.run.app`

## 🔧 Configuration

### Model Configuration

You can configure different AI models for each agent by modifying the environment variables:

- `BA_VISTA_COORDINATOR_MODEL`: Model for the Business Analyst coordinator
- `UR_AGENT_MODEL`: Model for User Requirements agent
- `DO_AGENT_MODEL`: Model for Data Objects agent
- `AC_AGENT_MODEL`: Model for Actions agent
- `UC_AGENT_MODEL`: Model for Use Cases agent

Available models:

- `gemini-2.5-pro` (recommended)
- `gemini-2.0-flash`

### CORS Configuration

Update `ALLOWED_ORIGINS` in `main.py` to configure CORS for your frontend:

```python
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
