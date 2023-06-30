import os
import sys

THIS_FILE = os.path.abspath(__file__)
THIS_FILE_DIR = os.path.dirname(THIS_FILE)
GRANDPARENT_DIR = os.path.join(THIS_FILE_DIR, "..", "..")

sys.path.append(THIS_FILE_DIR)
sys.path.append(os.path.join(GRANDPARENT_DIR))

from prr.commands.run import RunPromptCommand
from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner import Runner
from prr.runner.run_collection import PromptRunCollection


class TestRunner:
    def test_basics(self):
        prompt_path = os.path.join(
            THIS_FILE_DIR, "..", "fixtures", "runner", "basic.yaml"
        )

        loader = PromptConfigLoader()
        prompt_config = loader.load_from_path(prompt_path)
        runner = Runner(prompt_config, True)

        services = prompt_config.configured_services()

        runner.run_services(services)

        run_collection = runner.run_collection
        run_collection.read_runs()
        assert run_collection.is_empty() == False
        assert run_collection.has_done_runs() == True
        assert len(run_collection.runs) == 1
