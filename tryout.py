from z3 import *

# Declare frame datatype in 2 steps - first the payload, then the frame wrapper.
FramePayload = Datatype("FramePayload")
# Declare constructors according to frame types, including accessors
FramePayload.declare('priority', ('exclusive', BoolSort()), ('dependency', IntSort()), ('weight', IntSort()))
FramePayload.declare('data', ('padlen', IntSort()), ('dataLenInFrame', IntSort()), ('padlenInFrame', IntSort()) ) # Both padlens need to be equal
FramePayload.declare('headers', ('padlen', IntSort()), ('exclusive', BoolSort()), ('dependency', IntSort()), ('headerBlockLen', IntSort()), ('padlenInFrame', IntSort()) ) # Both padlens need to be equal
FramePayload.declare('rst_stream', ('errorCode', IntSort()))
FramePayload.declare('settings', ('id', IntSort()), ('value', IntSort()))
FramePayload.declare('push_promise', ('padlen', IntSort()), ('reservedStreamId', IntSort()), ('headerBlockLen', IntSort()), ('padlenInFrame', IntSort()) ) # Both padlens need to be equal
FramePayload.declare('ping')
FramePayload.declare('goaway', ('lastStreamId', IntSort()), ('errorCode', IntSort()))
FramePayload.declare('ping', ('windowInc', IntSort()))
FramePayload.declare('continuation', ('headerBlockLen', IntSort()))

# Create the data type
FramePayload = FramePayload.create()

# Now creating the wrapped datatype
Frame = Datatype("Frame")
Frame.declare('frame', ('length', IntSort()), ('type', IntSort()), ('flags', IntSort()), ('streamId', IntSort()), ('payload', FramePayload) )

Frame = Frame.create()

print "Created", Frame

# Now, model our state machine. It should match the actual code.
# TODO: Put some simple example model for the POC

# In the end, we shall write a formula: exists a state and exists a frame such that leads to an error / no new state (can be written without quantifiers)