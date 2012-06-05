# -*- coding: utf-8 -*-

""" Methods used to include / register web parts (images, CSS & JS files) throughout the application """
from app.utils.mm import multimethod
import web

# Built-in CSS & JS files
CSS_JQUERYUI = "jquery-ui-1.8.20.custom.css"
JS_JQUERY = "jquery-1.7.2.min.js"
JS_JQUERYUI = ["jquery-ui-1.8.20.custom.min.js", "jquery.ui.datepicker-fr.js"]
JS_JQUERY_AND_FORMS = [JS_JQUERY, "forms.js"]

def ajax_animation(animation_id):
    """ Returns a 16 x 16 wheel animation, hidden by default """
    return "<img style=\"width: 16px; height: 16px; display: none;\" id=\"%s\" src=\"/public/img/ajax-loader.gif\" />" % animation_id

def init_webparts():
    """ Initializes 2 empty lists (CSS & JS files) inside the context at the beginning of every request into which each view can register components """
    web.ctx.registered_stylesheets = []
    web.ctx.registered_scripts = []

def register_stylesheet(stylesheet_name):
    """ Appends the provided CSS (file name only) into the CSS list for further inclusion """
    web.ctx.registered_stylesheets.append(stylesheet_name)

def registered_stylesheets():
    """ Returns the registered CSS files for the current request """
    return web.ctx.registered_stylesheets

@multimethod(str)
def register_script(script_name):
    """ Appends the provided JS (file name only) into the JS list for further inclusion """
    web.ctx.registered_scripts.append(script_name)

@multimethod(list)
def register_script(bundled_script):
    """ Appends all dependencies of the provided bundled script into the JS list for further inclusion """
    for script_name in bundled_script:
        register_script(script_name)

def registered_scripts():
    """ Returns the registered JS files for the current request """
    return web.ctx.registered_scripts
