#!/bin/bash

for example_prompt in ./examples/simple/poem ./examples/simple/sky ./examples/configured/dingo_from_file.yaml ./examples/configured/chihuahua.yaml ./examples/configured/dingo.yaml ./examples/code/html_boilerplate.yaml ./examples/templating/tell-me-all-about ./examples/shebang/get_famous_poet ./examples/shebang/dingo_with_shebang.yaml
do
	echo "-----------------------------"
	echo RUNNING $example_prompt
	echo "-----------------------------"

	python -m prr run --abbrev --max_tokens 1234 --temperature 0.98 $example_prompt
done
