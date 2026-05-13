"""Test that router returns correct timeout values from INTENT_CATEGORIES."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router import INTENT_CATEGORIES, classify_intent
from unittest.mock import patch, MagicMock
import json

def test_code_intent_timeout_correct():
    """When router classifies 'code' intent, timeout should match INTENT_CATEGORIES exactly."""
    
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
    expected_timeout = INTENT_CATEGORIES["code"]["timeout"]
    
    assert plan["timeout"] == expected_timeout, \
        f"Expected timeout {expected_timeout}, got {plan['timeout']}"

def test_research_intent_timeout_correct():
    """When router classifies 'research' intent, timeout should match INTENT_CATEGORIES exactly."""
    
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
    expected_timeout = INTENT_CATEGORIES["research"]["timeout"]
    
    assert plan["timeout"] == expected_timeout, \
        f"Expected timeout {expected_timeout}, got {plan['timeout']}"

if __name__ == "__main__":
    test_code_intent_timeout_correct()
    test_research_intent_timeout_correct()
    print("All tests passed")
