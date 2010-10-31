"""Wrapper around unittest.TestCase adding functionality"""

import unittest

class TestCase(unittest.TestCase):
    """Wrapper around unittest.TestCase adding functionality"""

    def assert_iterator(self, iterator, count=None, assert_item_function=None):
        """Retrieve all items from iterator.

        If count is not None it should be an integer which should equal number
        of item retrieved from iterator.

        If assert_item_function is not None is should be a function
        that should be called with each item from iterator and should return
        True."""
        iterator_index = 0
        for item in iterator:
            iterator_index += 1
            if assert_item_function is not None:
                self.assertTrue(assert_item_function(item))
        if count is not None:
            self.assertEqual(iterator_index, count)

def main(**kwargs):
    """Wrapper around unittest.main()"""
    return unittest.main(**kwargs)
