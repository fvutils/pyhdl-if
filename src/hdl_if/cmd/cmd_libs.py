
class CmdLibs(object):

    def __call__(self, args):
        from hdl_if import libs
        print(" ".join(libs()))
