import os
import sys

THIS_FILE = os.path.abspath(__file__)
THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(THIS_FILE_DIR)
sys.path.append(os.path.join(THIS_FILE_DIR, "..", ".."))

from helpers import create_temp_file, remove_temp_file

from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner.run_collection import PromptRunCollection


class TestPromptConfigLoader:
    def test_basics(self):
        prompt_path = os.path.join(THIS_FILE_DIR, "..", "fixtures", "run_collection", "basic.yaml")

        assert os.path.exists(prompt_path)
        assert os.access(prompt_path, os.R_OK)

        loader = PromptConfigLoader()
        prompt_config = loader.load_from_path(prompt_path)

        assert prompt_config

        collection = PromptRunCollection(prompt_config)
        assert collection
        assert collection.is_empty() == False
        assert collection.has_done_runs() == True
        assert len(collection.runs) == 3

        run1 = collection.run('1')
        assert run1
        assert run1.state == 'done'
        assert run1.service_run_names() == ['gpt35']

        run2 = collection.run('2')
        assert run2
        assert run2.state == 'done'
        assert run2 == collection.the_one_before('3')
        assert run2.service_run_names() == ['gpt35', 'gpt4']

        run3 = collection.run('3')
        assert run3
        assert run3 == collection.latest_run()
        assert run3.state == 'in-progress'
