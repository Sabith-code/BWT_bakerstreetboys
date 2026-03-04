import asyncio
import os
import subprocess
from tools.base import Tool, ToolConfirmation, ToolInvocation, ToolKind, ToolResult
from pydantic import BaseModel, Field
from typing import Optional

class GitHubIssueParams(BaseModel):
    repo: str = Field(..., description="Repository in format owner/repo (e.g., Sameerwalikar/x_ford)")
    title: str = Field(..., description="Issue title")
    body: Optional[str] = Field(None, description="Issue body/description")
    labels: Optional[str] = Field(None, description="Comma-separated labels (optional)")

class GitHubCreateIssueTool(Tool):
    name = "github_create_issue"
    kind = ToolKind.SHELL
    description = "Create a GitHub issue using GitHub CLI (gh). Requires GH_TOKEN environment variable to be set."
    
    schema = GitHubIssueParams
    
    async def execute(self, invocation: ToolInvocation) -> ToolResult:
        params = GitHubIssueParams(**invocation.params)
        
        try:
            # Build the gh command
            cmd = [
                "C:\\Program Files\\GitHub CLI\\gh.exe",
                "issue",
                "create",
                "--repo", params.repo,
                "--title", params.title,
            ]
            
            if params.body:
                cmd.extend(["--body", params.body])
            
            if params.labels:
                cmd.extend(["--label", params.labels])
            
            # Run the command with token
            env = {**os.environ}
            if "GH_TOKEN" not in env:
                return ToolResult(
                    success=False,
                    output="Error: GH_TOKEN environment variable not set. Please set your GitHub token."
                )
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return ToolResult(
                    success=True,
                    output=result.stdout.strip()
                )
            else:
                return ToolResult(
                    success=False,
                    output=f"GitHub CLI error: {result.stderr.strip()}"
                )
                
        except FileNotFoundError:
            return ToolResult(
                success=False,
                output="Error: GitHub CLI (gh) is not installed. Please install it using: winget install GitHub.cli"
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output="Error: GitHub CLI command timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=f"Error: {str(e)}"
            )


class GitHubListReposParams(BaseModel):
    limit: int = Field(10, ge=1, le=100, description="Number of repos to list (default: 10)")

class GitHubListReposTool(Tool):
    name = "github_list_repos"
    kind = ToolKind.SHELL
    description = "List your GitHub repositories using GitHub CLI (gh)."
    
    schema = GitHubListReposParams
    
    async def execute(self, invocation: ToolInvocation) -> ToolResult:
        params = GitHubListReposParams(**invocation.params)
        
        try:
            cmd = [
                "C:\\Program Files\\GitHub CLI\\gh.exe",
                "repo",
                "list",
                "--limit", str(params.limit),
            ]
            
            env = {**os.environ}
            if "GH_TOKEN" not in env:
                return ToolResult(
                    success=False,
                    output="Error: GH_TOKEN environment variable not set."
                )
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return ToolResult(
                    success=True,
                    output=result.stdout.strip()
                )
            else:
                return ToolResult(
                    success=False,
                    output=f"GitHub CLI error: {result.stderr.strip()}"
                )
                
        except FileNotFoundError:
            return ToolResult(
                success=False,
                output="Error: GitHub CLI (gh) is not installed."
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=f"Error: {str(e)}"
            )
