import unittest
import mock
from mock import MagicMock

from mqtl.expressions import *

class TestExpressions(unittest.TestCase):
  
  def test_BinOpExp_dispatching_eval_to_operate_on_values(self):
    left  = Exp()
    right = Exp()
    left.eval  = MagicMock(return_value="left")
    right.eval = MagicMock(return_value="right")

    op = BinOpExp(left, right)
    op._operate = MagicMock()
    op.eval("context")

    left.eval.assert_called_with("context")
    right.eval.assert_called_with("context")
    op._operate.assert_called_with("left", "right")

  def test_is_bool(self):
    self.assertTrue(is_bool(True))
    self.assertTrue(is_bool(False))

    self.assertFalse(is_bool(0))
    self.assertFalse(is_bool(123))
    self.assertFalse(is_bool(-123))

  def test_is_int(self):
    self.assertTrue(is_int(123))
    self.assertTrue(is_int(-123))

    self.assertFalse(is_int(123.0))

  def test_is_float(self):
    self.assertTrue(is_float(123.0))
    self.assertTrue(is_float(-123.0))

    self.assertFalse(is_float(123))

  def test_is_string(self):
    self.assertTrue(is_string("hello"))
    self.assertTrue(is_string(""))

    self.assertFalse(is_string(123))
    self.assertFalse(is_string(123.0))
    self.assertFalse(is_string(True))

  def test_is_number(self):
    self.assertTrue(is_number(123))
    self.assertTrue(is_number(0))
    self.assertTrue(is_number(-123))
    self.assertTrue(is_number(123.0))
    self.assertTrue(is_number(-123.0))

    self.assertFalse(is_number(True))
    self.assertFalse(is_number("test"))
    self.assertFalse(is_number(""))

  def test_val2bool(self):
    self.assertTrue(val2bool(1))
    self.assertTrue(val2bool("test"))
    self.assertTrue(val2bool(True))

    self.assertFalse(val2bool(0))
    self.assertFalse(val2bool(float('NaN')))
    self.assertFalse(val2bool(""))
    self.assertFalse(val2bool(False))

    self.assertRaises(ValueError, val2bool, {})

  def test_AndExp_TT_is_T(self):
    left, right = Exp(), Exp()
    left.eval  = MagicMock(return_value=True)
    right.eval = MagicMock(return_value=True)
    self.assertTrue(AndExp(left, right).eval())

  def test_AndExp_FT_is_F(self):
    left, right = Exp(), Exp()
    left.eval  = MagicMock(return_value=False)
    right.eval = MagicMock(return_value=True)
    self.assertFalse(AndExp(left, right).eval())
    # And is short-cutting
    left.eval.assert_called_with(None)
    self.assertFalse(right.eval.called)

  def test_AndExp_TF_is_F(self):
    left, right = Exp(), Exp()
    left.eval  = MagicMock(return_value=True)
    right.eval = MagicMock(return_value=False)
    self.assertFalse(AndExp(left, right).eval())
    # And is short-cutting, but can't here
    left.eval.assert_called_with(None)
    right.eval.assert_called_with(None)

  def test_AndExp_FF_is_F(self):
    left, right = Exp(), Exp()
    left.eval  = MagicMock(return_value=False)
    right.eval = MagicMock(return_value=False)
    self.assertFalse(AndExp(left, right).eval())
    # And is short-cutting
    left.eval.assert_called_with(None)
    self.assertFalse(right.eval.called)

  def test_OrExp_TT_is_T(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=True)
    right.eval  = MagicMock(return_value=True)
    self.assertTrue(OrExp(left, right).eval())
    # Or is short-cutting
    left.eval.assert_called_with(None)
    self.assertFalse(right.eval.called)

  def test_OrExp_FT_is_T(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=False)
    right.eval  = MagicMock(return_value=True)
    self.assertTrue(OrExp(left, right).eval())
    # Or is short-cutting, but can't here
    left.eval.assert_called_with(None)
    right.eval.assert_called_with(None)

  def test_OrExp_TF_is_T(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=True)
    right.eval  = MagicMock(return_value=False)
    self.assertTrue(OrExp(left, right).eval())
    # Or is short-cutting
    left.eval.assert_called_with(None)
    self.assertFalse(right.eval.called)

  def test_OrExp_FF_is_F(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=False)
    right.eval  = MagicMock(return_value=False)
    self.assertFalse(OrExp(left, right).eval())
    # Or is short-cutting, but can't here
    left.eval.assert_called_with(None)
    right.eval.assert_called_with(None)
