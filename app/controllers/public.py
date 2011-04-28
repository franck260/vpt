# -*- coding: utf-8 -*-

'''
Created on 19 nov. 2010

@author: fperez
'''
 
from app.utils import session
import mimetypes
import web


class Public:
    
    @session.configure_session(enabled = False)
    def GET(self): 
        public_dir = 'public'
        try:
            path = web.ctx.path
            file_name = path.split('/')[-1]
            web.header('Content-type', mime_type(file_name))
            return open(public_dir + web.ctx.path, 'rb').read()
        except IOError:
            raise web.notfound()
            
def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream' 
