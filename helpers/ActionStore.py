from . import RegexHelper as re
from . import Actions as A
from . import PropertyActions as PA
from . import ClassActions as CA
from . import MethodActions as MA
from . import ConstructorActions as CtorA
from . import logger


def __init__():
	pass


log = logger.get(__name__)


class ActionStore():
	def __init__(self, message, action):
		super(ActionStore, self).__init__()
		self.message = message
		self.action = action


actions = {
	A.ADD_GETTER: PA.AddGetterAction(),
	A.ADD_SETTER: PA.AddSetterAction(),
	A.ADD_GETTER_SETTER: PA.AddGetterSetterAction(),
	A.ADD_CONSTRUCTOR_PARAMETER: PA.AddConstructorParameterAction(),
	A.ADD_GET_SET_PROPS: PA.AddGetSetProps(),

	A.ADD_CONSTRUCTOR: CA.AddConstructorAction(),
	A.ADD_INITIALIZER: CA.AddInitializerAction(),
	A.ADD_CONSTRUCTOR_INITIALIZER: CA.AddConstructorInitializerAction(),

	A.ADD_METHOD_OVERRIDE: MA.AddMethodOverrideChooseArgAction(),
	A.ADD_METHOD_OVERRIDE_CREATE: MA.AddMethodOverrideAction(),

	A.ADD_CONSTRUCTOR_OVERRIDE: CtorA.AddConstructorOverloadChooseArgAction(),
	A.ADD_CONSTRUCTOR_OVERRIDE_CREATE: CtorA.AddConstructorOverloadAction(),
}
prop_actions = [
	ActionStore('Add getter and setter', actions[A.ADD_GETTER_SETTER]),
	ActionStore('Add getter', actions[A.ADD_GETTER]),
	ActionStore('Add setter', actions[A.ADD_SETTER]),
	ActionStore('Add constructor parameter', actions[A.ADD_CONSTRUCTOR_PARAMETER]),
	ActionStore('Add {get; set;}', actions[A.ADD_GET_SET_PROPS])
]
class_actions = [
	ActionStore('Add constructor', actions[A.ADD_CONSTRUCTOR]),
	ActionStore('Add initializer', actions[A.ADD_INITIALIZER]),
	ActionStore('Add constructor and initializer', actions[A.ADD_CONSTRUCTOR_INITIALIZER]),
]
method_actions = [
	ActionStore('Generate overload', actions[A.ADD_METHOD_OVERRIDE]),
]
constructor_actions = [
	ActionStore('Generate overload', actions[A.ADD_CONSTRUCTOR_OVERRIDE]),
]
actions_map = {
	'prop': prop_actions,
	'class': class_actions,
	'method': method_actions,
	'constructor': constructor_actions,
}
regex_map = {
	'prop': re.PROP_DEF,
	'class': re.CLASS_DEF,
	'method': re.METHOD_DEF_ARGS,
	'constructor': re.CONSTRUCTOR_WITH_ARGS,
}


def getActions(view, line_reg):
	result = []
	log.info('re.METHOD_DEF_ARGS >> ', re.METHOD_DEF_ARGS)
	line = view.substr(line_reg)
	for key, regex in regex_map.items():
		if(re.match_stripped(regex, line)):
			result = actions_map[key]
	for store in result:
		store.action.setView(view)
		store.action.setCode(line_reg)
	return result
