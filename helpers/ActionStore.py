import re


def __init__():
	pass


prop_actions = [
	'Add getter and setter',
	'Add getter',
	'Add setter',
	'Add constructor parameter',
]
class_actions = [
	'Add constructor',
	'Add initializer',
]
actions_map = {
	'prop': prop_actions,
	'class': class_actions,
}
regex_map = {
	'prop': r'(public|private|global|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;',
	'class': r'\w+\s*(virtual|abstract|with sharing|without sharing){0,1}\s+class\s+(\w+)\s*.*{',
}


def getActions(line):
	for key, regex in regex_map.items():
		if(re.match(regex, line.strip())):
			return actions_map[key]
