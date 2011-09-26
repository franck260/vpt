# -*- coding: utf-8 -*-

""" WSGI wrapper (see http://wiki.dreamhost.com/Passenger_WSGI) """

# On-the-fly interpreter change
import sys, os
INTERP = "/home/franck260/ENV2.7/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

# Application configuration
import application as application_module
application_module.app.configure("production.cfg")

# The file must export a WSGI server with the name application
application = application_module.app.wsgifunc() #@UndefinedVariable