from ..decorators import api, imp

@api
class RootIF(object):

    @imp
    def info(self, level : int, msg : str): pass

    @imp
    def error(self, msg : str): pass

    @imp
    def fatal(self, msg : str): pass
