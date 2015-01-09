""""A rather generic implementation of a basic expression language."""

import math

class Exp(object):
  """Abstract base class for expressions."""

  def eval(self, context=None):
    """Evaluates the expression in the given context."""

class UnOpExp(Exp):
  """Abstract base class for unary operators."""

  def __init__(self, operand):
    self.operand = operand

  def eval(self, context=None):
    return self._operate(self.operand.eval(context))

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

# logical expressions

class NotExp(UnOpExp):
  def _operate(self, operand):
    return not val2bool(operand)

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

# comparison expressions

class ComparisonExp(BinOpExp):
  """
  Abstract base class for comparison expressions, preparing values for
  comparison.
  """
  def _operate(self, left, right):
    if is_bool(left) or is_bool(right):
      return self._compare(val2bool(left), val2bool(right))
    return self._compare(left, right)

class EQExp(ComparisonExp):
  def _compare(self, left, right):
    return left == right

class NEQExp(ComparisonExp):
  def _compare(self, left, right):
    return left != right

class LTExp(ComparisonExp):
  def _compare(self, left, right):
    return left < right

class LTEQExp(ComparisonExp):
  def _compare(self, left, right):
    return left <= right

class GTExp(ComparisonExp):
  def _compare(self, left, right):
    return left > right

class GTEQExp(ComparisonExp):
  def _compare(self, left, right):
    return left >= right

# arithmatic expressions

def val2number(value):
  """Converts a value to a number."""
  try:
    return float(value)
  except ValueError:
    return float('NaN')

class NegationExp(UnOpExp):
  def _operate(self, operand):
    return - val2number(operand)

class AddExp(BinOpExp):
  def _operate(self, left, right):
    return val2number(left) + val2number(right)

class SubExp(BinOpExp):
  def _operate(self, left, right):
    return val2number(left) - val2number(right)

class MulExp(BinOpExp):
  def _operate(self, left, right):
    return val2number(left) * val2number(right)

class DivExp(BinOpExp):
  def _operate(self, left, right):
    return val2number(left) / val2number(right)

class ModExp(BinOpExp):
  def _operate(self, left, right):
    return val2number(left) % val2number(right)
