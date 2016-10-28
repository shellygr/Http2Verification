from z3 import *

# Datatypes for Nodes (GW, host), rule (algebraic) and RB (list of rules)
Node = Datatype("Node")
Node.declare('node', ('id', IntSort()), ('isGw', BoolSort()), ('isDnsServer', BoolSort()), ('isHttpProxy', BoolSort()), ('allowOutgoing', BoolSort()), ('hasNextProxy', BoolSort()), ('hasUrlf', BoolSort()), ('hasAv', BoolSort()), ('hasAb', BoolSort()))
# Node.declare('node', ('id', IntSort()), )
Node = Node.create()

Rule = Datatype('Rule')
Rule.declare('rule', ('src', IntSort()), ('dst', IntSort()), ('service', IntSort()), ('isAllow', BoolSort())) # Src, dst, service can be lists, negation support, more columns
Rule = Rule.create()

RuleList = Datatype('RuleList')
RuleList.declare('cons', ('car', Rule), ('cdr', RuleList))
RuleList.declare('nil')
RuleList = RuleList.create()

hasRoute = Function('hasRoute', Node, Node, BoolSort())

def createObjectRules(node):
    # node = Const('node', Node)
    # ForAll causes it to become unsat! not EPR
    return Not(And(Node.isGw(node), Node.isDnsServer(node)))

def prettyPrint(node):
    # print node.__class__.__name__
    if isinstance(node, DatatypeRef):
        # print "sort", node.sort()
        children = node.children()
        id = children[0]
        isGw = children[1]
        isDnsServer = children[2]
        isHttpProxy = children[3]
        allowOutgoing = children[4]
        hasNextProxy = children[5]
        hasUrlf = children[6]
        hasAv = children[7]
        hasAb = children[8]
        if is_true(isGw):
            return "Gateway - isHttpProxy = %s, allowOutgoing = %s, hasNextProxy = %s, hasUrlf = %s, hasAv = %s, hasAb = %s" %(isHttpProxy, allowOutgoing,hasNextProxy, hasUrlf,hasAv,hasAb)
        elif is_true(isDnsServer):
            return "DNS server"
        else:
            return "General node"
    else:
        return node