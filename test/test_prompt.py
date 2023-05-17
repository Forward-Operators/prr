import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prr.prompt import Prompt 

from helpers import create_temp_file, remove_temp_file


class TestPrompt:
    value = 0

    # def test_one(self):
    #     path = create_temp_file("f00b4r", "yaml")
    #     remove_temp_file(path)
    #     print(path)
    #     assert self.value == 0
