from z3 import *

Frame = Datatype("Frame")
Frame.declare('type', ('val', IntSort()), ('streamId', IntSort()))
Frame.declare('priority', ('val', IntSort()))