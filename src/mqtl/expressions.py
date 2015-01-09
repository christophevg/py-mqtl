""""A rather generic implementation of a basic expression language."""

import math

class Exp(object):
  """Abstract base class for expressions."""

  def eval(self, context=None):
    """Evaluates the expression in the given context."""

class BinOpExp(Exp):
  """Abstract base class for binary operators."""

  def __init__(self, left, right):
    self.left  = left
    self.right = right

  def eval(self, context=None):
    return self._operate(self.left.eval(context),
                         self.right.eval(context))
  
  def _operate(self, left, right):
    """Utility function. Performs actual binary operate on operand values."""

def is_bool(value):
  """Returns true if value is a bool."""
  return isinstance(value, bool)

def is_int(value):
  """Returns true if value is a int."""
  return isinstance(value, int)

def is_float(value):
  """Returns true if value is a float."""
  return isinstance(value, float)

def is_string(value):
  """Returns true if value is a string."""
  return isinstance(value, basestring)

def is_number(value):
  """Returns true if value is a number."""
  return not is_bool(value) and ( is_int(value) or is_float(value) )

def val2bool(value):
  """Converts a value to a bool."""
  if is_number(value):
    return value != 0 and not math.isnan(value)
  elif is_string(value):
    return value != ""
  elif is_bool(value):
    return value
  else:
    raise ValueError, "Value can not be represented as a boolean."

class AndExp(BinOpExp):
  def eval(self, context=None):
    # don't use _operate here, to keep short-cutting and-op
    return val2bool(self.left.eval(context)) \
       and val2bool(self.right.eval(context))

class OrExp(BinOpExp):
  def eval(self, context=None):
    # don't use _operate here, to keep short-cutting or-op
    return val2bool(self.left.eval(context)) \
        or val2bool(self.right.eval(context))
