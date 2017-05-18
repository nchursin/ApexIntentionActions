from . import logger
from . import TemplateHelper as TH
from . import RegexHelper as re
from . import Actions as A
from . import ClassActions as CA
from .SublimeHelper import SublimeHelper as SH


log = logger.get(__name__)


class PropertyAction(A.Action):
	"""Stores info on property actions"""
	def __init__(self, name):
		super(PropertyAction, self).__init__(name)

	def get_class_code(self):
		return self.full_region(self.code_region)

	def get_prop_name(self):
		result = re.findPropName(self.to_text(self.code_region))
		log.debug('property name >> ' + result)
		return result

	def get_prop_type(self):
		result = re.findPropType(self.to_text(self.code_region))
		log.debug('property type >> ' + result)
		return result

	def is_prop_static(self):
		result = re.findPropIsStatic(self.to_text(self.code_region))
		log.debug('property static >> ', result)
		return result

	def generate_code(self):
		raise Exception("generate_code not defined")

	def is_applicable(self):
		return re.is_prop_def(self.to_text())


class AddGetterAction(PropertyAction):
	def __init__(self):
		super(AddGetterAction, self).__init__(A.ADD_GETTER)

	def generate_code(self, edit):
		template = TH.Template('other/getter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', self.is_prop_static())
		template.addVar('indent', self.get_inner_indent())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())

	def is_applicable(self):
		result = super(AddGetterAction, self).is_applicable()
		return result and re.findGetter(self.to_text(self.get_class_code()), self.get_prop_name()) is None


class AddSetterAction(PropertyAction):
	def __init__(self):
		super(AddSetterAction, self).__init__(A.ADD_SETTER)

	def generate_code(self, edit):
		template = TH.Template('other/setter')
		template.addVar('type', self.get_prop_type())
		template.addVar('varName', self.get_prop_name())
		template.addVar('static', self.is_prop_static())
		template.addVar('indent', self.get_inner_indent())
		self.view.insert(edit, self.find_end_of_class().begin(), template.compile())

	def is_applicable(self):
		result = super(AddSetterAction, self).is_applicable()
		return result and re.findSetter(self.to_text(self.get_class_code()), self.get_prop_name()) is None


class AddGetterSetterAction(PropertyAction):
	def __init__(self):
		super(AddGetterSetterAction, self).__init__(A.ADD_GETTER_SETTER)
		self.getter = AddGetterAction()
		self.setter = AddSetterAction()

	def setView(self, view):
		super(AddGetterSetterAction, self).setView(view)
		self.getter.setView(view)
		self.setter.setView(view)

	def setCode(self, code_region):
		super(AddGetterSetterAction, self).setCode(code_region)
		self.getter.setCode(code_region)
		self.setter.setCode(code_region)

	def is_applicable(self):
		return self.getter.is_applicable() and self.setter.is_applicable()

	def generate_code(self, edit):
		self.getter.generate_code(edit)
		self.setter.generate_code(edit)


class AddConstructorParameterAction(PropertyAction):
	def __init__(self):
		super(AddConstructorParameterAction, self).__init__(A.ADD_CONSTRUCTOR_PARAMETER)

	def generate_code(self, edit):
		constr_regions = self.find_constructors()

		if not constr_regions:
			constructorAction = CA.AddConstructorAction()
			constructorAction.setView(self.view)
			constructorAction.setCode(self.find_class_def())
			constructorAction.generate_code(edit)
			constr_regions = self.find_constructors()

		log.debug('constr_regions size >> ' + str(len(constr_regions)))
		for constr in constr_regions:
			start = constr.begin()
			def_line = self.view.line(start)
			def_str = self.view.substr(def_line)
			log.debug('def_str >> ' + def_str)
			args = re.find(r'\([\s|\n|\w]*?\)\s*\{{0,1}', def_str)
			log.debug('args >> ' + str(args))
			arg_def = self.get_prop_type() + ' ' + self.get_prop_name()
			if re.contains_regex(args, r'\(\s*\w+'):
				arg_def = ', ' + arg_def
			def_str = def_str.replace(')',
				arg_def + ')')
			self.view.replace(edit, def_line, def_str)
			def_line = self.view.line(start)
			indent = self.get_inner_indent() + '\t'
			insert_to = def_line.end() + 1
			text = '{indent}this.{varname} = {varname};\n'.format(indent=indent, varname=self.get_prop_name())
			self.view.insert(edit, insert_to, text)

	def is_applicable(self):
		result = re.is_prop_def(self.to_text(), allow_get_set=True, allow_static=False)
		result = result and re.findConstructorWithParam(
			self.to_text(self.get_class_code()),
			self.find_class_name(),
			self.get_prop_name(),
			self.get_prop_type()) is None
		return result


class AddGetSetProps(PropertyAction):
	def __init__(self):
		super(AddGetSetProps, self).__init__(A.ADD_GET_SET_PROPS)

	def generate_code(self, edit):
		to_insert = ' { ${1:public} get; ${2:public} set; }'
		# to_insert = ' { get; set; }'
		line_text = self.to_text()
		index_of_end = line_text.rfind(';')
		index_of_end = self.begin() + index_of_end
		sublimeHelper = SH(self.view)
		sublimeHelper.insert_snippet(to_insert, (index_of_end, index_of_end + 1))

	def is_applicable(self):
		result = super(AddGetSetProps, self).is_applicable()
		return result
