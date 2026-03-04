# FORD – Automated Feedback-to-Code Pipeline

> Turn social media feedback into verified code fixes automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)


FORD is an AI-powered developer productivity system that converts unstructured social media feedback into actionable engineering tasks, automatically generating validated code changes and pull requests. It closes the loop between users and developers by transforming tweets, bug reports, and feature requests into structured issues, test-driven code fixes, and CI-verified pull requests.

---

## The Problem

Modern software teams receive massive amounts of feedback through platforms like X (Twitter), Reddit, Discord, and product communities. However, this feedback pipeline is fundamentally broken:

- **Feedback is unstructured and scattered** across multiple platforms
- **Developers must manually triage** thousands of messages
- **Important issues are missed** in the noise
- **Converting feedback into tickets is time-consuming** and error-prone
- **Users rarely know if their feedback resulted in real fixes**

### Why Existing Tools Fail

| Tool Category | Limitation |
|--------------|------------|
| **Bug Trackers** (Jira, Linear) | Require manual issue creation and lack user context |
| **Customer Support Tools** (Zendesk, Intercom) | Focus on ticket management, not engineering fixes |
| **Social Listening Tools** (Hootsuite, Sprout) | Collect feedback but don't connect to development workflow |
| **AI Coding Assistants** (Copilot, Cursor) | Generate code but lack real user context and feedback signals |

The missing piece is an **automated system that closes the loop from feedback → code → deployment → user update**.

---

## The Solution

FORD creates an **AI-driven feedback-to-engineering pipeline** that treats social media as a direct input channel for CI/CD workflows.

```
Tweets → Issues → Tests → Code → PR → Deployment → User Notification
```

Instead of treating social feedback as noise, FORD treats it as **structured developer input**, creating a closed feedback loop between users and engineering teams.

### What FORD Does Automatically

1. **Collects** user feedback from social media platforms
2. **Understands** and clusters similar issues using AI
3. **Prioritizes** feedback based on engagement and impact
4. **Generates** test-first implementations
5. **Validates** code through CI pipelines
6. **Creates** pull requests with context
7. **Notifies** users when their issues are resolved

---

## Key Features

### 🔄 End-to-End Feedback Automation

Convert social media feedback directly into structured GitHub issues, code patches, and pull requests without manual intervention. FORD monitors configured social platforms, extracts actionable feedback, and initiates the development workflow automatically.

### 🎯 Context-Aware AI Prioritization

Uses engagement signals (likes, retweets, replies) and semantic clustering to determine issue severity. The system analyzes:
- Engagement metrics (viral tweets get higher priority)
- Semantic similarity (clusters related feedback)
- User impact (affected user count)
- Historical patterns (recurring issues)

### 🔐 Secure MCP Tooling

Uses the **Model Context Protocol (MCP)** to safely allow AI agents to interact with developer tools:
- **GitHub**: Issue creation, PR management, code review
- **File Systems**: Safe sandboxed code execution
- **Terminals**: Controlled command execution
- **CI Pipelines**: Automated test validation

MCP provides a security boundary that prevents unauthorized actions while enabling powerful automation.

### 🧪 Test-First Development

AI generates comprehensive unit tests before implementing fixes, ensuring:
- Code correctness through test coverage
- Regression prevention
- Clear specification of expected behavior
- Validation of edge cases

### ✅ CI-Validated Code

Every generated code change passes through automated verification:
- Linting and code style checks
- Unit and integration tests
- Security vulnerability scanning
- Performance regression tests

### 👤 Human-in-the-Loop Control

Developers maintain full control over the automation:
- Review AI-generated pull requests before merging
- Approve or reject proposed changes
- Provide feedback to improve AI suggestions
- Override priority decisions

### 🔔 Closed Feedback Loop

Users are automatically notified when their reported issue is resolved, creating transparency and building trust. Notifications include:
- Link to the merged pull request
- Explanation of the fix
- Timeline from report to resolution

---

## System Architecture

FORD is built as a modular, event-driven system with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                     FORD Architecture                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   X (Twitter)│      │    Reddit    │      │   Discord    │
│   API Client │      │   Scraper    │      │   Webhook    │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Ingestion Layer │
                    │  (Flask Backend) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  AI Analysis     │
                    │  (Grok Models)   │
                    │  • Clustering    │
                    │  • Prioritization│
                    │  • Summarization │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Issue Creation  │
                    │  (GitHub API)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Code Generation │
                    │  (MCP Agent)     │
                    │  • Test Gen      │
                    │  • Implementation│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  CI Validation   │
                    │  (Sandbox)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Pull Request    │
                    │  (GitHub)        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  User Notification│
                    │  (X API)         │
                    └──────────────────┘
