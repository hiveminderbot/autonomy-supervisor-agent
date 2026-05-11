#!/usr/bin/env python3
"""
Trismegistus Supervisor Agent — Phase 3: Live Subagent Delegation
Replaces simulated subagents with actual subprocess-based delegation.

Since delegate_task requires a parent_agent context that is only available
inside the Hermes runtime, Phase 3 uses subprocess execution of the Hermes
CLI with a crafted prompt to achieve real delegation.

Usage:
    python supervisor_phase3.py "<query>" [--dry-run]

Example:
    python supervisor_phase3.py "Find recent papers on LLM agents"
    python supervisor_phase3.py "Fix the bug in deduplicator.py" --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import time

# Add router to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from router import classify_intent, INTENT_CATEGORIES


def run_hermes_subagent(query: str, execution_plan: dict, timeout: int = 120) -> dict:
    """Run a real subagent via Hermes CLI subprocess."""
    
    intent = execution_plan["intent"]
    skills = execution_plan["skills"]
    tools = execution_plan["tools"]
    model = execution_plan["model"]
    success_criteria = execution_plan["success_criteria"]
    
    # Build a focused prompt for the subagent
    subagent_prompt = f"""You are a specialized {intent} subagent.

Your task: {query}

You have access to these tools: {', '.join(tools)}
You must meet this success criteria: {success_criteria}

Execute the task autonomously. Do not ask the user for clarification unless 
a dimension genuinely requires their input (credentials, funds, legal risk).

Report back with:
1. What you did (2-3 sentences)
2. The result/output (include URLs, file paths, or code snippets)
3. Whether success criteria were met (yes/no/partial)
4. Any blockers or next steps needed

Be concise but thorough. If research, include at least 3 sources with URLs.
If code, include the git diff or test results.
"""
    
    # Run hermes CLI with the subagent prompt
    # Use --quiet to reduce noise, --no-memory to avoid polluting memory
    hermes_bin = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/hermes")
    if not os.path.exists(hermes_bin):
        # Try system hermes
        hermes_bin = "hermes"
    
    cmd = [
        hermes_bin,
        "chat",
        "-q", subagent_prompt,
        "-m", model,
        "--provider", "openrouter",
        "-Q",
        "--yolo",
        "--max-turns", "8",
    ]
    
    print(f"\n{'='*60}")
    print(f"SUPERVISOR: Delegating to {intent.upper()} subagent (LIVE)")
    print(f"{'='*60}")
    print(f"  Query: {query[:80]}...")
    print(f"  Skills: {', '.join(skills)}")
    print(f"  Tools: {', '.join(tools)}")
    print(f"  Model: {model}")
    print(f"  Timeout: {timeout}s")
    print(f"  Success criteria: {success_criteria}")
    print(f"  Command: {' '.join(cmd[:3])} ...")
    
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        elapsed = time.time() - start
        
        output = result.stdout + result.stderr
        
        # Determine success heuristically
        success = result.returncode == 0 and len(output) > 50
        
        return {
            "status": "success" if success else "failed",
            "intent": intent,
            "output": output[:2000],  # Truncate for JSON safety
            "returncode": result.returncode,
            "elapsed_seconds": round(elapsed, 2),
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return {
            "status": "timeout",
            "intent": intent,
            "output": f"Subagent timed out after {timeout}s",
            "elapsed_seconds": round(elapsed, 2),
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "intent": intent,
            "output": f"Hermes CLI not found at {hermes_bin}",
            "elapsed_seconds": 0,
        }


def reflect_on_result(query: str, execution_plan: dict, subagent_result: dict) -> dict:
    """Reflection node: review subagent output before delivery."""
    
    print(f"\n{'='*60}")
    print("REFLECTION NODE: Reviewing subagent output")
    print(f"{'='*60}")
    
    status = subagent_result.get("status", "unknown")
    output = subagent_result.get("output", "")
    intent = execution_plan["intent"]
    
    # Intent-specific validation
    checks = {
        "completed": status == "success",
        "has_output": len(output) > 50,
        "meets_criteria": False,
    }
    
    if intent == "research":
        # Check for URLs in output
        import re
        urls = re.findall(r'https?://[^\s\)\"\'\>]+', output)
        checks["meets_criteria"] = len(urls) >= 3
        checks["url_count"] = len(urls)
    elif intent == "code":
        checks["meets_criteria"] = "test" in output.lower() or "diff" in output.lower() or "fix" in output.lower()
    elif intent == "ops":
        checks["meets_criteria"] = "success" in output.lower() or "done" in output.lower()
    else:
        checks["meets_criteria"] = checks["has_output"]
    
    verdict = "PASS" if checks["completed"] and checks["meets_criteria"] else "NEEDS_REVIEW"
    risk_level = "low" if checks["meets_criteria"] else "medium"
    
    reflection = {
        "query": query,
        "intent": intent,
        "subagent_status": status,
        "checks": checks,
        "verdict": verdict,
        "risk_level": risk_level,
        "recommendation": "Deliver to user" if verdict == "PASS" else "Review output before delivery",
    }
    
    print(f"  Verdict: {reflection['verdict']}")
    print(f"  Risk level: {reflection['risk_level']}")
    print(f"  Recommendation: {reflection['recommendation']}")
    if "url_count" in checks:
        print(f"  URLs found: {checks['url_count']}")
    
    return reflection


def human_in_the_loop(reflection: dict, subagent_result: dict) -> dict:
    """Human-in-the-loop for high-risk outputs."""
    
    if reflection["risk_level"] == "high":
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
    parser = argparse.ArgumentParser(description="Trismegistus Supervisor Agent — Phase 3")
    parser.add_argument("query", help="User query to process")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("TRISMEGISTUS SUPERVISOR AGENT — PHASE 3 (LIVE DELEGATION)")
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
    
    if args.dry_run:
        subagent_result = {
            "status": "dry_run",
            "intent": execution_plan["intent"],
            "message": "Would spawn subagent with above configuration",
        }
    else:
        # Step 2: Live Subagent Delegation
        subagent_result = run_hermes_subagent(
            args.query,
            execution_plan,
            timeout=execution_plan["timeout"],
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
    
    # Save result
    os.makedirs("results", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    result_path = f"results/phase3_{execution_plan['intent']}_{timestamp}.json"
    with open(result_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResult saved to: {result_path}")
    
    return output


if __name__ == "__main__":
    main()
