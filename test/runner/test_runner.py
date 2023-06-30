import os
import sys

THIS_FILE = os.path.abspath(__file__)
THIS_FILE_DIR = os.path.dirname(THIS_FILE)
GRANDPARENT_DIR = os.path.join(THIS_FILE_DIR, "..", "..")

sys.path.append(THIS_FILE_DIR)
sys.path.append(os.path.join(GRANDPARENT_DIR))

import shutil

from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner import Runner


class TestRunner:
    def setup_method(self, method):
        self.prompt_path = os.path.join(
            THIS_FILE_DIR, "..", "fixtures", "runner", "basic.yaml"
        )

        self.dot_runs_path = os.path.join(
            THIS_FILE_DIR, "..", "fixtures", "runner", "basic.runs"
        )

        self.loader = PromptConfigLoader()
        self.prompt_config = self.loader.load_from_path(self.prompt_path)

        try:
            shutil.rmtree(self.dot_runs_path)
        except:
            pass

    def test_basics(self):
        runner = Runner(self.prompt_config, True)

        services = self.prompt_config.configured_services()

        runner.run_services(services)

        run_collection = runner.run_collection
        run_collection.read_runs()
        assert run_collection.is_empty() == False
        assert run_collection.has_done_runs() == True
        assert len(run_collection.runs) == 1

        first_run = run_collection.runs[0]

        assert first_run
        assert first_run.state == "done"

        assert first_run.service_runs
        assert len(first_run.service_runs) == 2

        first_service_run = first_run.service_runs[0]

        assert first_service_run
        assert first_service_run.name() == "test1"

        assert (
            first_service_run.prompt_content()
            == """- content: You are sporting goods store assistant and you answer customer queries
    with fun responses,  making up stock items and prices as you go, suggesting  irrelevant
    things. Be kind.
  role: system
- content: How can I help you?
  name: Henry
  role: assistant
- content: I am looking for a pair of running shoes.
  name: Frige
  role: user
"""
        )

        assert (
            first_service_run.output_content()
            == """TEST COMPLETION. INPUT RECEIVED:
model: test_model-A1
messages: [{'role': 'system', 'content': 'You are sporting goods store assistant and you answer customer queries with fun responses,  making up stock items and prices as you go, suggesting  irrelevant things. Be kind.'}, {'role': 'assistant', 'content': 'How can I help you?', 'name': 'Henry'}, {'role': 'user', 'content': 'I am looking for a pair of running shoes.', 'name': 'Frige'}]
temperature: 1337
max_tokens: 128
"""
        )

        assert first_service_run.run_details()["request"] == {
            "model": "test_provider/test_service/test_model-A1",
            "options": {"max_tokens": 128, "temperature": 1337},
        }

        assert first_service_run.run_details()["response"] == {
            "completion_tokens": 666,
            "finish_reason": "stop",
            "prompt_tokens": 12345,
            "tokens_used": 666,
            "total_tokens": 31337,
        }

        assert first_service_run.run_details()["stats"]["elapsed_time"]
        assert first_service_run.run_details()["stats"]["start_time"]
        assert first_service_run.run_details()["stats"]["end_time"]
        assert first_service_run.run_details()["stats"]["tokens_generated"]
        assert first_service_run.run_details()["stats"]["tokens_per_second"]

        assert first_service_run.run_details_content()

    def test_basics_no_save(self):
        runner = Runner(self.prompt_config, False)

        services = self.prompt_config.configured_services()

        runner.run_services(services)

        run_collection = runner.run_collection
        run_collection.read_runs()
        assert run_collection.is_empty() == True
        assert run_collection.has_done_runs() == False
        assert len(run_collection.runs) == 0
