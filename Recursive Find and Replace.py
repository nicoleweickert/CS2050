from __future__ import print_function
import unittest

'''
Description:    Assignment 3: Recursive Find and Replace
Author:         Nicole Weickert
Python Version: 3.6.1
Help received:  
Help provided:  
'''


def findandreplace(find, replace, string, processed=""):
    """
    Replace all instances of find with replace in string.
    Recursive approach:
    If the string starts with find, return replace and findandreplace
    with the rest of the string, else return the first character of the
    string and findandreplace with the rest of the string
    """

    if find is None or replace is None or string is None:
        return string

    elif string == "":
        return processed

    else:
        length = min(len(find),len(string))

        if (string[0:max(length,1)]) == find:
            return findandreplace(find, replace, string[max(length,1):], processed + replace)

        else:
            return findandreplace(find, replace, string[1:], processed + string[0])


class TestFindAndReplace(unittest.TestCase):

    def test_all_none(self):
        self.assertEqual(findandreplace(None, None, None), None)

    def test_find_none(self):
        self.assertEqual(findandreplace(None, "a", "aabb"), "aabb")

    def test_find_empty(self):
        self.assertEqual(findandreplace("", "a", "aabb"), "aabb")

    def test_replace_none(self):
        self.assertEqual(findandreplace("a", None, "aabb"), "aabb")

    def test_string_none(self):
        self.assertEqual(findandreplace("a", "b", None), None)

    def test_simple(self):
        self.assertEqual(findandreplace("a", "b", "aabb"), "bbbb")

    def test_remove(self):
        self.assertEqual(findandreplace(" ", "", " a abb"), "aabb")

    def test_gettysburg(self):
        self.assertEqual(findandreplace("Four score", "Eighty",
            "Four score and seven years ago"), "Eighty and seven years ago")