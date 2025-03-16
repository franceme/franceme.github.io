#!/usr/bin/env python3
import os
import sys
import pip
run = lambda x:os.system(x)

for x in [
	'Gruntfuggly.todo-tree',
	'ms-python.python',
	'actboy168.tasks',
	'MS-SarifVSCode.sarif-viewer',
	'dchanco.vsc-invoke',
	'donjayamanne.githistory',
	'alefragnani.Bookmarks',
	'littlefoxteam.vscode-python-test-adapter',
	'njpwerner.autodocstring',
	'sourcery.sourcery',
	'GitHub.copilot',
	'hbenl.vscode-test-explorer',
	'ritwickdey.LiveServer'
]:
	run(f"code-server --install-extension {x}")

requirements = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "", "requirements.txt")
if os.path.exists(requirements):
	pip.main(f"install -r {requirements}".split())