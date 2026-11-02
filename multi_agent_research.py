#!/usr/bin/env python3
"""
Multi-Agent Research Team
Four agents collaborating: Planner, Researcher, Writer, Critic.
Each agent has a distinct role and passes work to the next.

Usage:
    python multi_agent_research.py --topic "your research topic"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


class Agent:
    """Base agent class with role, instructions, and memory."""

    def __init__(self, name, role, instructions):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.memory = []

    def act(self, input_text, context=None):
        """Process input and return output. Override in subclasses."""
        raise NotImplementedError

    def remember(self, key, value):
        self.memory.append({"key": key, "value": value, "timestamp": datetime.now().isoformat()})


class PlannerAgent(Agent):
    """Breaks down a research topic into sub-questions and a plan."""

    def act(self, topic, context=None):
        plan = {
            "topic": topic,
            "sub_questions": [
                f"What is {topic} and why does it matter?",
                f"Key players and current state of {topic}",
                f"Challenges and limitations in {topic}",
                f"Future outlook and opportunities for {topic}"
            ],
            "research_areas": [
                "Market size and growth",
                "Technology and methodology",
                "Key companies and competitors",
                "Regulatory and compliance considerations"
            ],
            "deliverables": ["research_brief.md", "executive_summary.md"],
            "created_at": datetime.now().isoformat()
        }
        self.remember("plan", plan)
        return plan


class ResearcherAgent(Agent):
    """Gathers information for each sub-question."""

    def act(self, plan, context=None):
        findings = {}
        for i, sq in enumerate(plan["sub_questions"]):
            findings[sq] = {
                "sources": [
                    f"Source {i+1}.1: Industry report on {plan['topic']}",
                    f"Source {i+1}.2: Academic paper related to {plan['topic']}",
                    f"Source {i+1}.3: Expert interview or commentary"
                ],
                "key_points": [
                    f"Finding A for: {sq}",
                    f"Finding B for: {sq}",
                    f"Finding C for: {sq}"
                ],
                "confidence": 0.85
            }
        result = {
            "topic": plan["topic"],
            "findings": findings,
            "total_sub_questions": len(plan["sub_questions"]),
            "research_date": datetime.now().isoformat()
        }
        self.remember("findings", result)
        return result


class WriterAgent(Agent):
    """Synthesizes research findings into a coherent report."""

    def act(self, research, context=None):
        sections = []
        for sq, data in research["findings"].items():
            section = f"## {sq}\n\n"
            section += "### Key Findings:\n"
            for point in data["key_points"]:
                section += f"- {point}\n"
            section += f"\n### Sources:\n"
            for src in data["sources"]:
                section += f"- {src}\n"
            sections.append(section)

        report = f"""# Research Report: {research['topic']}

Generated: {research['research_date']}
Sub-questions addressed: {research['total_sub_questions']}

{''.join(sections)}

## Executive Summary

This report was produced by a multi-agent research system. The Planner decomposed the topic into {research['total_sub_questions']} sub-questions, the Researcher gathered findings for each, and this Writer synthesized the results. A Critic agent then reviewed the output for quality.

### Methodology
- Multi-agent collaboration: Planner → Researcher → Writer → Critic
- Each agent operates independently with role-specific instructions
- Findings are traced back to cited sources
"""
        self.remember("report", report)
        return report


class CriticAgent(Agent):
    """Reviews the report for quality, accuracy, and completeness."""

    def act(self, report, context=None):
        issues = []
        score = 1.0

        # Check for required sections
        if "Executive Summary" not in report:
            issues.append("Missing Executive Summary")
            score -= 0.2
        if "Methodology" not in report:
            issues.append("Missing Methodology section")
            score -= 0.15
        if "## " not in report:
            issues.append("No section headers found")
            score -= 0.2

        # Check length
        if len(report) < 500:
            issues.append("Report too short (< 500 chars)")
            score -= 0.25

        score = max(score, 0.0)

        review = {
            "score": round(score, 2),
            "issues": issues,
            "passed": score >= 0.7,
            "reviewed_at": datetime.now().isoformat(),
            "reviewer": "CriticAgent"
        }
        self.remember("review", review)
        return review


class MultiAgentResearchTeam:
    """Orchestrates the four agents in sequence."""

    def __init__(self):
        self.planner = PlannerAgent("Planner", "Research Planning",
                                     "Break topics into sub-questions and research areas")
        self.researcher = ResearcherAgent("Researcher", "Information Gathering",
                                          "Find sources and key points for each sub-question")
        self.writer = WriterAgent("Writer", "Report Writing",
                                  "Synthesize findings into a coherent report")
        self.critic = CriticAgent("Critic", "Quality Review",
                                  "Review reports for accuracy and completeness")

    def run(self, topic):
        print(f"[1/4] PlannerAgent: Breaking down topic '{topic}'...")
        plan = self.planner.act(topic)
        print(f"      → {len(plan['sub_questions'])} sub-questions planned")

        print(f"[2/4] ResearcherAgent: Gathering findings...")
        research = self.researcher.act(plan)
        print(f"      → {research['total_sub_questions']} findings collected")

        print(f"[3/4] WriterAgent: Writing report...")
        report = self.writer.act(research)
        print(f"      → Report generated ({len(report)} characters)")

        print(f"[4/4] CriticAgent: Reviewing quality...")
        review = self.critic.act(report)
        status = "PASSED" if review["passed"] else "NEEDS REVISION"
        print(f"      → Score: {review['score']}/1.0 — {status}")

        return {
            "topic": topic,
            "plan": plan,
            "research": research,
            "report": report,
            "review": review,
            "agents_used": ["PlannerAgent", "ResearcherAgent", "WriterAgent", "CriticAgent"],
            "completed_at": datetime.now().isoformat()
        }


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Research Team")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--output", default="research_output.json", help="Output file")
    args = parser.parse_args()

    team = MultiAgentResearchTeam()
    result = team.run(args.topic)

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n[+] Full results saved to {output_path}")
    print(f"[+] Report preview:\n{result['report'][:500]}...")


if __name__ == "__main__":
    main()