import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig


class TestModelOptions:
    def test_basic_options(self):
        options = ModelOptions({"foo": 42})

        assert options != None

        for option_key in ModelOptions.DEFAULT_OPTIONS.keys():
            assert options.value(option_key) == ModelOptions.DEFAULT_OPTIONS[option_key]

        assert options.value("foo") == 42

    def test_default_override(self):
        options = ModelOptions({"max_tokens": 31337})

        assert options != None

        for option_key in ModelOptions.DEFAULT_OPTIONS.keys():
            if option_key == "max_tokens":
                assert options.value(option_key) == 31337
            else:
                assert (
                    options.value(option_key)
                    == ModelOptions.DEFAULT_OPTIONS[option_key]
                )
