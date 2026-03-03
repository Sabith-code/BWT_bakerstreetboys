# MARS - Memory-Augmented Reasoning System

An autonomous AI engineering agent that combines context recovery and feedback-to-code automation to help developers maintain flow state and automatically address issues.

## Overview

MARS is a persistent, tool-using autonomous AI engineering agent designed to solve two critical developer problems:

1. **Context Loss**: Losing track of what you were working on after interruptions
2. **Manual Bug Fixing**: Manually translating bug reports and test failures into code changes

MARS continuously captures your development context, understands your codebase, and autonomously converts feedback into tested code changes.

## Core Capabilities

### Context Recovery (FlowState)
- Captures open files, code diffs, git commits, and terminal output
- Tracks active files and changes in real-time
- Builds semantic repository models with dependency graphs
- Stores structured reasoning memory across sessions
- Restores complete workflow context after interruptions

### Feedback-to-Code Automation
- Ingests external feedback (bug reports, logs, test failures, feature requests)
- Converts feedback into structured engineering actions
- Executes tools autonomously (read_file, write_file, run_tests)
- Iteratively refines code based on test results
- Detects and prevents infinite reasoning loops
- Produces structured summaries of all changes

## System Architecture

MARS consists of four core subsystems:

### 1. Context Capture Layer (FlowState Core)
Monitors and records:
- Open files and code diffs
- Git commits and terminal output
- Test results and stack traces
- TODO comments and developer intent signals

Builds structured session memory including:
- Active components and WIP logic
- Unresolved errors and pending tasks
- Developer intent and task context

### 2. Repository Understanding Engine
- Parses file structure and builds dependency graphs
- Identifies entry points and code relationships
- Tracks modified modules and function relationships
- Summarizes code responsibilities using static analysis
- Generates embeddings for semantic code search

### 3. Persistent Memory System
Stores across sessions:
- Task summaries and decision history
- Feedback history and code evolution
- Bug fix attempts and partial implementations
- Compressed long-term context
- Structured reasoning logs

### 4. Autonomous Feedback-to-Code Engine (MARS Core)
Executes the autonomous loop:
1. **Analyze**: Map feedback to relevant modules
2. **Plan**: Generate patch plan with specific changes
3. **Execute**: Apply changes using tool actions
4. **Test**: Run tests and capture results
5. **Refine**: Iteratively correct failures
6. **Summarize**: Produce structured change summary

## Key Features

### Resume Work
When you return to your code, MARS provides:
- Summary of your last active task
- Relevant files and specific code regions
- Unresolved errors with stack traces
- Pending TODOs from active files
- Failing tests with failure reasons
- Recent feedback history
- Suggested next steps

### Autonomous Feedback-to-Code Loop
Submit feedback and MARS automatically:
- Analyzes the issue and identifies relevant code
- Plans the necessary changes
- Executes modifications with tool actions
- Runs tests and observes results
- Iteratively corrects failures
- Summarizes all changes made

### Safety & Loop Detection
- Step-by-step reasoning with execution logs
- Tool routing and validation
- Execution limits and loop detection
- Context compression for efficiency
- Sandbox execution for safety

## Tech Stack

- **Language**: Python
- **API Framework**: FastAPI
- **Tool Execution**: Custom tool layer with safety checks
- **Git Integration**: Native git command integration
- **Static Analysis**: AST parsing and code structure analysis
- **Semantic Search**: Embedding-based retrieval
- **Execution Environment**: Local sandbox with resource limits

## Example Scenario

### Scenario 1: Context Recovery
```
1. Developer works on dashboard export feature
2. Modifies ExportComponent.tsx and adds validation logic
3. Gets interrupted by a meeting
4. Returns next day, presses "Resume Work"
5. MARS shows:
   - Last task: "Implementing CSV export with validation"
   - Active files: ExportComponent.tsx, exportUtils.ts
   - Unresolved: Missing null check on line 47
   - Failing test: "should handle empty dataset"
   - Stack trace from last test run
   - Suggested fix: Add null guard before data.map()
```

### Scenario 2: Autonomous Bug Fix
```
1. User submits bug report: "Export crashes when no data selected"
2. MARS automatically:
   - Identifies validation logic in exportUtils.ts
   - Reads the relevant code
   - Plans to add guard clause
   - Applies the fix
   - Runs tests (2 failing → all passing)
   - Fixes edge case in test setup
   - Summarizes: "Added null check in exportData(), fixed 2 tests"
```

## MVP Scope (Hackathon Version)

The initial MVP focuses on demonstrating:

✅ **Implemented Features**:
- Context capture and session memory
- Basic feedback-to-code automation
- Tool execution loop (read, write, test)
- Safety mechanisms and loop detection
- Work resumption with context summary

🚧 **Simulated/Simplified Features**:
- Advanced semantic search (basic keyword matching)
- Full embedding-based retrieval (simplified similarity)
- Complex dependency graph analysis (basic imports only)
- Production-grade sandbox (basic isolation)

## Getting Started

### Prerequisites
- Python 3.9+
- Git
- Virtual environment tool (venv or conda)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd mars

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run MARS
python -m mars.main
```

### Configuration
Create a `mars_config.yaml` file:
```yaml
workspace: /path/to/your/project
loop_detection:
  max_iterations: 10
  repetition_threshold: 3
sandbox:
  timeout: 300
  memory_limit_mb: 512
logging:
  level: INFO
  destination: stdout
```

### API Usage
```bash
# Start the API server
python -m mars.api

# Resume work
curl http://localhost:8000/api/resume

# Submit feedback
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"text": "Export crashes when no data selected", "type": "bug_report"}'

# Check task status
curl http://localhost:8000/api/task/{task_id}
```

## Project Structure

```
mars/
├── context_capture/      # FlowState context capture layer
├── repository/           # Repository understanding engine
├── memory/              # Persistent memory system
├── feedback_engine/     # Autonomous feedback-to-code engine
├── tools/               # Tool execution layer
├── api/                 # FastAPI interface
├── config/              # Configuration management
└── utils/               # Shared utilities

.kiro/specs/mars/        # Project specifications
├── requirements.md      # Feature requirements
├── design.md           # System design (to be created)
└── tasks.md            # Implementation tasks (to be created)
```

## Development Status

This project is currently in the specification phase. The requirements document is complete, and the design and implementation phases are upcoming.

**Current Phase**: Requirements ✅ → Design 🚧 → Implementation ⏳

## Contributing

This is a hackathon project. Contributions are welcome after the initial MVP is complete.

## License

[To be determined]

## Contact

[To be determined]

---

**Note**: MARS is designed to augment developer capabilities, not replace human judgment. Always review automated changes before committing to production.
