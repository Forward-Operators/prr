# https://console.anthropic.com/docs/api/reference
# https://github.com/anthropics/anthropic-sdk-python/tree/main/examples

import os
import anthropic

from ..options import ModelOptions
from ..response import ModelResponse

# https://console.anthropic.com/docs/api/reference

# Anthropic model provider class
class LLMProviderAnthropic:
  def run(self, prompt, config):
    self.options = ModelOptions(config)
    prompt_text = prompt.text()

    client = anthropic.Client(os.environ['ANTHROPIC_API_KEY'])
    response = client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt_text}{anthropic.AI_PROMPT}",
        stop_sequences = [anthropic.HUMAN_PROMPT],
        model = config['model_name'],
        max_tokens_to_sample = self.options.max_tokens,
        temperature = self.options.temperature,
        top_p = self.options.top_p,
        top_k = self.options.top_k
    )

    # {
    #   'completion': ' [\n     { \n         name: "Four Noble Truths  🕉️",\n         description: "core teaching"\n     },\n     { \n         name: "Eightfold Path",\n         description: "core principles"\n     },\n     { \n         name: "Anicca",  \n         description: "impermanence"\n     },\n     { \n         name: "Anatta", \n         description: "non-self"\n     },\n     { \n         name: "Karma", \n         description: "law', 
    #   'stop': None, 
    #   'stop_reason': 'max_tokens', 
    #   'truncated': False, 
    #   'log_id': '9ac56ec912bfea79af8a09a43f7f220d', 
    #   'model': 'claude-v1', 
    #   'exception': None
    # }

    # print (response)

    return ModelResponse({
      'completion': response['completion'],
      'tokens_used': anthropic.count_tokens(response['completion']),
    })