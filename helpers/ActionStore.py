from . import RegexHelper as re
from . import Actions as A


def __init__():
	pass


class ActionStore():
	def __init__(self, message, action):
		super(ActionStore, self).__init__()
		self.message = message
		self.action = action


prop_actions = [
	ActionStore('Add getter and setter', A.AddGetterAction()),
	ActionStore('Add getter', A.AddGetterAction()),
	ActionStore('Add setter', A.AddSetterAction()),
	ActionStore('Add constructor parameter', A.AddGetterAction())
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
