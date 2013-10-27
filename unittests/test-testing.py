#!/usr/bin/env python
"""Unittests for testing.py"""

import sys

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

    def test_stdout_to_pipe(self):
        """Test the stdout_to_pipe() context manager"""
        original_stdout = sys.stdout
        with self.stdout_to_pipe() as output:
            self.assertNotEqual(original_stdout, sys.stdout)
            print "Hello world!"
            self.assertEqual(output.readline(), "Hello world!\n")
            # Line without CR should be readable after closing
            sys.stdout.write("Goodbye")
        self.assertEqual(original_stdout, sys.stdout)
        # Now that writing side is closed, we should be able to read
        # up to EOF.
        self.assertEqual(output.readline(), "Goodbye")

    def test_pipe_to_stdin(self):
        """Test the pipe_to_stdin() context manager"""
        original_stdin = sys.stdin
        with self.pipe_to_stdin() as input:
            self.assertNotEqual(original_stdin, sys.stdin)
            input.write("Hello world!\n")
            self.assertEqual(sys.stdin.readline(), "Hello world!\n")
        self.assertEqual(original_stdin, sys.stdin)
        
if __name__ == "__main__":
    testing.main()
