import aiohttp.test_utils, aiohttp.web
import time
import config_functions

async def make_server():
    async def respond (req):
        return aiohttp.web.Response(content_type = "application/pdf", body=b"%PDF-1.5")
    async def respond_text (req):
        return aiohttp.web.Response(content_type = "application/pdf", body=b"not a pdf file")
    app = aiohttp.web.Application()
    app.router.add_get("/works", respond)
    app.router.add_get("/not-pdf", respond_text)
    server = aiohttp.test_utils.TestServer(app)
    return server

class config(config_functions.config):
    def __init__(self, content_dict):
        self.__dict__ = content_dict
        self.error = None

class ui:
    class progress_bar:
        def add(self, *args):
            pass
    def __init__(self, *args):
        pass
    def communicate_error(self, *args):
        pass
    def communicate_progress (self, *args):
        pass
    def finish(self):
        pass

class flags:
    def __init__(self):
        self.skip_downloads = False
        self.has_timer = False
        self.from_empty = False
        self.only_first_hundred = False