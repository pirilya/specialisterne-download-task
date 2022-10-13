class dummy_response:
    def __init__(self, is_ok, is_pdf, will_timeout):
        self.ok = is_ok
        self.content_type = "application/pdf" if is_pdf else "text/html"
        self.will_timeout = will_timeout
    async def read():
        if self.will_timeout:
            time.sleep(1000)
        return "this is definitely pdf data"
    def __await__(self, *args, **kwargs):
        print("he", args, kwargs)
        return iter([])

class dummy_session:
    def __init__(self):
        pass
    class get:
        def __init__(self, url, **kwargs):
            self.url = url
        def __aenter__(self, **kwargs):
            print("blah", self, kwargs)
            is_ok = "non-resolving" in self.url
            is_pdf = "pdf" in self.url
            will_timeout = "timeout" in self.url
            return dummy_response(is_ok, is_pdf, will_timeout)
        def __aexit__(self, *args, **kwargs):
            return dummy_response(True, True, True)

def dont_print (s):
    return