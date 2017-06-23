from __future__ import print_function
import unittest

'''
Description:        Assignment 2:  Dictionaries
Author:             Nicole Weickert
Python Version:     3.6.1
Helped:             "samson01"
Help received from: Luke Smith
'''

class dictionary:

    def __init__(self, init=None):
        self.__limit = 10
        self.__items = [[] for _ in range(self.__limit)]
        self.__length = 0

        if init:
            for i in init:
                self.__setitem__(i[0], i[1])

    def __len__(self):
        return self.__length

    def __flattened(self):
        return [item for inner in self.__items for item in inner]

    def __iter__(self):
        return(iter(self.__flattened()))

    def __str__(self):
        return(str(self.__flattened()))

    def __finditem(self,key):
        """
        Assigns a pair to the correct array based on the key hash value and current limit.
        Returns the index array and pair if it exists ."""

        index = hash(key) % self.__limit
        for pair in self.__items[index]:
            if pair[0] == key:
                return index, pair
        return index, None

    def __setitem__(self, key, value):
        """
        Calls __finditem() to determine correct index and check for existing key.
        If the key exists, it overwrites the value.  Otherwise, it inserts the key/value pair.
        Last, it increases the length attribute and prompts a rehash check."""

        index, pair = self.__finditem(key)
        if pair:
            pair[1] = value
        else:
            self.__items[index].append([key,value])
            self.__length += 1
            if self.__length >= self.__limit * .75:
                self.__rehash(True)

    def __getitem__(self, key):
        """
        Calls __finditem() to determine correct index and check for existing key.
        If the key exists, it returns the value.  Otherwise, it raises an error. """

        _, pair = self.__finditem(key)                  # Underscore denotes a placeholder variable that won't be used
        if pair:
            return pair[1]
        raise(KeyError("Key not found."))

    def __contains__(self, key):
        ''' Implements the 'in' operator. '''
        return self.__finditem(key)[1] is not None

    def __delitem__(self, key):
        """
        Calls __finditem() to determine correct index and check for existing key.
        If the key exists, it removes the pair.  Otherwise, it raises an error.
        Last, it decreases the length attribute and prompts a rehash check. """

        index, pair = self.__finditem(key)
        if not pair:
            raise KeyError("Key not found.")
        self.__items[index].remove(pair)
        self.__length -= 1
        if self.__length <= self.__limit * .25:
            self.__rehash(False)

    def __rehash(self, increase):
        """
        Doubles or halves the limit attribute based on the passed increase boolean.
        Saves a temporary copy of the dictionary and empties the target dictionary.
        Reinserts each pair from the copy back into the dictionary with the new hash limit """

        if increase:
            self.__limit *= 2
        else:
            self.__limit = int(self.__limit / 2)

        flat_list = self.__flattened()
        self.__items = [[] for _ in range(self.__limit)]
        self.__length = 0

        for key,value in flat_list:
            self.__setitem__(key, value)

    def keys(self):
        '''  Returns all keys. '''
        return [item[0] for inner in self.__items for item in inner]

    def values(self):
        '''  Returns all values. '''
        return [item[1] for inner in self.__items for item in inner]

    def items(self):
        '''  Returns all key/value pairs as tuples. '''
        return [(item[0], item[1]) for inner in self.__items for item in inner]

    def __eq__(self, other):
        """
        Compares equality between two dictionaries.
        Dictionaries are considered equal if:
            they have idential lengths
            each key from dictionary 1 matches a key from dictionary 2
            and each matching key contains matching values.  """

        if len(self) != len(other):
            return False
        for each in self.__items:
            for key, value in each:
                if not other.__contains__(key):
                    return False
                else:
                    if value != other[key]:
                        return False
        return True

''' C-level work
'''
class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], "one")
        self.assertEqual(s[2], "two")

class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[1] = "one"
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], "one")

class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertTrue(1 in s)
        self.assertFalse(s[1])

class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)

class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)

class test_False_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)

class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)

''' B-level work
    Add doubling and rehashing when load goes over 75%
    Add __delitem__(self, key)
'''
class test_rehash_high(unittest.TestCase):
    def test(self):
        s = dictionary([(i,i) for i in range(10)])
        self.assertEqual(s._dictionary__limit, 20)

class test_delitem(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        self.assertTrue(1 in s)
        self.assertEqual(s._dictionary__limit, 10)
        del s[1]
        self.assertFalse(1 in s)
        self.assertEqual(s._dictionary__limit, 5)

''' A-level work
    Add halving and rehashing when load goes below 25%
    Add keys()
    Add values()
'''
class test_rehash_low(unittest.TestCase):
    def test(self):
        s = dictionary([(i,i) for i in range(3)])
        del s[0]
        self.assertEqual(s._dictionary__limit, 5)
        self.assertEqual(len(s),2)

class test_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        self.assertEqual(s.keys(),[1,2,3])

class test_values(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        print(s.values())
        self.assertEqual(s.values(), ["one", "two", "three"])

''' Extra credit
    Add __eq__()
    Add items(), "a list of D's (key, value) pairs, as 2-tuples"
'''
class test_items(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        self.assertEqual(s.items(), [(1,"one"),(2,"two"),(3,"three")])

class test_eq(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"

        t = dictionary()
        t[2] = "two"
        t[1] = "one"
        t[3] = "three"

        u = dictionary()
        u["one"] = 1
        u["two"] = 2
        u["three"] = 3

        self.assertTrue(s.__eq__(t))
        self.assertFalse(s.__eq__(u))

if '__main__' == __name__:
    unittest.main()