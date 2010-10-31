#!/usr/bin/env python
"""Unittests for testing.py"""

import testing

class TestCase(testing.TestCase):

    def testBasic(self):
        """The most basic test."""
        self.assertEqual(True, True)

    def test_assert_iterator(self):
        """Test the test_iterator() method"""
        iterator = iter([1,2,3,4])
        # Should pass
        self.assert_iterator(iterator,
                           count=4,
                           assert_item_function=lambda i: i>0)

if __name__ == "__main__":
    testing.main()
