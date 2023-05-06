import openai

from lib.response import ModelResponse

# OpenAI model provider class
class ServiceOpenAIChat:
  provider = 'openai'
  service = 'chat'
  
  def run(self, prompt, service_config):
    self.prompt = prompt
    self.service_config = service_config
    options = self.service_config.options

    messages = self.messages_from_prompt()

    completion = openai.ChatCompletion.create(
      model = self.service_config.model_name(),
      messages = messages,
      temperature = options.temperature,
      max_tokens = options.max_tokens
    )

    usage = completion.usage

    return ModelResponse({
      'completion': completion.choices[0].message.content,
      'tokens_used': usage.total_tokens,
      'completion_tokens': usage.completion_tokens,
      'prompt_tokens': usage.prompt_tokens,
      'total_tokens': usage.total_tokens
    })

  def messages_from_prompt(self):
    messages = self.prompt.messages

    # prefer messages from prompt if they exist
    if messages:
      return messages
    
    return [
      {
        "role": "user", 
        "content": self.prompt.text()
      }
    ]
