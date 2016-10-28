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

def createProxyValidation():
    gw = Const('gw1', Node)
    dnsServer = Const('dnsServer1', Node)
    return Implies(And(Node.isGw(gw), Node.isHttpProxy(gw), Node.isDnsServer(dnsServer)),
                        Or(Node.allowOutgoing(gw), Node.hasNextProxy(gw)))

# Create solver and add rules to it defining what is a correct configuration.
s = Solver() # Empty solver is illegal, must add rules and validations

# Declare objects
gw = Const('gw1', Node)
dnsServer = Const('dnsServer1', Node)
s.add(createObjectRules(gw))
s.add(createObjectRules(dnsServer))

# We search for a violation of any of the rules
s.add(Not(createProxyConnectivityRule(gw, dnsServer)))                                           # To search in general for violating configurations possible, use for all?

# Given a set of validations we added to our logic
# s.add(createProxyValidation())
s.add(assumeHasRoutes())

res = s.check()
# print res
# print s.sexpr()
if res==unsat:
    print "All configurations are legal"

else:
    print "There are illegal configurations: "
    model = s.model()
    for node in model:
        print node, "is", prettyPrint(model[node])
    # TODO: Find the violated rule
    # print s.model()