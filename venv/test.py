import unittest
from FindSame import Same
from RootClass import Root
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        root = Root(os.getcwd(), "test")
        root.init("test", root.Albums[0], True)
        same = Same(root)
        fl = same.find_copy(0.5, None)
        self.assertEqual(len(same.Albums), 3)


if __name__ == '__main__':
    unittest.main()
