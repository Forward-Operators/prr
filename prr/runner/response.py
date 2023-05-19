# response coming from service
class ServiceResponse:
    def __init__(self, response_content, data={}):
        self.data = data
        self.response_content = response_content

    def response_abbrev(self, max_len=25):
        str = self.response_content

        if len(self.response_content) > max_len:
            str = self.response_content[0:max_len] + "..."

        return str.replace("\n", " ").replace("  ", " ")

    def __repr__(self):
        return " ".join([f"{key}={value}" for key, value in self.data.items()])

    def to_dict(self):
        return {key: value for key, value in self.data.items() if key != "completion"}

    def tokens_used(self):
        if self.data:
            if self.data.get("tokens_used"):
                return self.data.get("tokens_used")

        return None