```

### Component Breakdown

#### Interface Layer
- **X API Integration**: Real-time tweet collection using streaming API
- **Chrome Extension**: Browser-based feedback capture for any platform
- **GitHub CLI Integration**: Issue creation, commits, and pull request management

#### Backend Core (Flask Orchestrator)

**`grok.py`** - AI Reasoning Engine
- Semantic analysis of feedback
- Issue clustering using embeddings
- Priority scoring and ranking
- Natural language summarization

**`coder.py`** - Code Generation Orchestrator
- Coordinates test generation and implementation
- Manages code review and validation
- Handles multi-file changes
- Integrates with version control

**`sandbox.py`** - Safe Execution Environment
- Isolated code execution
- Resource limits and timeouts
- Security sandboxing
- Dependency management

**`testing.py`** - Automated Test Verification
- Test runner integration
- Coverage analysis
- Regression detection
- Performance benchmarking

#### Data Layer

**PostgreSQL** - Structured Data Storage
- Feedback records
- Issue tracking
- User mappings
- Audit logs

**pgvector (Supabase)** - Semantic Search
- Embedding storage
- Similarity search
- Clustering support
- Fast nearest-neighbor queries

#### AI Intelligence

**Grok-1** - Embeddings and Understanding
- Text embeddings for semantic search
- Sentiment analysis
- Entity extraction

**Grok-4-1 Fast Reasoning** - Planning and Analysis
- Issue prioritization
- Test case generation
- Code review

**Grok Code Fast-1** - Code Generation
- Implementation synthesis
- Refactoring suggestions
- Bug fix generation

---

## System Workflow

```mermaid
flowchart TB
    A[Social Media Feedback] --> B[Chrome Extension / API]
    B --> C[Ingestion Service]
    C --> D[AI Analysis Engine]
    D --> E{Clustering & Prioritization}
    E --> F[GitHub Issue Creation]
    F --> G[Test Generation]
    G --> H[Code Implementation]
    H --> I[Sandbox Execution]
    I --> J{Tests Pass?}
    J -->|No| K[Retry with Feedback]
    K --> H
    J -->|Yes| L[CI Validation]
    L --> M{CI Pass?}
    M -->|No| N[Human Review Required]
    M -->|Yes| O[Create Pull Request]
    O --> P[Human Approval]
    P --> Q[Merge to Main]
    Q --> R[Deploy]
    R --> S[Notify User]
    S --> T[Close Feedback Loop]
```

### Detailed Pipeline Stages

#### 1. INGEST
- Monitor X API for configured keywords and accounts
- Chrome extension captures feedback from any web platform
- Normalize data format across sources
- Deduplicate entries

#### 2. PLAN
- Generate embeddings using Grok-1
- Cluster similar feedback using cosine similarity
- Identify duplicate or related issues
- Group by affected component

#### 3. PRIORITIZE
- Calculate engagement score (likes + retweets + replies)
- Assess severity from content analysis
- Count affected users
- Apply business rules and weights
- Generate priority ranking

#### 4. IMPLEMENT
- Create GitHub issue with full context
- Generate test cases that reproduce the issue
- Implement fix using Grok Code Fast-1
- Ensure code follows project conventions

#### 5. VERIFY
- Run tests in isolated sandbox
- Execute linting and type checking
- Perform security scans
- Validate against CI requirements

#### 6. DEPLOY
- Create pull request with detailed description
- Link to original feedback
- Request human review
- Auto-merge if approved
- Trigger deployment pipeline

#### 7. NOTIFY
- Post reply to original tweet
- Include PR link and fix description
- Thank user for feedback
- Close the feedback loop

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js | Dashboard and admin interface |
| | TailwindCSS | Responsive UI styling |
| | Chrome Extension API | Browser-based feedback capture |
| **Backend** | Flask (Python) | API orchestration and routing |
| | asyncio | Async event processing |
| | Celery | Background task queue |
| **Database** | PostgreSQL | Structured data storage |
| | pgvector (Supabase) | Vector embeddings and similarity search |
| | Redis | Caching and session management |
| **AI Models** | Grok-1 | Embeddings and semantic understanding |
| | Grok-4-1 Fast Reasoning | Planning, analysis, and prioritization |
| | Grok Code Fast-1 | Code generation and fixes |
| **Integrations** | X API v2 | Tweet collection and posting |
| | GitHub CLI | Issue and PR management |
| | GitHub Actions | CI/CD automation |
| **Automation** | Model Context Protocol (MCP) | Safe AI-tool interaction |
| | Docker | Sandboxed execution |

---

## Project Structure

```
ford/
│
├── backend/
│   ├── agent/              # Core AI agent logic
│   │   ├── agent.py        # Main agent orchestrator
│   │   └── events.py       # Event system
│   ├── client/             # LLM client integration
│   │   └── llm_client.py   # Grok API wrapper
│   ├── tools/              # MCP tool implementations
│   │   ├── github.py       # GitHub operations
│   │   ├── sandbox.py      # Code execution
│   │   └── testing.py      # Test runner
│   ├── coder.py            # Code generation orchestrator
│   ├── grok.py             # AI reasoning engine
│   ├── app.py              # Flask API server
│   └── main.py             # CLI entry point
│
├── extension/              # Chrome extension
│   ├── manifest.json       # Extension config
│   ├── background.js       # Service worker
│   ├── content.js          # Page scraping
│   ├── popup.html          # UI
│   └── config.js           # Settings
│
├── frontend/               # Next.js dashboard
│   ├── components/         # React components
│   ├── pages/              # Next.js pages
│   ├── styles/             # CSS modules
│   └── lib/                # Utilities
│
├── database/
│   ├── schema.sql          # PostgreSQL schema
│   ├── migrations/         # Database migrations
│   └── seed.sql            # Sample data
│
├── scripts/
│   ├── setup.sh            # Environment setup
│   └── deploy.sh           # Deployment script
│
├── docker/
│   ├── Dockerfile          # Container definition
│   └── docker-compose.yml  # Multi-container setup
│
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
└── README.md               # This file
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Git
- Chrome browser (for extension)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/ford.git
cd ford
```

### Step 2: Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
```

