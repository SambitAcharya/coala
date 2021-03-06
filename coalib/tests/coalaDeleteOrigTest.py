import os
import unittest

from coalib import coala_delete_orig
from coalib.misc.ContextManagers import retrieve_stdout
from coalib.parsing import Globbing
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def raise_assertion_error(*args, **kwargs):
    raise AssertionError


class coalaDeleteOrigTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("default")
        self.section.append(Setting("config", '/path/to/file'))

    def test_nonexistent_coafile(self):
        old_getcwd = os.getcwd
        os.getcwd = lambda *args: None
        with retrieve_stdout() as stdout:
            retval = coala_delete_orig.main()
            self.assertIn("Can only delete .orig files if ", stdout.getvalue())
            self.assertEqual(retval, 255)
        os.getcwd = old_getcwd

    def test_remove_exception(self):
        old_remove = os.remove
        old_glob = Globbing.glob
        Globbing.glob = lambda *args: ["file1", "file2"]
        os.remove = raise_assertion_error
        with retrieve_stdout() as stdout:
            retval = coala_delete_orig.main(section=self.section)
            output = stdout.getvalue()
            self.assertEqual(retval, 0)
            self.assertIn("Couldn't delete... file1", output)
            self.assertIn("Couldn't delete... file2", output)
        os.remove = old_remove
        Globbing.glob = old_glob
