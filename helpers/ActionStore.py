from . import RegexHelper as re
from . import Actions as A
from . import PropertyActions as PA
from . import ClassActions as CA


def __init__():
	pass


class ActionStore():
	def __init__(self, message, action):
		super(ActionStore, self).__init__()
		self.message = message
		self.action = action


actions = {
	A.ADD_GETTER: PA.AddGetterAction(),
	A.ADD_SETTER: PA.AddSetterAction(),
	A.ADD_GETTER_SETTER: PA.AddGetterSetterAction(),

	A.ADD_CONSTRUCTOR: CA.AddConstructorAction(),
	A.ADD_INITIALIZER: CA.AddInitializerAction(),
}
prop_actions = [
	ActionStore('Add getter and setter', actions[A.ADD_GETTER_SETTER]),
	ActionStore('Add getter', actions[A.ADD_GETTER]),
	ActionStore('Add setter', actions[A.ADD_SETTER]),
	# ActionStore('Add constructor parameter', A.AddGetterAction())
]
class_actions = [
	ActionStore('Add constructor', actions[A.ADD_CONSTRUCTOR]),
	ActionStore('Add initializer', actions[A.ADD_INITIALIZER]),
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
