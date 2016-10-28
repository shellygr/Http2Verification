from z3 import *

# Datatypes for Nodes (GW, host), rule (algebraic) and RB (list of rules)
Node = Datatype("Node")
Node.declare('gw', ('id', IntSort()), ('isHttpProxy', BoolSort()), ('allowOutgoing', BoolSort()), ('hasNextProxy', BoolSort()), ('hasUrlf', BoolSort()), ('hasAv', BoolSort()), ('hasAb', BoolSort()))
Node.declare('node', ('id', IntSort()))
Node = Node.create()

Rule = Datatype('Rule')
Rule.declare('rule', ('src', IntSort()), ('dst', IntSort()), ('service', IntSort()), ('isAllow', BoolSort())) # Src, dst, service can be lists, negation support, more columns
Rule = Rule.create()

RuleList = Datatype('RuleList')
RuleList.declare('cons', ('car', Rule), ('cdr', RuleList))
RuleList.declare('nil')
RuleList = RuleList.create()

# Create solver and add rules to it defining what is a correct configuration.
s = Solver() # Empty solver is legal - no rules

# Declare objects
gw = Const('gw1', Node)
dnsServer = Const('dnsServer1', Node)

proxyConnectivityRule = Implies(Node.isHttpProxy(gw), Or(Node.allowOutgoing(gw), Node.hasNextProxy(gw))) # TODO Add connectivity predicate

# We search for a violation of any of the rules
s.add(Not(proxyConnectivityRule)) # To search in general for violating configurations possible, use for all?

# We add constraints based on our knowledge of the objects
s.add(And(Node.isHttpProxy(gw), Node.allowOutgoing(gw)))

res = s.check()
print res
print s.model()


#
# # Declare frame datatype in 2 steps - first the payload, then the frame wrapper.
# FramePayload = Datatype("FramePayload")
# # Declare constructors according to frame types, including accessors
# FramePayload.declare('priority', ('exclusive', BoolSort()), ('dependency', IntSort()), ('weight', IntSort()))
# FramePayload.declare('data', ('padlen', IntSort()), ('dataLenInFrame', IntSort()), ('padlenInFrame', IntSort()) ) # Both padlens need to be equal
# FramePayload.declare('headers', ('padlen', IntSort()), ('exclusive', BoolSort()), ('dependency', IntSort()), ('headerBlockLen', IntSort()), ('padlenInFrame', IntSort()) ) # Both padlens need to be equal
# FramePayload.declare('rst_stream', ('errorCode', IntSort()))
# FramePayload.declare('settings', ('id', IntSort()), ('value', IntSort()))
# FramePayload.declare('push_promise', ('padlen', IntSort()), ('reservedStreamId', IntSort()), ('headerBlockLen', IntSort()), ('padlenInFrame', IntSort()) ) # Both padlens need to be equal
# FramePayload.declare('ping')
# FramePayload.declare('goaway', ('lastStreamId', IntSort()), ('errorCode', IntSort()))
# FramePayload.declare('ping', ('windowInc', IntSort()))
# FramePayload.declare('continuation', ('headerBlockLen', IntSort()))
#
# # Create the data type
# FramePayload = FramePayload.create()
#
# # Now creating the wrapped datatype
# Frame = Datatype("Frame")
# Frame.declare('frame', ('length', IntSort()), ('type', IntSort()), ('flags', IntSort()), ('streamId', IntSort()), ('payload', FramePayload) )
#
# Frame = Frame.create()
#
# print "Created", Frame
#
# # Now, model our state machine. It should match the actual code.
# # TODO: Put some simple example model for the POC
#
# # In the end, we shall write a formula: exists a state and exists a frame such that leads to an error / no new state (can be written without quantifiers)