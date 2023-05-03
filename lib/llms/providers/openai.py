import openai

from ..options import ModelOptions

# OpenAI model provider class
class LLMProviderOpenAI:
  def run(self, prompt, model, options={}):
    self.options = ModelOptions(options)
    prompt_text = prompt.text(model)

    completion = openai.ChatCompletion.create(
      model = model, 
      messages = [
        {
          "role": "user", 
          "content": prompt_text
        }
      ],
      temperature = self.options.temperature,
      max_tokens = self.options.max_tokens,
    )

    # "usage": {
    #   "completion_tokens": 246,
    #   "prompt_tokens": 15,
    #   "total_tokens": 261
    # }


    return {
      'completion': completion.choices[0].message.content,
      'tokens_used': completion.usage.total_tokens
    }
  
    # return completion.choices[0].message.content