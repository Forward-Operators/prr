# response coming from service
class ServiceResponse:
    def __init__(self, response_content, data={}):
        self.data = data
        self.response_content = response_content

    def is_response_content_text(self):
        return isinstance(self.response_content, str)

    def response_text(self, length_limit=None):
        if self.is_response_content_text():
            _str = str(self.response_content)

            if length_limit != None and len(_str) > length_limit:
                _str = _str[0:length_limit] + "..."

            return _str.replace("\n", " ").replace("  ", " ")

        return f"[{len(self.response_content)} bytes of data]"

    def __repr__(self):
        return " ".join([f"{key}={value}" for key, value in self.data.items()])

    def to_dict(self):
        return {key: value for key, value in self.data.items() if key != "completion"}

    # how many tokens we have to pay for
    def tokens_used(self):
        if self.data:
            if self.data.get("tokens_used"):
                return int(self.data.get("tokens_used"))

        return None

    # how many tokens have we generated
    def tokens_generated(self):
        if self.data:
            if self.data.get("completion_tokens"):
                return int(self.data.get("completion_tokens"))

        return None
