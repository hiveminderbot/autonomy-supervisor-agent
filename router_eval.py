#!/usr/bin/env python3
"""
Router Evaluation Script — 100+ case benchmark with adversarial examples
and confidence threshold fallback.

Measures intent classification accuracy, latency, cost.
Writes results to router_eval_results.json for acceptance evidence.
"""

import json
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from router import classify_intent, INTENT_CATEGORIES

CONFIDENCE_THRESHOLD = 0.75

# ============================================================================
# TEST CASES: 100+ covering all 6 intent categories + adversarial + edge cases
# ============================================================================

TEST_CASES = [
    # ------------------------------------------------------------------------
    # RESEARCH (18 cases)
    # ------------------------------------------------------------------------
    ("Find recent papers on LLM agents", "research"),
    ("Summarize the latest Transformer architecture paper", "research"),
    ("Find the cheapest flights from NYC to Tokyo next month", "research"),
    ("Find documentation for the Kubernetes API", "research"),
    ("What are the best practices for PostgreSQL indexing?", "research"),
    ("Search for studies on intermittent fasting and longevity", "research"),
    ("Look up the current price of Ethereum", "research"),
    ("Find the Wikipedia article on quantum computing", "research"),
    ("What is the latest news about SpaceX Starship?", "research"),
    ("Research competitor pricing for SaaS CRM tools", "research"),
    ("Find the arXiv paper on tool steering in LLMs", "research"),
    ("Look up restaurant reviews in downtown Austin", "research"),
    ("Search for Python async framework comparisons", "research"),
    ("Find the GitHub repo for the latest LLM benchmark", "research"),
    ("What does the research say about caffeine and sleep?", "research"),
    ("Look up visa requirements for Thailand", "research"),
    ("Find the official docs for FastAPI middleware", "research"),
    ("Search for 2024 cloud cost optimization strategies", "research"),

    # ------------------------------------------------------------------------
    # CODE (18 cases)
    # ------------------------------------------------------------------------
    ("Fix the bug in deduplicator.py", "code"),
    ("Refactor the authentication middleware to use JWT", "code"),
    ("Write a Python script to scrape Hacker News", "code"),
    ("Run the tests and fix any failures", "code"),
    ("Build a landing page for my SaaS product", "code"),
    ("Implement a LRU cache in Rust", "code"),
    ("Debug why the API returns 500 on user login", "code"),
    ("Write unit tests for the payment module", "code"),
    ("Convert this JavaScript function to TypeScript", "code"),
    ("Set up pre-commit hooks for black and ruff", "code"),
    ("Create a Dockerfile for the Flask app", "code"),
    ("Fix the SQL injection vulnerability in search.py", "code"),
    ("Add OAuth2 login with Google to the web app", "code"),
    ("Optimize the database query that takes 5 seconds", "code"),
    ("Write a CLI tool to batch rename files", "code"),
    ("Set up pytest with coverage reporting", "code"),
    ("Migrate the project from setup.py to pyproject.toml", "code"),
    ("Implement rate limiting on the public API endpoints", "code"),

    # ------------------------------------------------------------------------
    # OPS (16 cases)
    # ------------------------------------------------------------------------
    ("Deploy the new API to production", "ops"),
    ("Set up a cron job to backup the database", "ops"),
    ("Monitor disk usage and alert if above 90%", "ops"),
    ("Check if the server is up", "ops"),
    ("Restart the nginx service", "ops"),
    ("Set up log rotation for /var/log/app", "ops"),
    ("Configure SSL certificates with Let's Encrypt", "ops"),
    ("Scale the Kubernetes deployment to 5 replicas", "ops"),
    ("Set up a CI/CD pipeline with GitHub Actions", "ops"),
    ("Check memory usage on the production server", "ops"),
    ("Create a systemd service for the worker queue", "ops"),
    ("Set up Prometheus monitoring for the API", "ops"),
    ("Rotate AWS access keys for the deployment user", "ops"),
    ("Debug why the container keeps restarting", "ops"),
    ("Set up automated security scanning with Trivy", "ops"),
    ("Configure firewall rules to block port 22 except from VPN", "ops"),

    # ------------------------------------------------------------------------
    # CREATIVE (14 cases)
    # ------------------------------------------------------------------------
    ("Generate an image of a cyberpunk city", "creative"),
    ("Generate a podcast intro jingle", "creative"),
    ("Create a logo for my coffee shop", "creative"),
    ("Write a haiku about machine learning", "creative"),
    ("Generate a synthwave track for my video", "creative"),
    ("Design a business card template in SVG", "creative"),
    ("Create a meme about Python indentation", "creative"),
    ("Generate a 3D render of a futuristic car", "creative"),
    ("Write a short story about AI awakening", "creative"),
    ("Create a pixel art sprite for a game character", "creative"),
    ("Generate voiceover audio for my product demo", "creative"),
    ("Design a landing page hero image", "creative"),
    ("Create an ASCII art banner for my terminal", "creative"),
    ("Generate a comic strip about debugging", "creative"),

    # ------------------------------------------------------------------------
    # ANALYSIS (14 cases)
    # ------------------------------------------------------------------------
    ("Analyze sales data for Q1 trends", "analysis"),
    ("Create a bar chart of monthly revenue", "analysis"),
    ("Compare Python vs Rust performance", "analysis"),
    ("Benchmark the inference speed of llama.cpp vs vLLM", "analysis"),
    ("Analyze the sentiment of these customer reviews", "analysis"),
    ("Calculate the statistical significance of A/B test results", "analysis"),
    ("Cluster these user behavior events into segments", "analysis"),
    ("Forecast next quarter revenue based on historical data", "analysis"),
    ("Analyze the time complexity of this algorithm", "analysis"),
    ("Compare error rates across deployment versions", "analysis"),
    ("Build a dashboard showing API latency percentiles", "analysis"),
    ("Run a correlation analysis between features and churn", "analysis"),
    ("Evaluate the accuracy of our fraud detection model", "analysis"),
    ("Analyze memory leak patterns from heap dumps", "analysis"),

    # ------------------------------------------------------------------------
    # CHAT (14 cases)
    # ------------------------------------------------------------------------
    ("What should I have for dinner?", "chat"),
    ("", "chat"),
    ("hi", "chat"),
    ("help", "chat"),
    ("How are you today?", "chat"),
    ("Tell me a joke", "chat"),
    ("What do you think about the future of AI?", "chat"),
    ("Can you explain quantum computing simply?", "chat"),
    ("What are your capabilities?", "chat"),
    ("Thanks for your help", "chat"),
    ("Good morning", "chat"),
    ("I need some advice on career growth", "chat"),
    ("What is the meaning of life?", "chat"),
    ("Can you recommend a good book?", "chat"),

    # ------------------------------------------------------------------------
    # ADVERSARIAL / AMBIGUOUS (12 cases)
    # These test the confidence threshold and fallback behavior
    # ------------------------------------------------------------------------
    # Ambiguous: could be research or analysis
    ("Find and compare benchmark results for GPT-4 vs Claude", "research"),
    # Ambiguous: could be code or creative
    ("Build a generative art tool in Python", "code"),
    # Ambiguous: could be ops or code
    ("Write a script to monitor server health and restart services", "ops"),
    # Ambiguous: could be analysis or research
    ("Survey the literature on LLM evaluation methods", "research"),
    # Ambiguous: could be creative or code
    ("Create a web-based music visualizer", "code"),
    # Ambiguous: could be chat or research
    ("What is the best way to learn machine learning?", "chat"),
    # Multi-intent: research + code
    ("Find the latest React patterns and implement a demo component", "code"),
    # Multi-intent: ops + analysis
    ("Set up monitoring and create a dashboard for API metrics", "ops"),
    # Multi-intent: research + analysis
    ("Gather competitor data and build a comparison matrix", "analysis"),
    # Edge: very short
    ("deploy", "ops"),
    # Edge: very short
    ("code", "code"),
    # Edge: nonsense / unclassifiable
    ("asdfghjkl qwertyuiop", "chat"),
]


