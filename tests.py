import unittest
from main import Utrykk

Faktor = Utrykk.Ledd.Faktor

class TestFaktorArithmetic(unittest.TestCase):
    
    def test_mul_variable_variable(self):
        f1 = Faktor("x", isVariable=True)
        f2 = Faktor("y", isVariable=True)
        result = f1 * f2
        self.assertIsInstance(result, Utrykk.Ledd)
        self.assertIn("x", str(result))
        self.assertIn("y", str(result))

    def test_mul_constant_constant(self):
        f1 = Faktor("3")
        f2 = Faktor("4")
        result = f1 * f2
        self.assertEqual(str(result), "12")  # If implemented to multiply numbers
        self.assertFalse(result.isVariable)

    def test_mul_constant_variable(self):
        f1 = Faktor("3")
        f2 = Faktor("x", isVariable=True)
        result = f1 * f2
        self.assertIn("3", str(result))
        self.assertIn("x", str(result))

    def test_mul_variable_constant(self):
        f1 = Faktor("x", isVariable=True)
        f2 = Faktor("3")
        result = f1 * f2
        self.assertIn("3", str(result))
        self.assertIn("x", str(result))

    def test_mul_with_parens(self):
        f1 = Faktor("(x+1)", isParantes=True)
        f2 = Faktor("2")
        result = f1 * f2
        self.assertTrue(isinstance(result, Utrykk.Ledd))

    def test_rmul_int_variable(self):
        f = Faktor("x", isVariable=True)
        result = 3 * f
        self.assertIn("3", str(result))
        self.assertIn("x", str(result))

    def test_add_same_variable(self):
        f1 = Faktor("x", isVariable=True)
        f2 = Faktor("x", isVariable=True)
        result = f1 + f2
        self.assertIn("2", str(result))  # like 2x
        self.assertIn("x", str(result))

    def test_add_different_variable(self):
        f1 = Faktor("x", isVariable=True)
        f2 = Faktor("y", isVariable=True)
        result = f1 + f2
        self.assertIn("x", str(result))
        self.assertIn("y", str(result))

    def test_add_constant_constant(self):
        f1 = Faktor("2")
        f2 = Faktor("5")
        result = f1 + f2
        self.assertEqual(str(result), "7")

    def test_add_variable_constant(self):
        f1 = Faktor("x", isVariable=True)
        f2 = Faktor("5")
        result = f1 + f2
        self.assertIn("x", str(result))
        self.assertIn("5", str(result))

    def test_radd_int_variable(self):
        f = Faktor("x", isVariable=True)
        result = 3 + f
        self.assertIn("3", str(result))
        self.assertIn("x", str(result))

    def test_add_with_parens(self):
        f1 = Faktor("x", isVariable=True)
        f2 = Faktor("(y+1)", isParantes=True)
        result = f1 + f2
        self.assertTrue(isinstance(result, Utrykk))

    def test_add_with_potens(self):
        f1 = Faktor("x^2", isPotens=True)
        f2 = Faktor("x", isVariable=True)
        result = f1 + f2
        self.assertIn("x^2", str(result))
        self.assertIn("x", str(result))

if __name__ == "__main__":
    unittest.main()
