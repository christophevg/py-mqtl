import inspect

# generic generator-visitor for object hierarchies, using inspection

def visit(obj, previous_stack=[]):
  stack = list(previous_stack)  # copy to achieve by value
  yield (None, obj, stack)      # visit self
  stack.append(obj)             # add to stack

  for key, value in inspect.getmembers(obj):
    # skip built-ins, None values and basic types
    if key.startswith("__"): continue
    if value is None: continue
    if isinstance(value, (bool, str, int)): continue

    # handle (lists of) objects
    if not isinstance(value, list): value = [value]

    for child in value:
      for k, v, s in visit(child, stack):
        if not k: k = key
        yield (k, v, s)

  if len(stack) == 1: raise StopIteration()
