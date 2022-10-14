import aiohttp.test_utils, aiohttp.web
import time

def dont_print (s):
    return

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
