import openai

from ..options import ModelOptions
from ..response import ModelResponse

# OpenAI model provider class
class LLMProviderOpenAI:
  def run(self, prompt, config):
    self.options = ModelOptions(config)
    prompt_text = prompt.text()

    completion = openai.ChatCompletion.create(
      model = config['model_name'],
      messages = [
        {
          "role": "user", 
          "content": prompt_text
        }
      ],
      temperature = self.options.temperature,
      max_tokens = self.options.max_tokens,
      # top_p = self.options.top_p,
      # top_k = self.options.top_k
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
