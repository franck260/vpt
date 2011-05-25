#!/home/franck260/ENV/bin/python

import application
application.app.configure("production.cfg")
application.app.run()