# -*- coding: utf-8 -*-

import mimetypes
import web

class Public:
    
    def GET(self): 
        try:
            path = web.ctx.path
            file_name = path.split("/")[-1]
            web.header("Content-type", mime_type(file_name))
            return open(path[1:], "rb").read()
        except IOError:
            raise web.notfound()
            
def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or "application/octet-stream" 