Required environment variables:

```env
# AI Models
GROK_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-4-1-fast

# X (Twitter) API
X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_SECRET=your_access_secret

# GitHub
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=username/repository

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ford
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Flask
FLASK_SECRET_KEY=your_random_secret_key
FLASK_ENV=development
```

### Step 4: Database Setup

```bash
# Create database
createdb ford

# Run migrations
psql -d ford -f database/schema.sql

# Enable pgvector extension
psql -d ford -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Step 5: Start Backend

```bash
# Development mode
python backend/app.py

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

Backend will be available at `http://localhost:5000`

### Step 6: Frontend Setup (Optional)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Step 7: Chrome Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension/` directory
5. Click the extension icon and configure:
   - API URL: `http://localhost:5000`
   - Keywords: `bug, issue, broken, crash, error, help`
   - Monitored Accounts: `@YourProduct`
6. Click "Save Configuration"

---

## Usage Example

### Real-World Workflow

**User tweets:**
```
@YourProduct Login keeps failing on Android app. 
Getting "null response" error every time I try to sign in.
```

**FORD automatically:**

1. **Detects tweet** via X API monitoring
2. **Analyzes content** using Grok-1:
   - Platform: Android
   - Component: Authentication
   - Error: Null response handling
   - Severity: High (blocks core functionality)

3. **Clusters feedback** with similar issues:
   - Found 3 other users reporting same issue
   - All on Android
   - Started 2 days ago

4. **Creates GitHub issue** #247:
   ```markdown
   ## Login Failure on Android - Null Response Error
   
   **Reported by:** 4 users
   **Platform:** Android
   **Component:** Authentication
   **Priority:** High
   
   ### User Feedback
   - @user1: "Login keeps failing on Android..."
   - @user2: "Can't sign in, null error"
   - @user3: "Android login broken"
   
   ### Analysis
   Null response suggests API timeout or network error 
   not being handled gracefully in Android client.
   ```

5. **Generates test** `test_login_null_response()`:
   ```python
   def test_login_null_response():
       """Test login handles null API response gracefully"""
       client = AuthClient()
       
       # Simulate null response
       with mock.patch('api.post', return_value=None):
           result = client.login('user@example.com', 'password')
           
       # Should return error, not crash
       assert result.success == False
       assert result.error == 'Network error, please try again'
       assert result.exception is None
   ```

6. **Implements fix** in `auth_client.py`:
   ```python
   def login(self, email: str, password: str) -> LoginResult:
       try:
           response = api.post('/auth/login', {
               'email': email,
               'password': password
           })
           
           # FIX: Handle null response
           if response is None:
               return LoginResult(
                   success=False,
                   error='Network error, please try again'
               )
           
           return LoginResult(success=True, token=response.token)
       except Exception as e:
           logger.error(f'Login failed: {e}')
           return LoginResult(success=False, error=str(e))
   ```

7. **Runs CI validation**:
   ```
   ✓ test_login_null_response PASSED
   ✓ test_login_success PASSED
   ✓ test_login_invalid_credentials PASSED
   ✓ Linting passed
   ✓ Type checking passed
   ```

