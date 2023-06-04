import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from helpers import create_temp_file, remove_temp_file

from prr.prompt.prompt_loader import PromptConfigLoader


class TestPromptConfigLoader:
    def test_basic_loading(self):
        prompt_template_file_path = create_temp_file(
            "Write a poem about AI from the projects, barely surviving on token allowance."
        )

        loader = PromptConfigLoader()
        prompt = loader.load_from_path(prompt_template_file_path)

        assert prompt

        remove_temp_file(prompt_template_file_path)
