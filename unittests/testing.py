"""Wrapper around unittest.TestCase adding functionality"""

import contextlib
import os
import sys
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

    @contextlib.contextmanager
    def stdout_to_pipe(self):
        """Context manager for creating a pipe that receives anything
        sent to stdout.

        >>> with self.stdout_to_pipe() as output:
        ...     print "Hello world!"
        ...     self.assertEqual(output.readline(), "Hello world!\n")

        output is a file object and is not closed so that calling context
        can read any data out of it after with block closes.
        """
        saved_stdout = sys.stdout
        read_fd, write_fd = os.pipe()
        reader = os.fdopen(read_fd)
        writer = os.fdopen(write_fd, "w", 0)  # 0 == unbuffered
        sys.stdout = writer
        try:
            yield reader
        finally:
            sys.stdout = saved_stdout
            writer.close()
            # Leave reader for calling context to close so they can read
            # any data off of it first.

    @contextlib.contextmanager
    def pipe_to_stdin(self):
        """Context manager for creating a pipe that sends anything it
        receives to stdin.

        >>> with self.pipe_to_stdin() as input:
        ...     input.write("Hello world!\n")
        ...     self.assertEqual(sys.stdin.readline(), "Hello world!\n")
        """
        saved_stdin = sys.stdin
        read_fd, write_fd = os.pipe()
        reader = os.fdopen(read_fd)
        writer = os.fdopen(write_fd, "w", 0)  # 0 == unbuffered
        sys.stdin = reader
        try:
            yield writer
        finally:
            sys.stdin = saved_stdin
            reader.close()
            writer.close()

def main(**kwargs):
    """Wrapper around unittest.main()"""
    return unittest.main(**kwargs)
