# Overview

This charm will manage a individual custom config file.
Additionally it can restart a system service if the file content was changed.

# Usage

juju deploy ubuntu

juju deploy configfile custommod

juju add-relation ubuntu custommod

juju config custommod filename=/etc/custommod.conf

juju config custommod restart_service=custommodd

juju config custommod content="FILE CONTENT"

This will result in a config file named /etc/custommod.conf containing "FILE CONTENT"


# Configuration

The content of the 'content' field is directly written in the config file.
No templating or syntax check is performed.


https://github.com/tbaumann/jujucharm-configfile
