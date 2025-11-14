from hdl_if import api, imp
from .component import uvm_component

@api
class uvm_analysis_port_proxy(uvm_component):

    @imp
    def add_listener(self, l : object):
        ...