8. **Creates pull request** #248:
   ```markdown
   ## Fix: Handle null response in Android login
   
   Fixes #247
   
   ### Changes
   - Added null check in AuthClient.login()
   - Returns user-friendly error message
   - Added test coverage
   
   ### Testing
   - All existing tests pass
   - New test covers null response case
   
   ### User Impact
   Resolves login failures for 4+ users on Android
   ```

9. **Notifies users** after merge:
   ```
   @user1 Thanks for reporting! We've fixed the Android 
   login issue. Update should be live in the next release.
   
   Fix details: https://github.com/yourorg/repo/pull/248
   ```

---

## Roadmap

### Phase 1: Core Pipeline (Current)
- [x] X (Twitter) feedback collection
- [x] AI-powered issue clustering
- [x] Automated GitHub issue creation
- [x] Test-first code generation
- [x] CI validation
- [x] Pull request automation

### Phase 2: Multi-Platform Support (Q2 2026)
- [ ] Reddit integration
- [ ] Discord webhook support
- [ ] Slack community monitoring
- [ ] Email feedback parsing
- [ ] In-app feedback widget

### Phase 3: Advanced Intelligence (Q3 2026)
- [ ] Autonomous issue clustering without supervision
- [ ] Predictive issue detection (catch bugs before users report)
- [ ] Code review automation
- [ ] Performance regression detection
- [ ] Security vulnerability scanning

### Phase 4: Production Scale (Q4 2026)
- [ ] Multi-repository support
- [ ] Team collaboration features
- [ ] Custom workflow definitions
- [ ] Advanced analytics dashboard
- [ ] Enterprise SSO integration

### Phase 5: DevOps Integration (2027)
- [ ] Kubernetes deployment automation
- [ ] Infrastructure-as-code generation
- [ ] Monitoring and alerting integration
- [ ] Rollback automation
- [ ] A/B testing framework

---

## Hackathon Context

This project was developed for the **AI for Bharat Hackathon 2026** in the **Student Track: AI for Learning and Developer Productivity**.

### Problem Statement Addressed

How can AI improve developer productivity by automating the feedback-to-code pipeline and closing the loop between users and engineering teams?

### Innovation Highlights

1. **Novel Application of MCP**: First system to use Model Context Protocol for safe AI-driven code generation in production workflows

2. **Closed Feedback Loop**: Unlike existing tools, FORD notifies users when their feedback results in actual fixes

3. **Context-Aware Prioritization**: Uses social engagement signals as a proxy for issue severity

4. **Test-First AI**: Generates tests before implementation, ensuring correctness

5. **Production-Ready**: Not just a demo—designed for real engineering teams

### Impact Metrics

- **Time Saved**: Reduces feedback-to-fix cycle from days to hours
- **User Satisfaction**: Users see their feedback result in real changes
- **Developer Focus**: Eliminates manual triage and ticket creation
- **Code Quality**: Test-first approach ensures robust fixes

---

## Contributing

We welcome contributions from the community! Here's how you can help:

### Areas for Contribution

- **New Platform Integrations**: Add support for Reddit, Discord, Slack
- **AI Model Improvements**: Enhance clustering and prioritization algorithms
- **Testing**: Expand test coverage and add integration tests
- **Documentation**: Improve guides and add tutorials
- **Bug Fixes**: Help us squash bugs and improve stability

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Commit with clear messages: `git commit -m 'Add amazing feature'`
7. Push to your fork: `git push origin feature/amazing-feature`
8. Open a pull request

### Code Standards

- Follow PEP 8 for Python code
- Use type hints for all functions
- Write docstrings for public APIs
- Maintain test coverage above 80%
- Run linting before committing: `flake8 backend/`

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 FORD Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Acknowledgements

This project was made possible by:

- **AI for Bharat Hackathon** - For providing the platform and inspiration
- **AWS** - Cloud infrastructure and services
- **Grok AI** - Advanced language models for reasoning and code generation
- **Model Context Protocol** - Safe AI-tool interaction framework
- **Open Source Community** - Flask, PostgreSQL, Next.js, and countless other tools

Special thanks to all contributors and early adopters who provided feedback and helped shape FORD into a production-ready system.

---

## Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/ford/issues)
- **Discussions**: [Join the community](https://github.com/yourusername/ford/discussions)
- **Email**: ford-support@example.com
- **Twitter**: [@FORDDevTools](https://twitter.com/FORDDevTools)

---

<div align="center">

**Built with ❤️ for developers who listen to their users**

[Documentation](https://ford-docs.example.com) • [Demo](https://ford-demo.example.com) • [Blog](https://ford-blog.example.com)

</div>
