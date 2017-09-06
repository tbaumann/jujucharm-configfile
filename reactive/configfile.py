from charms.reactive import when, when_not, set_state, hook, when_any, remove_state
from charmhelpers.core.hookenv import log, status_set, config, service_name
from charmhelpers.core import hookenv
from charms.reactive.helpers import data_changed
from charmhelpers.core.unitdata import kv
from charmhelpers.core.host import service_restart

import os


@when_not('configfile.ready')
def ready():
    config = hookenv.config()
    filename = config['filename']
    if filename:
        write_config()
        status_set('active', 'Ready')
        set_state('configfile.ready')
    else:
        status_set('blocked', 'Filename required')


@when('config.changed.filename')
def filename_changed():
    cache = kv()
    config = hookenv.config()

    filename = config['filename']
    oldfilename = cache.get('configfile.filename')

    if oldfilename:
        try:
            os.remove(oldfilename)
        except FileNotFoundError:
            pass

    if filename:
        cache.set('configfile.filename', filename)
        data_changed('content', "")
        write_config()
    else:
        status_set('blocked', 'Filename required')
        remove_state('configfile.ready')


@when('config.changed.content')
@when('configfile.ready')
def write_config():
    cache = kv()
    config = hookenv.config()
    filename = config['filename']
    if filename:
        cache.set('configfile.filename', filename)
        set_state('configfile.ready')
        if data_changed('content', config['content']):
            log("Writing configfile {}".format(filename))
            app_name = hookenv.service_name()
            if config['content']:
                with open(filename, 'w') as conf_file:
                    conf_file.write(str(config['content']))
            else:
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass
            if config['restart_service']:
                service_restart(config['restart_service'])


@hook('stop')
def stopped():
    config = hookenv.config()
    filename = config['filename']
    if filename:
        log("Deleting conf file. {}".format(filename))
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
