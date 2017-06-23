from __future__ import print_function
import unittest

class LinkedList(object):
    class Node(object):
        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node

    def __init__(self, initial=None):
        '''
        LinkedList constructor
            initial:    Optional parameter.  If included, converts to tuple (if necessary)
                        and adds data to the list in the original order.
        '''
        self.front = self.back = self.current = None    #   Initialize front, back, and current pointers
        if initial != None:                             #   If data has been passed:
            if type(initial) != tuple:
                initial = (initial, )                   #       Convert to tuple if necessary
            for each in initial:
                self.push("back", str(each))            #       Add each item to the list

    def empty(self):
        return self.front == self.back == None

    def __iter__(self):
        self.current = self.front
        return self

    def __next__(self):
        if self.current:
            tmp = self.current.value
            self.current = self.current.next_node
            return tmp
        else:
            raise StopIteration()

    def __str__(self):
        '''
        Return LinkedList in a printable format
        '''
        string = ""
        for each in self:
            string += str(each) + ", "
        return string[:-2]                              #   Truncate the trailing comma and space

    def __repr__(self):
        '''
        Return class name and contents in printable format
        '''
        string = "LinkedList(("
        string += str(self)
        string += "))"
        return string

    def push(self, position, value):
        '''
        Inserts a value into a LinkedList
            position:   Determines insertion point.  Requires "front" or "back"
            value:      The value entered into the list.
        '''
        if position == "front":                         #   If insertion point is front:
            next = self.front                           #       Set next pointer to front node
        elif position == "back":                        #   If insertion point is back:
            next = None                                 #       Set next pointer to None
        else:                                           #   Otherwise, raise error
            raise ValueError("Insertion point either not specified or invalid.")
        new_node = self.Node(value, next)               #   New node with passed value and next pointer
        if self.empty():                                #   For empty lists:
            self.front = self.back = new_node           #       Set front and back pointers to reference the new node
        elif position == "front":                       #   For non-empty lists (Front insertion):
            self.front = new_node                       #       Set front pointer to reference the new node
        else:                                           #   For non-empty lists (Back insertion):
            self.back.next_node = new_node              #       Create a 'next' pointer from the last node to the new node
            self.back = new_node                        #       Move the 'back' pointer to the new node

    def pop(self, position):
        '''
        Removes the first or last node from a LinkedList
            position:   Determines which node is removed.  Requires "front" or "back"
        '''
        if self.empty():                                #   Error on empty list
            raise RuntimeError("Cannot delete from empty list.")
        pop_value = self.front.value                    #   Initialize first node as return value
        if self.front == self.back:                     #   For lists with 1 node:
            self.front = self.back = None               #       Remove node references to clear list
        elif position == 'front':                       #   For lists with 2+ nodes (front removal):
            self.front = self.front.next_node           #       Set front pointer to reference 2nd node
        elif position == 'back':                        #   For lists with 2+ nodes (back removal):
            current_node = self.front                   #       Start at first node
            previous_node = current_node                #       Track previous node
            while current_node.next_node:               #       Loop to last node
                previous_node = current_node            #           Increment previous node
                current_node = current_node.next_node   #           Increment current node
            pop_value = current_node.value              #       Set return value equal to last node's value
            self.back = previous_node                   #       Previous node becomes new end node
            self.back.next_node = None                  #       Break end node's next link
        else:                                           #   Error if missing/incorrect position variable
            raise ValueError("Removal point either not specified or invalid.")
        return pop_value

    def remove(self, value):
        '''
        Removes all instances of a given value from a list
        '''
        current = self.front                            #   Start at first node
        previous = current                              #   Track previous node
        for each in self:                               #   Check each node's value against target
            if current.value == str(value):             #   If values match:
                if current == self.front and current == self.back:
                    self.front = self.back = None       #       If front AND back node, clear list and end
                    return
                if current == self.front:               #       If front node:
                    self.front = current.next = current #           Move front pointer to next node
                if current == self.back:                #       If back node:
                    self.back = previous                #           Move back pointer to previous node
                previous.next_node = current.next_node  #       Link previous to next
                current = current.next_node             #       Increment current node
            else:                                       #   Increment previous and current
                previous = current
                current = current.next_node

    def find_middle(self):
        '''
        Returns the value of the middle node in a linked list.
        For lists with an even number of elements, returns both middle values.
        '''
        elements = ()                                   #   Initialize tuple
        for each in self:
            elements += (str(each), )                   #   Add each element to list
        mid = int(len(elements)/2)                      #   Middle node location
        if len(elements)%2 == 1:                        #   For odd-numbered lists:
            return elements[mid]                        #       Return middle value
        else:                                           #   For even-numbered lists:
            return elements[mid-1:mid+1]                #       return both middle values as tuple

''' C-level work '''
class TestEmpty(unittest.TestCase):
    def test(self):
        self.assertTrue(LinkedList().empty())

class TestPushFrontPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push("front", 1)
        linked_list.push("front", 2)
        linked_list.push("front", 3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop("back"), 1)
        self.assertEqual(linked_list.pop("back"), 2)
        self.assertEqual(linked_list.pop("back"), 3)
        self.assertTrue(linked_list.empty())

class TestPushFrontPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push("front", 1)
        linked_list.push("front", 2)
        linked_list.push("front", 3)
        self.assertEqual(linked_list.pop("front"), 3)
        self.assertEqual(linked_list.pop("front"), 2)
        self.assertEqual(linked_list.pop("front"), 1)
        self.assertTrue(linked_list.empty())

class TestPushBackPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push("back", 1)
        linked_list.push("back", 2)
        linked_list.push("back", 3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop("front"), 1)
        self.assertEqual(linked_list.pop("front"), 2)
        self.assertEqual(linked_list.pop("front"), 3)
        self.assertTrue(linked_list.empty())

class TestPushBackPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push("back", 1)
        linked_list.push("back", "foo")
        linked_list.push("back", [3, 2, 1])
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop("back"), [3, 2, 1])
        self.assertEqual(linked_list.pop("back"), "foo")
        self.assertEqual(linked_list.pop("back"), 1)
        self.assertTrue(linked_list.empty())

''' B-level work '''
class TestInitialization(unittest.TestCase):
    def test(self):
        linked_list = LinkedList(("one", 2, 3.141592))
        self.assertEqual(linked_list.pop("front"), "one")
        self.assertEqual(linked_list.pop("front"), "2")
        self.assertEqual(linked_list.pop("front"), "3.141592")

class TestStr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__str__(), '1, 2, 3')

''' A-level work '''
class TestRepr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__repr__(), 'LinkedList((1, 2, 3))')

class TestErrors(unittest.TestCase):
    def test_pop_front_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop("front"))
    def test_pop_back_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop("back"))

''' Extra Credit '''
# write test cases for and implement a delete(value) method.
# write test cases for and implement a method that finds the middle element with only a single traversal.

class TestRemove(unittest.TestCase):
    '''
    Tests remove()
    Expected behavior:
        All nodes with values matching the passed value will be deleted.
        Nodes with partially matching values (eg '42' and '142') will remain.
    '''
    def test_empty_list(self):
        linked_list = LinkedList()
        linked_list.remove(42)
        self.assertEqual(repr(linked_list), "LinkedList(())")

    def test_single_list(self):
        linked_list = LinkedList(42)
        linked_list.remove(42)
        self.assertEqual(repr(linked_list), "LinkedList(())")

    def test_short_list(self):
        linked_list = LinkedList((1, 42, 2))
        linked_list.remove(42)
        self.assertEqual(repr(linked_list), "LinkedList((1, 2))")
        self.assertEqual(linked_list.front.value, '1')
        self.assertEqual(linked_list.back.value, '2')

    def test_subset_value(self):
        linked_list = LinkedList((142, 1))
        linked_list.remove(42)
        self.assertEqual(repr(linked_list), "LinkedList((142, 1))")
        self.assertEqual(linked_list.front.value, '142')
        self.assertEqual(linked_list.back.value, '1')

    def test_long_list(self):
        linked_list = LinkedList((1, 42, 42, 2, 42, 3, 42, 4, 5, 42))
        linked_list.remove(42)
        self.assertEqual(repr(linked_list), "LinkedList((1, 2, 3, 4, 5))")
        self.assertEqual(linked_list.front.value, '1')
        self.assertEqual(linked_list.back.value, '5')

    def test_string_list(self):
        linked_list = LinkedList(("one", "forty-two", "two", "three"))
        linked_list.remove("forty-two")
        self.assertEqual(repr(linked_list), "LinkedList((one, two, three))")
        self.assertEqual(linked_list.front.value, 'one')
        self.assertEqual(linked_list.back.value, 'three')

class TestFindMiddle(unittest.TestCase):
    '''
    Expected behavior:
        Returns the value of the middle node in a linked list.
        For lists with an even number of elements, returns both values.
    '''

    def test_empty_list(self):
        linked_list = LinkedList()
        self.assertEqual(linked_list.find_middle(),())

    def test_odd_list(self):
        linked_list = LinkedList((1, 2, 3, 4, 5))
        self.assertEqual(linked_list.find_middle(),"3")

    def test_even_list(self):
        linked_list = LinkedList((1, 2, 3, 4))
        self.assertEqual(linked_list.find_middle(),('2', '3'))

    def test_string_list(self):
        linked_list = LinkedList(("one", "two", "three"))
        self.assertEqual(linked_list.find_middle(),"two")

def fact(number):
    '''"Pretend" to do recursion via a stack and iteration'''

    if number < 0: raise ValueError("Less than zero")
    if number == 0 or number == 1: return 1

    stack = LinkedList()
    while number > 1:
        stack.push("front", number)
        number -= 1

    result = 1
    while not stack.empty():
        result *= stack.pop("front")

    return result

class TestFactorial(unittest.TestCase):
    def test_less_than_zero(self):
        self.assertRaises(ValueError, lambda: fact(-1))
    def test_zero(self):
        self.assertEqual(fact(0), 1)
    def test_one(self):
        self.assertEqual(fact(1), 1)
    def test_two(self):
        self.assertEqual(fact(2), 2)
    def test_10(self):
        self.assertEqual(fact(10), 10*9*8*7*6*5*4*3*2*1)

if '__main__' == __name__:
    unittest.main()