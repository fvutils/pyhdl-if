
from ..decorators import api, exp

@api
class Root(object):

    @exp
    def post_build(self, root : object):
        pass

    @exp
    def post_connect(self, root : object):
        pass

    @exp
    async def run(self, root : object):
        pass