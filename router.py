#!/usr/bin/env python3
"""
Trismegistus Intent Router — Phase 1 Prototype
Classifies user queries into intent categories and selects appropriate
skill sets, models, and success criteria.

Uses OpenRouter + Claude 3.5 Haiku for cheap, fast classification.
"""

import json
import os
import re
import sys
import urllib.request

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-3.5-haiku"

INTENT_CATEGORIES = {
    "research": {
        "description": "Web search, information gathering, literature review, source discovery",
        "skills": ["web", "search", "arxiv", "blogwatcher"],
        "tools": ["web_search", "web_extract", "arxiv"],
        "model": "kimi-coding",
        "timeout": 120,
        "success_criteria": "Found at least 3 relevant sources with URLs and summaries",
    },
    "code": {
        "description": "Software development, debugging, file editing, system operations",
        "skills": ["terminal", "file", "code_exec", "patch"],
        "tools": ["terminal", "patch", "execute_code", "read_file", "write_file"],
        "model": "claude-sonnet-4",
        "timeout": 300,
        "success_criteria": "Code compiles/tests pass or file changes are applied correctly",
    },
    "ops": {
        "description": "DevOps, cron jobs, system monitoring, deployment, infrastructure",
        "skills": ["terminal", "cronjob", "file", "process"],
        "tools": ["terminal", "cronjob", "process", "execute_code"],
        "model": "claude-sonnet-4",
        "timeout": 180,
        "success_criteria": "Command executed successfully, service restarted, or config applied",
    },
    "creative": {
        "description": "Image generation, audio, video, design, content creation",
        "skills": ["image_gen", "tts", "vision"],
        "tools": ["image_generate", "text_to_speech", "vision_analyze"],
        "model": "claude-sonnet-4",
        "timeout": 180,
        "success_criteria": "Media file generated and saved to specified path",
    },
    "analysis": {
        "description": "Data processing, visualization, benchmarking, evaluation",
        "skills": ["code_exec", "terminal", "file"],
        "tools": ["execute_code", "terminal", "read_file", "write_file"],
        "model": "claude-sonnet-4",
        "timeout": 300,
        "success_criteria": "Analysis complete with quantitative results and visualizations",
    },
    "chat": {
        "description": "General conversation, advice, planning, brainstorming",
        "skills": [],
        "tools": [],
        "model": "kimi-coding",
        "timeout": 60,
        "success_criteria": "Response is helpful, accurate, and appropriately scoped",
    },
}

ROUTER_PROMPT = """You are an intent classifier for an AI agent system. 

Given a user query, classify it into EXACTLY ONE of these categories:
- research: Web search, information gathering, literature review, source discovery
- code: Software development, debugging, file editing, system operations  
- ops: DevOps, cron jobs, system monitoring, deployment, infrastructure
- creative: Image generation, audio, video, design, content creation
- analysis: Data processing, visualization, benchmarking, evaluation
- chat: General conversation, advice, planning, brainstorming

Respond with ONLY a JSON object in this exact format:
{
  "intent": "<category>",
  "confidence": 0.0-1.0,
  "reasoning": "One sentence explaining why this category fits best",
  "subtasks": ["brief description of likely subtasks"]
}

Query: """

# ---------------------------------------------------------------------------
# OpenRouter Key Discovery
# ---------------------------------------------------------------------------

def get_openrouter_key() -> str:
    """Find OpenRouter API key from env or auth.json."""
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key and "..." not in key:
        return key
    
    auth_path = os.path.expanduser("~/.hermes/auth.json")
    if os.path.exists(auth_path):
        try:
            with open(auth_path) as f:
                data = json.load(f)
            pool = data.get("credential_pool", {})
            entries = pool.get("openrouter", [])
            for entry in entries:
                token = entry.get("access_token", "")
                if token and "..." not in token:
                    return token
        except Exception:
            pass
    
    return ""

# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_intent(query: str) -> dict:
    """Classify user query into intent category."""
    key = get_openrouter_key()
    if not key:
        raise RuntimeError("No valid OpenRouter API key found")
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise intent classifier. Respond only with valid JSON."},
            {"role": "user", "content": ROUTER_PROMPT + query},
        ],
        "max_tokens": 200,
        "temperature": 0.0,
    }
    
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://trismegistus.local",
            "X-Title": "Trismegistus Intent Router",
        },
        method="POST",
    )
    
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    
    content = result["choices"][0]["message"]["content"]
    
    # Extract JSON from possible markdown fences or trailing text
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    # Sometimes the model adds trailing text after the JSON; find the last valid JSON object
    try:
        classification = json.loads(content)
    except json.JSONDecodeError:
        # Try to extract the last JSON object in the text
        brace_matches = list(re.finditer(r'\{', content))
        for start in reversed(brace_matches):
            for end in range(len(content), start.start(), -1):
                try:
                    candidate = content[start.start():end]
                    classification = json.loads(candidate)
                    break
                except json.JSONDecodeError:
                    continue
            else:
                continue
            break
        else:
            # Fallback: empty or unparseable input defaults to chat
            classification = {"intent": "chat", "confidence": 0.5, "reasoning": "Empty or unparseable input"}
    
    # Enrich with execution plan
    intent = classification.get("intent", "chat")
    plan = INTENT_CATEGORIES.get(intent, INTENT_CATEGORIES["chat"])
    
    return {
        "query": query,
        "classification": classification,
        "execution_plan": {
            "intent": intent,
            "skills": plan["skills"],
            "tools": plan["tools"],
            "model": plan["model"],
            "timeout": plan["timeout"],
            "success_criteria": plan["success_criteria"],
        },
        "cost": {
            "model_used": MODEL,
            "input_tokens": result["usage"]["prompt_tokens"],
            "output_tokens": result["usage"]["completion_tokens"],
            "total_tokens": result["usage"]["total_tokens"],
        },
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python router.py '<query>'")
        print("\nExamples:")
        print('  python router.py "Find recent papers on LLM agents"')
        print('  python router.py "Fix the bug in deduplicator.py"')
        print('  python router.py "Generate an image of a cyberpunk city"')
        sys.exit(1)
    
    query = sys.argv[1]
    result = classify_intent(query)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
