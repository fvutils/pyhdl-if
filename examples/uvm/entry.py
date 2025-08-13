from hdl_if.via import Root, error, info

class Entry(Root):

    def post_build(self, root):
        try:
            print("-- post_build", flush=True)
            print("  ob: %s" % str(root), flush=True)
            print("  name: %s" % root.get_name(), flush=True)
            print("  full_name: %s" % root.get_full_name(), flush=True)

            obj = root.create_object_by_name("trans_a", "abc")
            print("obj: %s" % obj.get_name())
            obj_t = obj.get_object_type()
            print("obj_t: %s" % obj_t.get_name())
            fields = obj_t.get_fields()
            print("fields: %s" % str(fields))
            obj = None
        except Exception as e:
            print("Exception: %s" % str(e), flush=True)

    def post_connect(self, root):
        info(1, "Hello World!")
        print("post_connect", flush=True)

    async def run(self, root):
        print("run", flush=True)

