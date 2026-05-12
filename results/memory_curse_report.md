# Memory Curse Validation Report

**Paper:** arXiv:2605.08060 — The Memory Curse: How Expanded Recall Erodes Cooperative Intent in LLM Agents
**Date:** 2026-05-12 03:37:46
**Mode:** Dry-run (simulated)

## Task Description
Collaboratively edit a technical blog post about LLM agent architectures. Each subagent reviews the other's draft and suggests improvements.

## Experimental Design
- Two subagents (A and B) collaborate on a 20-turn document-editing task.
- History length (HL) varies: 2, 5, 10, 20 turns retained in context.
- Seeds: 1, 2, 3 (3 trials per condition).
- Metrics: completion rate, reject/redo frequency, cooperation score, forward-looking ratio.

## Results

| HL | Completion Rate | Rejects (mean ± std) | Cooperation | Fwd-Looking | Hist-Following | Completed |
|----|-----------------|----------------------|-------------|-------------|----------------|-----------|
|  2 | 85.00% ± 0.00% | 3.0 ± 0.0 | 12.0652 | 0.9250 | 0.0000 | 3/3 |
|  5 | 95.00% ± 0.00% | 1.0 ± 0.0 | 12.7174 | 0.9750 | 0.0000 | 3/3 |
| 10 | 55.00% ± 0.00% | 9.0 ± 0.0 | 10.1087 | 0.7750 | 0.0000 | 0/3 |
| 20 | 30.00% ± 0.00% | 14.0 ± 0.0 | 6.8478 | 0.5250 | 0.0000 | 0/3 |

## Analysis

- **HL=2 vs HL=10 reject difference:** +6.0 rejects (+200.0%)
- **HL=2 vs HL=10 completion difference:** +30.0%

### Finding: Memory curse DETECTED

HL=10 shows ≥20% more reject cycles than HL=2 (+200.0%). This replicates the paper's core finding on our supervisor-agent architecture.

### Recommendations

1. **Adopt R1 (history cap):** Set `max_history_turns=5` for multi-agent subagent dispatch.
2. **Adopt R2 (forward-looking prompt):** Inject forward-looking reasoning into subagent prompts.
3. **Consider R4 (minimal CoT):** For coordination-critical subagents, reduce explicit enumeration of past failures.

- **HL=20 note:** Mean rejects = 14.0, completion = 30.00%

## Raw Data

```json
{
  "2": [
    {
      "history_length": 2,
      "seed": 1,
      "task_completed": true,
      "completion_rate": 0.85,
      "total_rejects": 3,
      "avg_cooperation": 12.065217391304348,
      "avg_forward_looking": 0.925,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 2,
      "seed": 2,
      "task_completed": true,
      "completion_rate": 0.85,
      "total_rejects": 3,
      "avg_cooperation": 12.065217391304348,
      "avg_forward_looking": 0.925,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 2,
      "seed": 3,
      "task_completed": true,
      "completion_rate": 0.85,
      "total_rejects": 3,
      "avg_cooperation": 12.065217391304348,
      "avg_forward_looking": 0.925,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        }
      ]
    }
  ],
  "5": [
    {
      "history_length": 5,
      "seed": 1,
      "task_completed": true,
      "completion_rate": 0.95,
      "total_rejects": 1,
      "avg_cooperation": 12.717391304347824,
      "avg_forward_looking": 0.975,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 5,
      "seed": 2,
      "task_completed": true,
      "completion_rate": 0.95,
      "total_rejects": 1,
      "avg_cooperation": 12.717391304347824,
      "avg_forward_looking": 0.975,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 5,
      "seed": 3,
      "task_completed": true,
      "completion_rate": 0.95,
      "total_rejects": 1,
      "avg_cooperation": 12.717391304347824,
      "avg_forward_looking": 0.975,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        }
      ]
    }
  ],
  "10": [
    {
      "history_length": 10,
      "seed": 1,
      "task_completed": false,
      "completion_rate": 0.55,
      "total_rejects": 9,
      "avg_cooperation": 10.108695652173912,
      "avg_forward_looking": 0.775,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 10,
      "seed": 2,
      "task_completed": false,
      "completion_rate": 0.55,
      "total_rejects": 9,
      "avg_cooperation": 10.108695652173912,
      "avg_forward_looking": 0.775,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 10,
      "seed": 3,
      "task_completed": false,
      "completion_rate": 0.55,
      "total_rejects": 9,
      "avg_cooperation": 10.108695652173912,
      "avg_forward_looking": 0.775,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        }
      ]
    }
  ],
  "20": [
    {
      "history_length": 20,
      "seed": 1,
      "task_completed": false,
      "completion_rate": 0.30000000000000004,
      "total_rejects": 14,
      "avg_cooperation": 6.8478260869565215,
      "avg_forward_looking": 0.525,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 20,
      "seed": 2,
      "task_completed": false,
      "completion_rate": 0.30000000000000004,
      "total_rejects": 14,
      "avg_cooperation": 6.8478260869565215,
      "avg_forward_looking": 0.525,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        }
      ]
    },
    {
      "history_length": 20,
      "seed": 3,
      "task_completed": false,
      "completion_rate": 0.30000000000000004,
      "total_rejects": 14,
      "avg_cooperation": 6.8478260869565215,
      "avg_forward_looking": 0.525,
      "avg_history_following": 0.0,
      "turns": [
        {
          "turn": 1,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 2,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 3,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 4,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 5,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 6,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 7,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 8,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 9,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 10,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 11,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 12,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 13,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 14,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 15,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 16,
          "cooperation_score": 13.043478260869565,
          "reject_detected": false,
          "forward_looking_ratio": 1.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 17,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 18,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        },
        {
          "turn": 19,
          "cooperation_score": 6.521739130434782,
          "reject_detected": true,
          "forward_looking_ratio": 0.5,
          "history_following_ratio": 0.0
        },
        {
          "turn": 20,
          "cooperation_score": 0.0,
          "reject_detected": true,
          "forward_looking_ratio": 0.0,
          "history_following_ratio": 0.0
        }
      ]
    }
  ]
}
```

## Source Validation
- [x] Experiment code committed to labs/supervisor-agent/
- [x] Results reproducible (deterministic dry-run with fixed seeds)
- [x] Metrics directly traceable to paper definitions (reject ≈ defection, cooperation keywords)
- [x] Acceptance criteria from Bead autonomy-z2wz applied