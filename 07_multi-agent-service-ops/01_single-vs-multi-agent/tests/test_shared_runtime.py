from __future__ import annotations

import os
import sys
import unittest
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

import httpx
from openai.lib._pydantic import to_strict_json_schema


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared import travel_llm
from shared.travel_contracts import SupportAgentResult, LearningAgentResult


class SharedRuntimeTests(unittest.TestCase):
    def test_handoff_schema_is_strict_and_explicit(self) -> None:
        schema = to_strict_json_schema(SupportAgentResult)
        context_schema = schema["$defs"]["HandoffContext"]

        self.assertFalse(context_schema["additionalProperties"])
        self.assertEqual(
            set(context_schema["required"]),
            {"order_id", "amount", "approval_id"},
        )

    def test_handoff_decision_builds_expected_transfer(self) -> None:
        module_path = Path(__file__).resolve().parents[1] / "11_handoff_preview.py"
        spec = importlib.util.spec_from_file_location("handoff_preview", module_path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        decision = SupportAgentResult(
            handoff_required=True,
            target_agent="refund_agent",
            reason="approved refund",
            handoff_context={
                "order_id": "order-301",
                "amount": 35_000,
                "approval_id": "approval-901",
            },
        ).model_dump()
        handoff = module.create_handoff(decision)

        self.assertIsNotNone(handoff)
        self.assertEqual(handoff.to_agent, "refund_agent")
        self.assertEqual(handoff.context["amount"], 35_000)

    def test_transient_provider_error_is_retried(self) -> None:
        class TransientError(Exception):
            status_code = 503

        parsed = LearningAgentResult(agent_id="analyst_agent", summary="ok")
        call = Mock(side_effect=[TransientError("busy"), parsed])

        with (
            patch.dict(os.environ, {"MAX_AGENT_RETRIES": "1"}),
            patch.object(travel_llm, "run_structured", call),
            patch.object(travel_llm, "sleep"),
        ):
            result = travel_llm.run_with_metadata("gemini", "request", LearningAgentResult)

        self.assertEqual(call.call_count, 2)
        self.assertEqual(result["result"]["summary"], "ok")

    def test_agent_role_mismatch_is_retried(self) -> None:
        base = {
            "provider_requested": "gemma",
            "provider_used": "gemma",
            "model": "gemma3:1b",
            "fallback_used": False,
            "latency_ms": 1,
            "error": None,
        }
        wrong = {
            **base,
            "result": {
                "agent_id": "analyzer_agent",
                "summary": "wrong",
                "details": [],
                "completed": True,
            },
        }
        correct = {
            **base,
            "result": {
                "agent_id": "analyst_agent",
                "summary": "ok",
                "details": [],
                "completed": True,
            },
        }
        call = Mock(side_effect=[wrong, correct])

        with (
            patch.dict(os.environ, {"MAX_AGENT_RETRIES": "1"}),
            patch.object(travel_llm, "run_with_metadata", call),
        ):
            result = travel_llm.run_learning_agent("analyst_agent", "goal", "request")

        self.assertEqual(call.call_count, 2)
        self.assertEqual(result["result"]["agent_id"], "analyst_agent")

    def test_ollama_error_keeps_response_body(self) -> None:
        request = httpx.Request("POST", "http://127.0.0.1:11434/api/chat")
        response = httpx.Response(
            404,
            request=request,
            json={"error": "model not found"},
        )

        with patch.object(travel_llm.httpx, "post", return_value=response):
            with self.assertRaises(travel_llm.ProviderHTTPError) as caught:
                travel_llm.run_structured("gemma", "request", LearningAgentResult)

        self.assertEqual(caught.exception.status_code, 404)
        self.assertIn("model not found", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
