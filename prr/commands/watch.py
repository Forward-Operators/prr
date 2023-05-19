#!/usr/bin/env python

import datetime
import os
import time

from prr.commands.run import RunPromptCommand
from prr.prompt import Prompt
from prr.prompt.prompt_loader import PromptConfigLoader


def timestamp_for_file(path):
    if os.path.exists(path):
        return os.path.getmtime(path)

    return 0


class WatchPromptCommand:
    def __init__(self, args, prompt_args=None):
        self.args = args
        self.prompt_args = prompt_args
        self.setup_files_to_monitor()

    def reload_files(self):
        self.setup_files_to_monitor()

    def current_timestamps(self):
        return [timestamp_for_file(path) for path in self.files]

    def update_timestamps(self, ready_timestamps=None):
        if ready_timestamps != None:
            self.file_timestamps = ready_timestamps
        else:
            self.file_timestamps = self.current_timestamps()

    def setup_files_to_monitor(self):
        loader = PromptConfigLoader()
        prompt_config = loader.load_from_path(self.args["prompt_path"])

        self.files = loader.file_dependencies
        self.update_timestamps()

    def files_changed(self):
        new_timestamps = self.current_timestamps()

        if new_timestamps != self.file_timestamps:
            self.update_timestamps(new_timestamps)
            self.reload_files()
            return True

        return False

    def status_message(self):
        prompt_path = self.args["prompt_path"]
        cooldown = self.args["cooldown"]

        message = f"👀 watching {self.files}."

        message += f"\nPress Ctrl+C to exit."

        return message

    def cooldown_if_needed(self):
        cooldown = self.args["cooldown"]

        print(f"🕶️ {cooldown}s cooldown started.\n")

        if cooldown != None:
            if int(cooldown) > 0:
                time.sleep(int(cooldown))
                print(self.status_message())

    def watch_prompt(self):
        print(self.status_message())

        while True:
            if self.files_changed():
                self.run()
                self.cooldown_if_needed()

            # standard tick
            time.sleep(0.25)

    def run(self):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print("\n")
        print("------------- new run at " + timestamp + " -------------")
        command = RunPromptCommand(self.args)
        command.run_prompt()
