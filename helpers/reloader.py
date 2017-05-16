import sys
import imp
import os.path

from . import logger
log = logger.get(__name__)

# Dependecy reloader stolen from the Emmet plugin
pack_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
pack_name, ext = os.path.splitext(pack_name)
pack_name = os.path.basename(pack_name)

parent = pack_name + '.helpers'
print('parent >> ', parent)

reload_mods = []


def fill_reload_mods():
    reload_mods = []
    for mod in sys.modules:
        if mod.startswith(parent) and sys.modules[mod] is not None:
            reload_mods.append(mod)
    return reload_mods


fill_reload_mods()

mods_load_order = [
    'logger',

    'FileReader',
    'RegexHelper',
    'TemplateHelper',
    'Actions',
    'PropertyActions',
    'ClassActions',
    'MethodActions',
    'ConstructorActions',
    'ActionStore',

    'reloader',
]

mods_load_order = [parent + '.' + mod for mod in mods_load_order]


def reload():
    reload_mods = fill_reload_mods()
    log.debug('reloading')
    for mod in mods_load_order:
        log.debug('mod >> ' + mod)
        if mod in reload_mods:
            log.debug('reload mod >> ' + mod)
            imp.reload(sys.modules[mod])
