# -*- coding: utf-8 -*-

""" WSGI wrapper (see http://wiki.dreamhost.com/Passenger_WSGI) """

import os
import sys


# Environment-related settings
INTERP = os.path.join(os.environ["HOME"], "ENV", "bin", "python")
CONFIGURATION_FILE = "production.cfg"

# On-the-fly interpreter change
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

# Application configuration
import application as application_module
application_module.app.configure(CONFIGURATION_FILE)

# The file must export a WSGI server with the name application
application = application_module.app.wsgifunc() #@UndefinedVariable