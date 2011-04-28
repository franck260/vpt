'''
Created on 17 nov. 2010

@author: fperez
'''

import web
from app.utils import formatting

# Init des vues
views = web.template.render("app/views/", globals={
   "formatting": formatting,
   "zip": zip,
   "getattr": getattr,
   "class_name": lambda x: x.__class__.__name__
})

# Autres constantes
DATABASE = "sqlite:///vpt.db"
