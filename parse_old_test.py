import unittest
from parse_old import get_objects__old_format

class ParseOldTests(unittest.TestCase):
    def test_parse_lore(self):
        item_str ="""Object: 'a large bowl of shark fin soup, bursting with carrots and potatoes' is type food.
Weight is 0.5, value is 82, level is 10
Material is food
//lore, not identify. not like it matters with this one."""
        objects = list(get_objects__old_format(item_str))
        self.assertEqual(len(objects), 1)
        item = objects[0].item
        self.assertEqual(item['material'], 'food')
        self.assertEqual(item['level'], '10')
        self.assertEqual(item['weight'], '0.5')



