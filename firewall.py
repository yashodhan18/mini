from pox.core import core
import pox.openflow.libopenflow_01 as of

class Firewall(object):
    def __init__(self):
        self.connection = None
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        self.connection = event.connection
        self.add_firewall_rules()

    def add_firewall_rules(self):
        fm = of.ofp_flow_mod()

        # Drop traffic from h1 to h2
        fm.match.dl_type = 0x0800
        fm.match.nw_src = '10.0.0.1'
        fm.match.nw_dst = '10.0.0.2'
        self.connection.send(fm)

        # Drop traffic from h2 to h1
        fm.match.dl_type = 0x0800
        fm.match.nw_src = '10.0.0.2'
        fm.match.nw_dst = '10.0.0.1'
        self.connection.send(fm)

def launch():
    core.registerNew(Firewall)