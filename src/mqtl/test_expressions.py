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

  def test_UnOpExp_dispatching_eval_to_operate_on_value(self):
    operand = Exp()
    operand.eval  = MagicMock(return_value="operand")

    op = UnOpExp(operand)
    op._operate = MagicMock()
    op.eval("context")

    operand.eval.assert_called_with("context")
    op._operate.assert_called_with("operand")

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

  def test_NotExp_T_is_F(self):
    operand = Exp()
    operand.eval = MagicMock(return_value=True)
    self.assertFalse(NotExp(operand).eval())

  def test_NotExp_F_is_T(self):
    operand = Exp()
    operand.eval = MagicMock(return_value=False)
    self.assertTrue(NotExp(operand).eval())

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

  def test_ComparisonExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=1)
    right.eval  = MagicMock(return_value=1.0)
    op = ComparisonExp(left, right)
    op._compare = MagicMock()
    op.eval()
    op._compare.assert_called_with(1, 1.0)

  def test_ComparisonExp_with_boolean_conversion(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=1)
    right.eval  = MagicMock(return_value=False)
    op = ComparisonExp(left, right)
    op._compare = MagicMock()
    op.eval()
    op._compare.assert_called_with(True, False)

    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=True)
    right.eval  = MagicMock(return_value="")
    op = ComparisonExp(left, right)
    op._compare = MagicMock()
    op.eval()
    op._compare.assert_called_with(True, False)

  def test_EQExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=1)
    right.eval  = MagicMock(return_value=1.0)
    self.assertTrue(EQExp(left, right).eval())

    left.eval   = MagicMock(return_value="a")
    right.eval  = MagicMock(return_value=123)
    self.assertFalse(EQExp(left, right).eval())

  def test_NEQExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=1)
    right.eval  = MagicMock(return_value=1.0)
    self.assertFalse(NEQExp(left, right).eval())

    left.eval   = MagicMock(return_value="a")
    right.eval  = MagicMock(return_value=123)
    self.assertTrue(NEQExp(left, right).eval())

  def test_LTExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=1)
    right.eval  = MagicMock(return_value=3)
    self.assertTrue(LTExp(left, right).eval())

    left.eval   = MagicMock(return_value=3)
    right.eval  = MagicMock(return_value=3)
    self.assertFalse(LTExp(left, right).eval())

  def test_LTEQExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=1)
    right.eval  = MagicMock(return_value=3)
    self.assertTrue(LTExp(left, right).eval())

    left.eval   = MagicMock(return_value=3)
    right.eval  = MagicMock(return_value=3)
    self.assertTrue(LTEQExp(left, right).eval())

  def test_GTExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=3)
    right.eval  = MagicMock(return_value=1)
    self.assertTrue(GTExp(left, right).eval())

    left.eval   = MagicMock(return_value=3)
    right.eval  = MagicMock(return_value=3)
    self.assertFalse(GTExp(left, right).eval())

  def test_GTEQExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=3)
    right.eval  = MagicMock(return_value=1)
    self.assertTrue(GTEQExp(left, right).eval())

    left.eval   = MagicMock(return_value=3)
    right.eval  = MagicMock(return_value=3)
    self.assertTrue(GTEQExp(left, right).eval())

  def test_val2number(self):
    self.assertEqual(val2number(123), 123)
    self.assertEqual(val2number(123.0), 123)
    self.assertEqual(val2number("123"), 123)
    self.assertEqual(val2number("123.0"), 123)
    self.assertTrue(math.isnan(val2number("abc")))

  def test_NegationExp(self):
    operand = Exp()
    operand.eval = MagicMock(return_value=123)
    self.assertEqual(NegationExp(operand).eval(), -123)

    operand.eval = MagicMock(return_value=-123)
    self.assertEqual(NegationExp(operand).eval(), 123)

  def test_AddExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=15)
    right.eval  = MagicMock(return_value=8)
    self.assertEqual(AddExp(left, right).eval(), 23)

  def test_SubExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=15)
    right.eval  = MagicMock(return_value=8)
    self.assertEqual(SubExp(left, right).eval(), 7)

  def test_MulExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=15)
    right.eval  = MagicMock(return_value=8)
    self.assertEqual(MulExp(left, right).eval(), 120)

  def test_DivExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=18)
    right.eval  = MagicMock(return_value=3)
    self.assertEqual(DivExp(left, right).eval(), 6)

  def test_SubExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=15)
    right.eval  = MagicMock(return_value=8)
    self.assertEqual(SubExp(left, right).eval(), 7)

  def test_ModExp(self):
    left, right = Exp(), Exp()
    left.eval   = MagicMock(return_value=15)
    right.eval  = MagicMock(return_value=4)
    self.assertEqual(ModExp(left, right).eval(), 3)
