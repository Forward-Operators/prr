import time


class PromptRunResult:
    def __init__(self, prompt, config):
        self.prompt = prompt
        self.config = config
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
        self.request = None
        self.response = None
        self.tokens_per_second = None
        self.tokens_generated = None

    def before_run(self):
        self.start_time = time.time()

    def after_run(self):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def update_with_response(self, response):
        self.response = response
        self.tokens_generated = self.response.tokens_generated()

        if self.tokens_generated != None:
            self.tokens_per_second = self.tokens_generated / self.elapsed_time

    def update_with_request(self, request):
        self.request = request

    def metrics(self):
        return {
            "stats": {
                "start_time": self.start_time,
                "end_time": self.end_time,
                "elapsed_time": self.elapsed_time,
                "tokens_per_second": self.tokens_per_second,
                "tokens_generated": self.tokens_generated,
            },
            "request": self.request.to_dict(),
            "response": self.response.to_dict(),
        }

    def __str__(self):
        return f"PromptRunResult(prompt={self.prompt}, config={self.config}, start_time={self.start_time}, end_time={self.end_time}, elapsed_time={self.elapsed_time}, request={self.request}, response={self.response}, tokens_per_second={self.tokens_per_second}, tokens_generated={self.tokens_generated})"
