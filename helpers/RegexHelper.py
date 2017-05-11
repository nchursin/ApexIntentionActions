import re
from . import logger

PROP_DEF = r'(public|private|global|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;'
PROP_DEF_GET_SET = r'(public|private|global|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*\{\s*(get(;|(\{(.|\n)*?\}))\s*set(;|(\{(.|\n)*?\})))\}'
SECURE_PROP_DEF = r'(private|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;'
SECURE_PROP_DEF_GET_SET = r'(private|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*\{\s*(get(;|(\{(.|\n)*?\}))\s*set(;|(\{(.|\n)*?\})))\}'
PROP_NAME = r'((public|private|global|protected)\s*(static){0,1}\s+(\w+)\s+(\w+)\s*;)'

CLASS_DEF = r'((public|private|global|protected)\s*(virtual|abstract|with sharing|without sharing){0,1}\s+class\s+(\w+)\s*.*{)'
CLASS_NAME = r'(class\s+(\w+)\s+.*{)'

INDENT = r'^(\s*)\w'

NON_PRIVATE_METHOD_DEF_START = r'((public|global|protected)\s*(static){0,1}\s*(override|virtual|abstract){0,1}\s+(\w+)\s+'
METHOD_DEF_END = r'\s*\((.|\n)*?\)\s*\{)'
METHOD_DEF_END_ARGS = r'\s*\((.+?\s+.+?(.|\n)*?)\)\s*\{)'
METHOD_DEF_END_NO_ARG = r'\s*\((\s*)*?\)\s*\{)'
METHOD_DEF_START = r'((public|global|protected|private)\s*(static){0,1}\s*(override|virtual|abstract){0,1}\s+(\w+)\s+'
METHOD_DEF = METHOD_DEF_START + r'(\w+)' + METHOD_DEF_END
METHOD_DEF_ARGS = METHOD_DEF_START + r'(\w+)' + METHOD_DEF_END_ARGS

CONSTRUCTOR_DEF_START = r'((public|private|global|protected)\s+'
CONSTRUCTOR = CONSTRUCTOR_DEF_START + r'(\w+)' + METHOD_DEF_END

log = logger.get(__name__)


def match(regex, line):
	return re.match(regex, line)


def match_stripped(regex, line):
	return match(regex, line.strip())


def find_all(regex, text):
	return re.compile(regex).findall(text)


def find(regex, text):
	result = re.compile(regex).findall(text)
	if result:
		return re.compile(regex).findall(text)[0]
	else:
		return None


def findClassName(code):
	result = find(CLASS_NAME, code)
	if result:
		return result[1]


def findPropName(code):
	result = find(PROP_NAME, code)
	if result:
		return result[4]


def findMethodName(code):
	result = find(METHOD_DEF, code)
	if result:
		return result[5]


def findMethodAccessLevel(code):
	result = find(METHOD_DEF, code)
	if result:
		return result[1]


def findMethodIsStatic(code):
	result = find(METHOD_DEF, code)
	if result:
		return result[2].lower() == 'static'


def findMethodReturnType(code):
	result = find(METHOD_DEF, code)
	if result:
		return result[4]


def findMethodArgs(code):
	result = find(METHOD_DEF_ARGS, code)
	if result:
		return result[6]


def findPropIsStatic(code):
	result = find(PROP_NAME, code)
	if result:
		return result[2].lower() == 'static'


def findGetter(code, prop_name):
	regex = NON_PRIVATE_METHOD_DEF_START + 'get' + prop_name.lower() + METHOD_DEF_END_NO_ARG
	return find(regex, code.lower())


def findSetter(code, prop_name):
	regex = NON_PRIVATE_METHOD_DEF_START + 'set' + prop_name.lower() + METHOD_DEF_END
	return find(regex, code.lower())


def findConstructor(code, class_name):
	regex = CONSTRUCTOR_DEF_START + class_name.lower() + METHOD_DEF_END
	return find(regex, code.lower())


def findConstructorWithParam(code, class_name, param_name, param_type):
	regex = CONSTRUCTOR_DEF_START + class_name.lower() + r'\s*\((.|\n)*?' + param_type.lower() + r'\s+' + param_name.lower() + r'(.|\n)*?\)\s*\{)'
	return find(regex, code.lower())


def findMethod(code, method_name):
	regex = METHOD_DEF_START + method_name.lower() + METHOD_DEF_END
	return find(regex, code.lower())


def findPropType(code):
	result = find(PROP_NAME, code)
	if result:
		return result[3]


def is_method_def(line):
	regex = METHOD_DEF
	result = match_stripped(regex, line)
	return result


def is_prop_def(line, allow_get_set=False, allow_static=True):
	regex = PROP_DEF
	if not allow_static:
		regex = regex.replace(r'\s*(static){0,1}', '')
	result = match_stripped(regex, line)
	if allow_get_set:
		regex = PROP_DEF_GET_SET
		result = result or match_stripped(regex, line)
	return result


def contains_regex(text, regex):
	reg = re.compile(regex)
	if reg.search(text):
		return True
	else:
		return False


def getIndent(code, spaces_to_tabs, tab_size):
	result = find(INDENT, code)
	if result:
		if isinstance(result, list):
			result = result[0]
		if spaces_to_tabs:
			tabs_num = len(result) / tab_size
			result = ''
			for i in range(0, int(tabs_num)):
				result += '\t'
		return result
	else:
		return ''
