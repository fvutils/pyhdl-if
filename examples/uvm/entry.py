from hdl_if.via import Root, error, info

class Entry(Root):

    def post_build(self, root):
        try:
            print("-- post_build", flush=True)
            print("  ob: %s" % str(root), flush=True)
            print("  name: %s" % root.get_name(), flush=True)
            print("  full_name: %s" % root.get_full_name(), flush=True)
        except Exception as e:
            print("Exception: %s" % str(e), flush=True)

    def post_connect(self, root):
        info(1, "Hello World!")
        for i in range(100):
            print("post_connect", flush=True)
        pass

    async def run(self, root):
        for i in range(100):
            print("run", flush=True)
        pass

