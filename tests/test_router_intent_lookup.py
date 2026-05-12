"""Test that router intent classification correctly maps to INTENT_CATEGORIES."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router import INTENT_CATEGORIES, classify_intent
from unittest.mock import patch, MagicMock
import json

def test_code_intent_maps_to_code_plan():
    """When router classifies 'code' intent, execution_plan should use code category config."""
    
    # Mock the API response to return 'code' intent
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "choices": [{"message": {"content": '{"intent": "code", "confidence": 0.95, "reasoning": "Fixing a bug"}'}}],
        "usage": {"prompt_tokens": 50, "completion_tokens": 30, "total_tokens": 80}
    }).encode()
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)
    
    with patch('urllib.request.urlopen', return_value=mock_response):
        with patch('router.get_openrouter_key', return_value='fake-key'):
            result = classify_intent("Fix the bug in deduplicator.py")
    
    plan = result["execution_plan"]
    
    # The bug: intent.upper() makes "CODE" which is not in INTENT_CATEGORIES,
    # so it falls back to "chat" instead of "code"
    assert plan["intent"] == "code", f"Expected intent 'code', got '{plan['intent']}'"
    assert plan["skills"] == INTENT_CATEGORIES["code"]["skills"], \
        f"Expected code skills {INTENT_CATEGORIES['code']['skills']}, got {plan['skills']}"
    assert plan["timeout"] == INTENT_CATEGORIES["code"]["timeout"], \
        f"Expected code timeout {INTENT_CATEGORIES['code']['timeout']}, got {plan['timeout']}"
    assert plan["model"] == INTENT_CATEGORIES["code"]["model"], \
        f"Expected code model {INTENT_CATEGORIES['code']['model']}, got {plan['model']}"

def test_research_intent_maps_to_research_plan():
    """When router classifies 'research' intent, execution_plan should use research category config."""
    
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "choices": [{"message": {"content": '{"intent": "research", "confidence": 0.9, "reasoning": "Finding papers"}'}}],
        "usage": {"prompt_tokens": 50, "completion_tokens": 30, "total_tokens": 80}
    }).encode()
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)
    
    with patch('urllib.request.urlopen', return_value=mock_response):
        with patch('router.get_openrouter_key', return_value='fake-key'):
            result = classify_intent("Find recent papers on LLM agents")
    
    plan = result["execution_plan"]
    
    assert plan["intent"] == "research", f"Expected intent 'research', got '{plan['intent']}'"
    assert plan["skills"] == INTENT_CATEGORIES["research"]["skills"], \
        f"Expected research skills {INTENT_CATEGORIES['research']['skills']}, got {plan['skills']}"
    assert plan["timeout"] == INTENT_CATEGORIES["research"]["timeout"], \
        f"Expected research timeout {INTENT_CATEGORIES['research']['timeout']}, got {plan['timeout']}"

if __name__ == "__main__":
    test_code_intent_maps_to_code_plan()
    test_research_intent_maps_to_research_plan()
    print("All tests passed")
