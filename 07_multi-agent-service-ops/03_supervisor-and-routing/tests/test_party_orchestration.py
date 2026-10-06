import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_DIR))
spec = importlib.util.spec_from_file_location("party", LAB_DIR / "08_my_orchestration.py")
party = importlib.util.module_from_spec(spec)
spec.loader.exec_module(party)


def state(last, completed, matcher_runs=1):
    return {"last_agent": last, "outputs": {last: {"completed": completed}}, "matcher_runs": matcher_runs}


def response(result):
    return {"provider_requested": "fake", "model": "fake", "result": result, "error": None}


class AllowedNextTest(unittest.TestCase):
    def test_transition_table(self):
        cases = [
            (party.new_state(), ["profile_agent"]),
            (state("profile_agent", True, 0), ["matcher_agent"]),
            (state("profile_agent", False, 0), ["ask_user"]),
            (state("matcher_agent", True), ["safety_agent"]),
            (state("matcher_agent", False, 1), ["matcher_agent", "finish"]),
            (state("matcher_agent", False, 2), ["finish"]),
            (state("safety_agent", True), ["finish"]),
            (state("safety_agent", False, 1), ["matcher_agent", "finish"]),
            (state("safety_agent", False, 2), ["finish"]),
        ]
        for current, expected in cases:
            with self.subTest(last=current["last_agent"], runs=current["matcher_runs"]):
                self.assertEqual(party.allowed_next(current), expected)

    def test_final_status(self):
        self.assertEqual(party.final_status(state("profile_agent", False, 0), "ask_user")[0], "needs_input")
        self.assertEqual(party.final_status(state("safety_agent", True), "finish")[0], "completed")
        self.assertEqual(party.final_status(state("matcher_agent", False, 2), "finish")[0], "no_match")
        self.assertEqual(party.final_status(state("safety_agent", False, 2), "finish")[0], "rejected")


class WorkerPromptTest(unittest.TestCase):
    def call_worker(self, agent_id, returned_id):
        captured = {}

        def fake_run(provider, prompt, schema):
            captured["prompt"] = prompt
            return response({"agent_id": returned_id, "summary": "s", "details": [], "completed": True})

        with patch.object(party, "run_with_metadata", fake_run):
            result = party.selected_worker_agent(agent_id, "요청", {})
        return result, captured["prompt"]

    def test_agent_id_is_stamped_by_orchestrator(self):
        result, _ = self.call_worker("safety_agent", "profile_agent")
        self.assertIsNone(result["error"])
        self.assertEqual(result["result"]["agent_id"], "safety_agent")

    def test_only_matcher_receives_participant_pool(self):
        _, matcher_prompt = self.call_worker("matcher_agent", "matcher_agent")
        _, profile_prompt = self.call_worker("profile_agent", "profile_agent")
        self.assertIn("U01", matcher_prompt)
        self.assertNotIn("U01", profile_prompt)


class PartyLoopTest(unittest.TestCase):
    def run_team(self, picks, worker_completed, max_llm_calls=12):
        picks, worker_completed = iter(picks), iter(worker_completed)
        supervisor = lambda *_: response({"next_agent": next(picks)})
        worker = lambda agent_id, *_: response({"agent_id": agent_id, "completed": next(worker_completed)})
        with patch.object(party, "supervisor_agent", supervisor), patch.object(party, "selected_worker_agent", worker):
            return party.party_team_agent("요청", max_llm_calls)

    def test_happy_path(self):
        result = self.run_team(["profile_agent", "matcher_agent", "safety_agent", "finish"], [True, True, True])
        self.assertEqual((result["status"], result["reason"]), ("completed", "safety_passed"))

    def test_missing_information_asks_user(self):
        result = self.run_team(["profile_agent", "ask_user"], [False])
        self.assertEqual(result["status"], "needs_input")

    def test_safety_failure_retries_matcher_once_then_rejected(self):
        picks = ["profile_agent", "matcher_agent", "safety_agent", "matcher_agent", "safety_agent", "finish"]
        result = self.run_team(picks, [True, True, False, True, False])
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["state"]["matcher_runs"], 2)

    def test_disallowed_choice_is_blocked(self):
        result = self.run_team(["safety_agent"], [])
        self.assertEqual((result["status"], result["reason"]), ("blocked", "invalid_transition"))

    def test_max_llm_calls(self):
        result = self.run_team(["profile_agent", "matcher_agent"], [True, True], max_llm_calls=4)
        self.assertEqual(result["reason"], "max_llm_calls")


if __name__ == "__main__":
    unittest.main()
