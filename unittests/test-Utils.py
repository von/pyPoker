#!/usr/bin/env python
"""Unittests for Utils module"""

import StringIO

import testing

from pyPoker.Utils import UserSelection

class TestSequenceFunctions(testing.TestCase):

    def test_UserSelection(self):
        """Test basic UserSelction functionality"""
        with self.pipe_to_stdin() as input:
            with self.stdout_to_pipe() as output:
                user_selection = UserSelection()
                self.assertIsNotNone(user_selection)
                user_selection.add_option('p',
                                          description="Play",
                                          return_value=0)
                user_selection.add_option('q',
                                          description="Quit",
                                          return_value=1)
                user_selection.add_option('r',
                                          description="Reset",
                                          return_value=2)
                input.write("pyrq")
                # 'p' should return 0
                self.assertEqual(user_selection.get_user_selection(), 0)
                # 'y' should be ignored, 'r' should return 2
                self.assertEqual(user_selection.get_user_selection(), 2)
                # 'q' should return 1
                self.assertEqual(user_selection.get_user_selection(), 1)
        lines = output.readlines()
        # (Three options plus prompt) times 3 calls to get_user_selection()
        # meands we should have 12 lines in output buffer.
        self.assertEqual(len(lines), 12)

    def test_UserSelection_with_streams(self):
        """Test basic UserSelction with specified streams"""
        input_buffer = StringIO.StringIO("pyrq")
        output_buffer = StringIO.StringIO()
        user_selection = UserSelection(input_stream=input_buffer,
                                       output_stream=output_buffer)
        self.assertIsNotNone(user_selection)
        user_selection.add_option('p', description="Play", return_value=0)
        user_selection.add_option('q', description="Quit", return_value=1)
        user_selection.add_option('r', description="Reset", return_value=2)
        # 'p' should return 0
        self.assertEqual(user_selection.get_user_selection(), 0)
        output_buffer.seek(0)
        lines = output_buffer.readlines()
        self.assertEqual(len(lines), 4)  # 3 options plus prompt
        # 'y' should be ignored, 'r' should return 2
        self.assertEqual(user_selection.get_user_selection(), 2)
        # 'q' should return 1
        self.assertEqual(user_selection.get_user_selection(), 1)
        
if __name__ == "__main__":
    testing.main()