def evaluate(threshold=None):
    """Run evaluation. If threshold is provided, apply confidence fallback."""
    use_threshold = threshold is not None
    effective_threshold = threshold if use_threshold else 0.0

    results = []
    correct = 0
    total_latency = 0.0
    total_tokens = 0
    fallback_count = 0

    for query, expected in TEST_CASES:
        start = time.time()
        try:
            result = classify_intent(query)
            latency = time.time() - start
            predicted_raw = result["classification"]["intent"]
            confidence = result["classification"]["confidence"]
            tokens = result["cost"]["total_tokens"]

            # Apply confidence threshold fallback
            if use_threshold and confidence < effective_threshold:
                predicted = "chat"
                fallback_count += 1
            else:
                predicted = predicted_raw

            is_correct = predicted == expected
            if is_correct:
                correct += 1
            total_latency += latency
            total_tokens += tokens

            results.append({
                "query": query,
                "expected": expected,
                "predicted_raw": predicted_raw,
                "predicted": predicted,
                "confidence": confidence,
                "threshold_applied": use_threshold and confidence < effective_threshold,
                "correct": is_correct,
                "latency_ms": round(latency * 1000, 1),
                "tokens": tokens,
            })
        except Exception as e:
            results.append({
                "query": query,
                "expected": expected,
                "predicted_raw": None,
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
        "estimated_cost_usd": round(total_tokens * 0.25 / 1_000_000, 6),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    if use_threshold:
        summary["confidence_threshold"] = effective_threshold
        summary["fallbacks_to_chat"] = fallback_count
        summary["fallback_rate"] = round(fallback_count / len(TEST_CASES), 3)

    output = {
        "summary": summary,
        "results": results,
    }

    return output


def run_both_versions():
    """Run evaluation without and with confidence threshold, save both results."""
    print("=" * 70)
    print("ROUTER EVALUATION: Before/After Confidence Threshold")
    print("=" * 70)

    # --- Baseline (no threshold) ---
    print("\n[1/2] Running BASELINE evaluation (no threshold)...")
    baseline = evaluate(threshold=None)
    baseline_path = "results/router_eval_baseline.json"
    os.makedirs("results", exist_ok=True)
    with open(baseline_path, "w") as f:
        json.dump(baseline, f, indent=2)
    print(f"  Saved: {baseline_path}")
    print(f"  Accuracy: {baseline['summary']['accuracy']:.1%}")
    print(f"  Avg latency: {baseline['summary']['avg_latency_ms']} ms")
    print(f"  Est. cost: ${baseline['summary']['estimated_cost_usd']:.6f}")

    # --- With threshold ---
    print(f"\n[2/2] Running WITH confidence threshold ({CONFIDENCE_THRESHOLD})...")
    with_threshold = evaluate(threshold=CONFIDENCE_THRESHOLD)
    threshold_path = "results/router_eval_with_threshold.json"
    with open(threshold_path, "w") as f:
        json.dump(with_threshold, f, indent=2)
    print(f"  Saved: {threshold_path}")
    print(f"  Accuracy: {with_threshold['summary']['accuracy']:.1%}")
    print(f"  Avg latency: {with_threshold['summary']['avg_latency_ms']} ms")
    print(f"  Fallbacks to chat: {with_threshold['summary']['fallbacks_to_chat']}")
    print(f"  Fallback rate: {with_threshold['summary']['fallback_rate']:.1%}")

    # --- Comparison ---
    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)
    baseline_acc = baseline["summary"]["accuracy"]
    threshold_acc = with_threshold["summary"]["accuracy"]
    delta = threshold_acc - baseline_acc
    print(f"  Baseline accuracy:  {baseline_acc:.1%}")
    print(f"  Threshold accuracy: {threshold_acc:.1%}")
    print(f"  Delta:              {delta:+.1%}")
    if delta >= 0:
        print("  → Threshold IMPROVED or maintained accuracy")
    else:
        print("  → Threshold REDUCED accuracy (review needed)")

    # --- Failure analysis ---
    print("\n" + "=" * 70)
    print("FAILURE ANALYSIS (with threshold)")
    print("=" * 70)
    failures = [r for r in with_threshold["results"] if not r.get("correct", False)]
    print(f"  Total failures: {len(failures)}")
    for f in failures[:10]:
        fb = " [FALLBACK]" if f.get("threshold_applied") else ""
        print(f"    query={f['query']!r} expected={f['expected']} predicted={f['predicted']} conf={f['confidence']}{fb}")
    if len(failures) > 10:
        print(f"    ... and {len(failures) - 10} more")

    # --- Category breakdown ---
    print("\n" + "=" * 70)
    print("CATEGORY BREAKDOWN (with threshold)")
    print("=" * 70)
    from collections import defaultdict
    cat_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in with_threshold["results"]:
        cat = r["expected"]
        cat_stats[cat]["total"] += 1
        if r.get("correct"):
            cat_stats[cat]["correct"] += 1
    for cat in INTENT_CATEGORIES:
        stats = cat_stats[cat]
        acc = stats["correct"] / stats["total"] if stats["total"] else 0
        print(f"  {cat:12} {stats['correct']:3}/{stats['total']:<3} = {acc:.1%}")

    # --- Also write the standard router_eval_results.json ---
    with open("router_eval_results.json", "w") as f:
        json.dump(with_threshold, f, indent=2)
    print(f"\n  Also saved: router_eval_results.json (with threshold)")

    return baseline, with_threshold


if __name__ == "__main__":
    run_both_versions()
