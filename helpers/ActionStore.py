from . import RegexHelper as re
from . import Actions as A


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
	'class': r'(public|private|global|protected)\s*(virtual|abstract|with sharing|without sharing){0,1}\s+class\s+(\w+)\s*.*{',
}


def getActions(line):
	for key, regex in regex_map.items():
		if(re.match_stripped(regex, line)):
			return actions_map[key]
