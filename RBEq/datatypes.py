from z3 import *


def check(param):
    s = Solver()
    s.add(param)

    res = s.check()
    # print res
    # print s.sexpr()
    if res==unsat:
        print "Rulebases are equivalent"
    else:
        print "There is traffic for which the rulebases are inequivalent: "
        model = s.model()
        print model



# Declare uninterpreted sorts?

#####Traffic datatype
# Traffic = Datatype("Traffic")
# Traffic.declare()

TrafficSort = DeclareSort("Traffic")

# Action datatype
Action = Datatype("Action")
Action.declare("Accept")
Action.declare("Drop")
Action = Action.create()

HTTP = Function("HTTP", TrafficSort, BoolSort())
SecretWebServer = Function("SecretWebServer", TrafficSort, BoolSort())
result = Const('result', Action)
x = Const('x', TrafficSort)

r1 = HTTP(x)
r2 = True
rb1 = And(Implies(r1,result==Action.Drop),Implies(And(Not(r1),r2),result==Action.Drop))
rb2 = result==Action.Drop

# print rb1, rb1.__class__.__name__
# print rb2, rb1.__class__.__name__
check(rb1!=rb2)

print "------------------------------------------------------------------------"

ruleA1 = And(SecretWebServer(x), HTTP(x))
ruleA2 = HTTP(x)
ruleA3 = True

ruleB1 = HTTP(x)
ruleB1_1 = SecretWebServer(x)
ruleB1_2 = True
ruleB2 = True

rb1 = And(Implies(ruleA1,result==Action.Drop), Implies(And(Not(ruleA1),ruleA2),result==Action.Accept),Implies(And(Not(ruleA1),Not(ruleA2),ruleA3),result==Action.Drop))
L1 = And(Implies(ruleB1_1,result==Action.Drop), Implies(And(Not(ruleB1_1),ruleB1_2),result==Action.Accept))
rb2 = And(Implies(ruleB1,L1),Implies(And(Not(ruleB1),ruleB2),result==Action.Drop))
#
# print rb1, rb1.__class__.__name__
# print L1
# print rb2, rb1.__class__.__name__
check(rb1!=rb2)

print "------------------------------------------------------------------------"

ruleA1 = And(SecretWebServer(x), HTTP(x))
ruleA2 = HTTP(x)
ruleA3 = True

ruleB1 = HTTP(x)
ruleB1_1 = SecretWebServer(x)
ruleB1_2 = True
ruleB2 = True

rb1 = And(Implies(ruleA1,result==Action.Drop), Implies(And(Not(ruleA1),ruleA2),result==Action.Accept),Implies(And(Not(ruleA1),Not(ruleA2),ruleA3),result==Action.Drop))
L1 = And(Implies(ruleB1_1,result==Action.Accept), Implies(And(Not(ruleB1_1),ruleB1_2),result==Action.Drop))
rb2 = And(Implies(ruleB1,L1),Implies(And(Not(ruleB1),ruleB2),result==Action.Drop))
#
# print rb1, rb1.__class__.__name__
# print L1
# print rb2, rb1.__class__.__name__
check(rb1!=rb2)
