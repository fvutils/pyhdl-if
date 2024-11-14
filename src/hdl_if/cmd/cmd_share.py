
class CmdShare(object):

    def __call__(self, args):
        from hdl_if import share
        print(share())

