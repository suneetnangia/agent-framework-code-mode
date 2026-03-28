import logging
import os
from pathlib import Path

import agent_framework.azure
import azure.identity
from progressive_exposure.agents.orchestrator import orchestrator_agent
from . import subprocess_inline_script_runner
from . import subprocess_file_script_runner

logger = logging.getLogger(__name__)

# Discover skills from the orchestrator 'skills' directory
skills_dir = Path(__file__).parent / "skills"
skill_files = list(skills_dir.glob("*/SKILL.md"))
if not skill_files:
    logger.warning("No valid skills found in %s", skills_dir)
else:
    logger.info("Discovered %d skill(s) in %s", len(skill_files), skills_dir)

run_code_skill = agent_framework.Skill(
    name="run-python-code",
    description=(
        "Executes dynamically generated Python code in an isolated subprocess and returns the output. "
        "Use this skill when the user asks to perform mathematical calculations, data transformations, "
        "string manipulation, algorithmic problem-solving, or any task that benefits from precise "
        "programmatic computation rather than plain-text reasoning. "
        "Also suitable for generating formatted output, validating logic, or prototyping small scripts."
    ),
    content="""
# Run Python Code

## When to use this skill
Use this skill when the user needs to:
- Perform mathematical calculations or numeric analysis
- Run a Python code snippet or prototype a small script
- Do data transformations, string manipulation, or formatting
- Solve algorithmic problems or validate logic programmatically
- Any task that benefits from precise programmatic computation rather than plain-text reasoning

## Usage
Run the `execute` script with the `code` parameter containing the Python source code.
The code runs in an isolated subprocess with a 30-second timeout.

## Limitations
- Maximum code size: 10 KB
- Execution timeout: 30 seconds
- No access to environment variables or secrets
- Output is truncated at 50,000 characters
    """,
)


@run_code_skill.script(
    name="execute",
    description="Execute Python code and return the output.",
)
def execute_code(code: str) -> str:
    return subprocess_inline_script_runner.inline_script_runner(code)


skills_provider = agent_framework._skills.SkillsProvider(
    skill_paths=skills_dir,
    skills=[run_code_skill],
    script_runner=subprocess_file_script_runner.subprocess_script_runner,
)

history_provider = agent_framework.InMemoryHistoryProvider()

chat_client = agent_framework.azure.AzureOpenAIChatClient(
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    credential=azure.identity.DefaultAzureCredential(),
)

agent = orchestrator_agent.OrchestratorAgent(
    chat_client, context_providers=[skills_provider, history_provider]
)
