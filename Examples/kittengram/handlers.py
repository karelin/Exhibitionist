# from exhibitionist.toolbox import  http_handler,JSONRequestHandler,Template
import os
import codecs
import threading
from exhibitionist.toolbox import *

from tornado.template import Template

context = None # lose the warnings

@http_handler(r'/numpy/{{objid}}/(?P<animal>cat|dog)')
class KittenGram(JSONRequestHandler):
    def __init__(self, *args, **kwds):
        super(KittenGram, self).__init__(*args, **kwds)
        tmpl_file = os.path.join(self.get_template_path(), "index.html")
        data = codecs.open(tmpl_file).read()
        self.tmpl = Template(data)

    def get(self, objid, animal):
        if self.get_argument("format", "").lower() == "json":
            self.write_json(context.object)
        else:
            api_url = context.get_view_url("KittenGram", context.object, animal)
            ws_url = context.get_ws_url()
            self.write(self.tmpl.generate(objid=objid,
                                          api_url=api_url + '?format=json',
                                          ws_url=ws_url,
                                          animal=animal,
                                          static_url=self.static_url))
