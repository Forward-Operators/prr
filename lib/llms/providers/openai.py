import openai

from ..options import ModelOptions
from ..response import ModelResponse

# OpenAI model provider class
class LLMProviderOpenAI:
  def messages_from_prompt(self):
    messages = self.prompt.messages
    text = self.prompt.text()

    if messages:
      return messages
    
    return [
      {
        "role": "user", 
        "content": text
      }
    ]


  def run(self, prompt, config):
    self.prompt = prompt
    self.options = ModelOptions(config)

    messages = self.messages_from_prompt()

    completion = openai.ChatCompletion.create(
      model = config['model_name'],
      messages = messages,
      temperature = self.options.temperature,
      max_tokens = self.options.max_tokens
    )

    # "usage": {
    #   "completion_tokens": 246,
    #   "prompt_tokens": 15,
    #   "total_tokens": 261
    # }

    return ModelResponse({
      'completion': completion.choices[0].message.content,
      'tokens_used': completion.usage.total_tokens
    })
