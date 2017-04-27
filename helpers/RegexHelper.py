import re

CLASS_DEF = r'((public|private|global|protected)\s*(virtual|abstract|with sharing|without sharing){0,1}\s+class\s+(\w+)\s*.*{)'
PROP_DEF = r'(public|private|global|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;'
SECURE_PROP_DEF = r'(private|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;'
CLASS_NAME = r'(class\s+(\w+)\s+.*{)'
PROP_NAME = r'((public|private|global|protected)\s*(static){0,1}\s+(\w+)\s+(\w+)\s*;)'
CONSTRUCTOR = r'((public|private|global|protected)\s+(\w+)\s*\((.|\n)*?\)\s*{)'
INDENT = r'^(\s*)\w'


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
		return []


def findClassName(code):
	result = find(CLASS_NAME, code)
	if result:
		return result[1]


def findPropName(code):
	result = find(PROP_NAME, code)
	if result:
		return result[4]


def findPropType(code):
	result = find(PROP_NAME, code)
	if result:
		return result[3]


def getIndent(code):
	result = find(INDENT, code)
	if result:
		return result[0]
	else:
		return ''
