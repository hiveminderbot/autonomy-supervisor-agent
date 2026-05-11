#!/usr/bin/env python3
"""
Router Evaluation Script — measures intent classification accuracy, latency, cost.
Writes results to router_eval_results.json for acceptance evidence.
"""

import json
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from router import classify_intent

# Test cases: (query, expected_intent)
TEST_CASES = [
    # Standard cases
    ("Find recent papers on LLM agents", "research"),
    ("Fix the bug in deduplicator.py", "code"),
    ("Deploy the new API to production", "ops"),
    ("Generate an image of a cyberpunk city", "creative"),
    ("Analyze sales data for Q1 trends", "analysis"),
    ("What should I have for dinner?", "chat"),
    ("Set up a cron job to backup the database", "ops"),
    ("Refactor the authentication middleware to use JWT", "code"),
    ("Create a bar chart of monthly revenue", "analysis"),
    ("Write a Python script to scrape Hacker News", "code"),
    ("Monitor disk usage and alert if above 90%", "ops"),
    ("Summarize the latest Transformer architecture paper", "research"),
    ("Find the cheapest flights from NYC to Tokyo next month", "research"),
    ("Build a landing page for my SaaS product", "code"),
    ("Generate a podcast intro jingle", "creative"),
    # Edge cases
    ("", "chat"),
    ("hi", "chat"),
    ("help", "chat"),
    ("Run the tests and fix any failures", "code"),
    ("Check if the server is up", "ops"),
    ("Compare Python vs Rust performance", "analysis"),
    ("Find documentation for the Kubernetes API", "research"),
]


def evaluate():
    results = []
    correct = 0
    total_latency = 0.0
    total_tokens = 0

    for query, expected in TEST_CASES:
        start = time.time()
        try:
            result = classify_intent(query)
            latency = time.time() - start
            predicted = result["classification"]["intent"]
            confidence = result["classification"]["confidence"]
            tokens = result["cost"]["total_tokens"]

            is_correct = predicted == expected
            if is_correct:
                correct += 1
            total_latency += latency
            total_tokens += tokens

            results.append({
                "query": query,
                "expected": expected,
                "predicted": predicted,
                "correct": is_correct,
                "confidence": confidence,
                "latency_ms": round(latency * 1000, 1),
                "tokens": tokens,
            })
        except Exception as e:
            results.append({
                "query": query,
                "expected": expected,
                "predicted": None,
                "correct": False,
                "error": str(e),
            })

    accuracy = correct / len(TEST_CASES) if TEST_CASES else 0
    avg_latency = total_latency / len(TEST_CASES) if TEST_CASES else 0
    avg_tokens = total_tokens / len(TEST_CASES) if TEST_CASES else 0

    summary = {
        "total_cases": len(TEST_CASES),
        "correct": correct,
        "accuracy": round(accuracy, 3),
        "avg_latency_ms": round(avg_latency * 1000, 1),
        "avg_tokens": round(avg_tokens, 1),
        "estimated_cost_usd": round(total_tokens * 0.25 / 1_000_000, 6),  # Haiku ~$0.25/M tokens
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    output = {
        "summary": summary,
        "results": results,
    }

    with open("router_eval_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"\nDetailed results written to router_eval_results.json")
    return output


if __name__ == "__main__":
    evaluate()
