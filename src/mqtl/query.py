from mqtl.visitor import visit

def find(model, withproperties=[]):
  for key, obj, stack in visit(model):
    for attr, value in withproperties:
      if getattr(obj, attr) != value: break
    else: yield (key, obj, stack)
