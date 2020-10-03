import unittest
from parse_new import get_objects__new_format

class ParseNewTests(unittest.TestCase):
    def test_object_with_quotes(self):
        item_str ="""
+-----------------------------------------------------------------------+
| Object:   a glass of a spicy, amber ale known as "B.B.'s Brutal Brew" |
| Flags:    none                                                        |
| Weight:   0.5                                                         |
| Wear:     none                                                        |
| Level:    20                                                          |
| Material: glass                                                       |
| --------------------------------------------------------------------- |
| Type:         drink                                                   |
| Color:        brown                                                   |
| Liquid:       ale                                                     |
+-----------------------------------------------------------------------+
"""
        objects = list(get_objects__new_format(item_str))
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].item['name'], '''a glass of a spicy, amber ale known as "B.B.'s Brutal Brew"''')

    def test_with_trailing_space(self):
        item_str = """
 +-------------------------------------------------------+
 | Object:   a ball of flame                             |
 | Flags:    glow warm evil anti-good nonmetal nodestroy |
 | Weight:   0.5                                         |
 | Wear:     float                                       |
 | Level:    55                                          |
 | Material: fire                                        |
 | ----------------------------------------------------- |
 | Type:         armor                                   |
 | AC vs pierce: 2                                       |
 | AC vs bash:   2                                       |
 | AC vs slash:  2                                       |
 | AC vs magic:  20                                      |
 | ----------------------------------------------------- |
 | Affects hp by 25                                      |
 | Affects damage roll by 2                              |
 +-------------------------------------------------------+
//Kzaya Ha Canyon, charred nefortu (5-ish% chance to drop)
//casts flamestrike during combat
"""
        objects = list(get_objects__new_format(item_str))
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].item['name'], 'a ball of flame')
