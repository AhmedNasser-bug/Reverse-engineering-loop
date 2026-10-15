"""
Orchestration Engine for the Reverse Engineering Loop Harness.
Wires together Honcho memory, MCP server tools, active skills, and agent rules.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

# Ensure local imports work cleanly
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from 03_orchestration.honcho.honcho_client import HonchoMemoryManager if False else None  # Dynamic import below

class Orchestrator:
    def __init__(self, session_id: str = "default-loop-session"):
        self.project_root = PROJECT_ROOT
        self.orchestration_dir = CURRENT_DIR
        self.skills_dir = CURRENT_DIR / "skills"
        self.mcp_config_path = CURRENT_DIR / "mcp" / "mcp-config.json"
        self.rules_dir = CURRENT_DIR / "rules"
        
        # Initialize Honcho memory
        from importlib.machinery import SourceFileLoader
        honcho_client_file = str(CURRENT_DIR / "honcho" / "honcho_client.py")
        honcho_module = SourceFileLoader("honcho_client", honcho_client_file).load_module()
        self.memory = honcho_module.HonchoMemoryManager(session_id=session_id)

    def list_available_skills(self) -> List[str]:
        """Returns names of all packaged skills in 03-orchestration/skills."""
        if not self.skills_dir.exists():
            return []
        skills = []
        for item in self.skills_dir.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                skills.append(item.name)
        return sorted(skills)

    def get_skill_instructions(self, skill_name: str) -> Optional[str]:
        """Reads the SKILL.md of a given skill."""
        skill_file = self.skills_dir / skill_name / "SKILL.md"
        if skill_file.exists():
            return skill_file.read_text(encoding="utf-8")
        return None

    def get_orchestration_rules(self) -> str:
        """Loads and consolidates all rules from 03-orchestration/rules."""
        rule_texts = []
        if self.rules_dir.exists():
            for rule_file in sorted(self.rules_dir.glob("*.md")):
                rule_texts.append(f"--- RULE: {rule_file.name} ---\n" + rule_file.read_text(encoding="utf-8"))
        return "\n\n".join(rule_texts)

    def load_mcp_config(self) -> Dict[str, Any]:
        """Loads the consolidated MCP server configuration."""
        if self.mcp_config_path.exists():
            with open(self.mcp_config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"mcpServers": {}}

    def compose_agent_system_prompt(self, agent_role: str, specific_skills: Optional[List[str]] = None) -> str:
        """
        Dynamically composes a high-context system prompt incorporating:
        1. Agent role and responsibilities
        2. Relevant packaged skills
        3. Mandatory loop rules (invariant, reverse engineering, memory)
        4. Distilled Honcho memory state
        """
        skills_to_include = specific_skills or ["rea", "loop-engineering", "openui", "honcho-memory"]
        skills_content = []
        for s in skills_to_include:
            inst = self.get_skill_instructions(s)
            if inst:
                skills_content.append(f"### SKILL: {s}\n{inst}\n")

        memory_context = self.memory.get_context_for_prompt()
        rules = self.get_orchestration_rules()

        prompt_parts = [
            f"# AGENT ROLE: {agent_role}",
            "You are an expert agent operating within the Reverse Engineering Loop Harness.",
            "\n## ORCHESTRATION RULES & PROTOCOLS:",
            rules,
            "\n## PERSISTENT STATE & MEMORY (HONCHO):",
            memory_context,
            "\n## LOADED SKILLS & CAPABILITIES:",
            "\n".join(skills_content) if skills_content else "Default operational skills loaded."
        ]
        return "\n\n".join(prompt_parts)


if __name__ == "__main__":
    orch = Orchestrator()
    print("Available Skills:", orch.list_available_skills())
    print("\nComposing sample system prompt:")
    sample_prompt = orch.compose_agent_system_prompt("Worker Agent")
    print(sample_prompt[:500] + "...\n[Truncated for brevity]")
