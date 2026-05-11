#!/usr/bin/env python3
"""
Trismegistus Supervisor Agent — Phase 2 Prototype
Orchestrates subagent execution based on intent router output.

Usage:
    python supervisor.py "<query>" [--dry-run]

Example:
    python supervisor.py "Find recent papers on LLM agents"
    python supervisor.py "Fix the bug in deduplicator.py" --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

# Add router to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from router import classify_intent, INTENT_CATEGORIES


def spawn_subagent(query: str, execution_plan: dict, dry_run: bool = False) -> dict:
    """Spawn a subagent via delegate_task or local execution."""
    
    intent = execution_plan["intent"]
    skills = execution_plan["skills"]
    tools = execution_plan["tools"]
    model = execution_plan["model"]
    timeout = execution_plan["timeout"]
    success_criteria = execution_plan["success_criteria"]
    
    print(f"\n{'='*60}")
    print(f"SUPERVISOR: Delegating to {intent.upper()} subagent")
    print(f"{'='*60}")
    print(f"  Query: {query[:80]}...")
    print(f"  Skills: {', '.join(skills)}")
    print(f"  Tools: {', '.join(tools)}")
    print(f"  Model: {model}")
    print(f"  Timeout: {timeout}s")
    print(f"  Success criteria: {success_criteria}")
    
    if dry_run:
        return {
            "status": "dry_run",
            "intent": intent,
            "message": "Would spawn subagent with above configuration",
        }
    
    # For now, we execute locally since delegate_task requires orchestrator role
    # In production, this would use delegate_task with role="orchestrator"
    
    # Build the subagent prompt
    subagent_prompt = f"""You are a specialized {intent} subagent.

Your task: {query}

You have access to these tools: {', '.join(tools)}
You must meet this success criteria: {success_criteria}
You have {timeout} seconds to complete the task.

Execute the task autonomously. Do not ask the user for clarification unless 
a dimension genuinely requires their input (credentials, funds, legal risk).

Report back with:
1. What you did
2. The result/output
3. Whether success criteria were met (yes/no/partial)
4. Any blockers or next steps needed
"""
    
    # For Phase 2, we simulate by printing what would happen
    # In Phase 3, this integrates with actual delegate_task
    
    return {
        "status": "simulated",
        "intent": intent,
        "prompt": subagent_prompt,
        "message": "Subagent execution simulated (Phase 2). Phase 3 will use delegate_task.",
    }


def reflect_on_result(query: str, execution_plan: dict, subagent_result: dict) -> dict:
    """Reflection node: review subagent output before delivery."""
    
    print(f"\n{'='*60}")
    print("REFLECTION NODE: Reviewing subagent output")
    print(f"{'='*60}")
    
    # Simple heuristic reflection (Phase 2)
    # Phase 3 will use LLM-as-judge
    
    status = subagent_result.get("status", "unknown")
    
    reflection = {
        "query": query,
        "intent": execution_plan["intent"],
        "subagent_status": status,
        "checks": {
            "completed": status in ("success", "simulated", "dry_run"),
            "has_output": "output" in subagent_result or "prompt" in subagent_result,
            "meets_criteria": status == "success",  # Heuristic
        },
        "verdict": "PASS" if status in ("success", "simulated", "dry_run") else "NEEDS_REVIEW",
        "risk_level": "low",  # Phase 2 default
        "recommendation": "Deliver to user" if status in ("success", "simulated", "dry_run") else "Escalate to human",
    }
    
    print(f"  Verdict: {reflection['verdict']}")
    print(f"  Risk level: {reflection['risk_level']}")
    print(f"  Recommendation: {reflection['recommendation']}")
    
    return reflection


def human_in_the_loop(reflection: dict, subagent_result: dict) -> dict:
    """Human-in-the-loop for high-risk outputs."""
    
    if reflection["risk_level"] == "high":
        print(f"\n{'='*60}")
        print("HUMAN-IN-THE-LOOP: High-risk task requires approval")
        print(f"{'='*60}")
        print("This task has been flagged for human review.")
        print("Summary:", reflection.get("summary", "See subagent output above"))
        return {
            "status": "paused_for_human",
            "reflection": reflection,
            "subagent_result": subagent_result,
        }
    
    return {
        "status": "approved",
        "reflection": reflection,
        "subagent_result": subagent_result,
    }


def main():
    parser = argparse.ArgumentParser(description="Trismegistus Supervisor Agent")
    parser.add_argument("query", help="User query to process")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("TRISMEGISTUS SUPERVISOR AGENT")
    print(f"{'='*60}")
    print(f"Query: {args.query}")
    
    # Step 1: Intent Classification (Router)
    print(f"\n{'='*60}")
    print("STEP 1: Intent Classification")
    print(f"{'='*60}")
    
    try:
        router_result = classify_intent(args.query)
    except Exception as e:
        print(f"Router failed: {e}")
        sys.exit(1)
    
    execution_plan = router_result["execution_plan"]
    print(f"  Intent: {execution_plan['intent']}")
    print(f"  Confidence: {router_result['classification']['confidence']}")
    print(f"  Reasoning: {router_result['classification']['reasoning']}")
    
    # Step 2: Subagent Delegation
    subagent_result = spawn_subagent(
        args.query,
        execution_plan,
        dry_run=args.dry_run,
    )
    
    # Step 3: Reflection
    reflection = reflect_on_result(args.query, execution_plan, subagent_result)
    
    # Step 4: Human-in-the-loop (if needed)
    final = human_in_the_loop(reflection, subagent_result)
    
    # Final output
    print(f"\n{'='*60}")
    print("FINAL RESULT")
    print(f"{'='*60}")
    
    output = {
        "query": args.query,
        "router": router_result,
        "subagent": subagent_result,
        "reflection": reflection,
        "final": final,
    }
    
    print(json.dumps(output, indent=2))
    
    return output


if __name__ == "__main__":
    main()
