from prr.prompt import Prompt
from helpers import create_temp_file, remote_temp_file

class TestPrompt:
    value = 0

    def test_one(self):
        path = create_temp_file('f00b4r', 'yaml')
	remove_temp_file(path)
        print(path)
        assert self.value == 2
