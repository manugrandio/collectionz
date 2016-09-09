import unittest
from unittest.mock import Mock
from collections import namedtuple, defaultdict
from datetime import date

from collectionz import GroupBy


Order = namedtuple('Order', 'date, email, product')
orders = [
    Order(date(2013, 3, 4), 'carl@mail.com', 'Computer'),
    Order(date(2014, 2, 20), 'mary@mail.com', 'Lamp'),
    Order(date(2016, 7, 1), 'eggs@mail.com', 'Desk'),
    Order(date(2016, 2, 12), 'mary@mail.com', 'TV'),
]


class TestGroupBy(unittest.TestCase):
    def test_groupby_init(self):
        def add_to_group(group, obj):
            return {
                True: orders[1:],
                False: [orders[0]],
            }
        GroupBy._build_add_to_group = Mock(return_value=add_to_group)
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(grouped._group[False]._group[0], orders[0])

    def test_build_add_to_group(self):
        group_by_mock = Mock()
        add_to_group = GroupBy._build_add_to_group(
            group_by_mock, lambda o: o.date.year > 2013)
        groups = add_to_group(defaultdict(list), orders[0])
        self.assertIn(orders[0], groups[False])

    def test_build_add_to_group_not_hashable(self):
        def a_grouper(o):
            return {}
        with self.assertRaises(Exception) as manager:
            group_by_mock = Mock()
            add_to_group = GroupBy._build_add_to_group(
                group_by_mock, a_grouper)
            add_to_group(defaultdict(list), orders[0])
        msg = 'Value returned by function "a_grouper" is not hashable'
        self.assertEqual(str(manager.exception), msg)

    def test_get_item(self):
        def add_to_group(group, obj):
            return {
                True: orders[1:],
                False: [orders[0]],
            }
        GroupBy._build_add_to_group = Mock(return_value=add_to_group)
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(grouped[False][0], orders[0])

    def test_iter(self):
        def add_to_group(group, obj):
            return {
                True: orders[1:],
                False: [orders[0]],
            }
        GroupBy._build_add_to_group = Mock(return_value=add_to_group)
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(sorted(list(grouped)), [False, True])

    def test_add_object(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        order = Order(date(2012, 9, 1), 'kate@mail.com', 'Toy')
        grouped.add(order)
        self.assertEqual(grouped[False][1], order)

    def test_len(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(len(grouped), len(orders))

    def test_eq(self):
        grouped1 = GroupBy(orders, [lambda o: o.date.year > 2013])
        grouped2 = GroupBy(orders[1:] + [orders[0]], [lambda o: o.date.year > 2013])
        self.assertEqual(grouped1, grouped2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
