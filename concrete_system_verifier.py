from datatypes import *


def connectivity(node1, node2):
   # return And(Node.allowOutgoing(node1), hasRoute(node1, node2))
    return hasRoute(node1, node2)

def assumeHasRoutes():
    node1, node2 = Consts('node1 node2', Node)
    return ForAll([node1, node2], (hasRoute(node1, node2)))

def createProxyConnectivityRule(gw, dnsServer):
    return Implies(And(Node.isGw(gw), Node.isHttpProxy(gw), Node.isDnsServer(dnsServer)),
                        And(Or(Node.allowOutgoing(gw), Node.hasNextProxy(gw)),
                            connectivity(gw, dnsServer)))

def createRadConnectivityRule(gw):
    return Implies(Or(Node.hasUrlf(gw), Node.hasAv(gw), Node.hasAb(gw)),
                   And(Node.allowOutgoing(gw), Node.hasNextProxy(gw)))

# Create solver and add rules to it defining what is a correct configuration.
s = Solver() # Empty solver is illegal, must add rules and validations

# Declare objects
gw = Const('gw1', Node)

s.add(Node.isGw(gw))
s.add(Not(Node.isDnsServer(gw)))
s.add(Node.isHttpProxy(gw))
s.add(Node.hasUrlf(gw))
s.add(Node.hasAv(gw))
s.add(Not(Node.hasAb(gw)))

s.add(Not(Node.allowOutgoing(gw))) # Bad
# s.add(Node.allowOutgoing(gw)) # Good

s.add(Not(Node.hasNextProxy(gw))) # Bad
# s.add(Node.hasNextProxy(gw)) # Good

dnsServer = Const('dnsServer1', Node)
s.add(Node.isDnsServer(dnsServer))

# We assume routes are OK (can fill automatically)
s.add(assumeHasRoutes())

# We search for a violation of any of the rules
proxyConnectivityRule = createProxyConnectivityRule(gw, dnsServer)
radConnectivityRule = createRadConnectivityRule(gw)

s.add(Or(Not(proxyConnectivityRule),Not(radConnectivityRule))) # At least one of the rules should be violated

res = s.check()
# print res
# print s.sexpr()
if res==unsat:
    print "All configurations are legal"
else:
    print "There are illegal configurations: "
    model = s.model()
    for node in model:
        print "\t", node, "is", prettyPrint(model[node])

    if is_false(model.eval(proxyConnectivityRule)):
        print "Proxy connectivity rule was violated"

    if is_false(model.eval(radConnectivityRule)):
        print "RAD connectivity rule was violated"

    # print s.model()