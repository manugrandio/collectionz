"""
A set of utility classes.
"""

from functools import reduce
from collections import defaultdict
from collections.abc import Hashable


class GroupBy:
    """
    Create objects hierarchy by grouping by a list of functions/groupers.
    Objects are grouped by first grouper and then, within each group, by
    the rest of groupers.

    >>> from datetime import date
    >>> from collections import namedtuple
    >>> Order = namedtuple('Order', 'date, email, product')
    >>> orders = [
    ...     Order(date(2013, 3, 4), 'carl@mail.com', 'Computer'),
    ...     Order(date(2014, 2, 20), 'mary@mail.com', 'Lamp'),
    ...     Order(date(2016, 7, 1), 'eggs@mail.com', 'Desk'),
    ...     Order(date(2016, 2, 12), 'mary@mail.com', 'TV'),
    ... ]
    >>> groupers = [lambda o: o.date.year > 2013, lambda o: o.email]
    >>> GroupBy(orders, groupers)
    ... {
    ...     False: {
    ...         'carl@mail.com': [
    ...             Order(
    ...                 date=datetime.date(2013, 3, 4),
    ...                 email='carl@mail.com',
    ...                 product='Computer')
    ...         ]
    ...     },
    ...     True: {
    ...         'mary@mail.com': [
    ...             Order(
    ...                 date=datetime.date(2014, 2, 20),
    ...                 email='mary@mail.com',
    ...                 product='Lamp'),
    ...             Order(
    ...                 date=datetime.date(2016, 2, 12),
    ...                 email='mary@mail.com',
    ...                 product='TV')
    ...         ],
    ...         'eggs@mail.com': [
    ...             Order(
    ...                 date=datetime.date(2016, 7, 1),
    ...                 email='eggs@mail.com',
    ...                 product='Desk')
    ...         ]
    ...     }
    ... }
    """

    def __init__(self, objects, groupers):
        self._groupers = groupers
        if not self._groupers:
            self._group = objects
        else:
            add_to_group = self._build_add_to_group(self._groupers[0])
            grouped = reduce(add_to_group, objects, defaultdict(list))
            self._group = {
                bucket: GroupBy(objs, self._groupers[1:])
                for bucket, objs in grouped.items()}

    def _build_add_to_group(self, grouper):
        """
        Build function that will add 'obj' to a 'group' by using 'grouper'.
        """
        def add_to_group(group, obj):
            bucket = grouper(obj)
            if not isinstance(bucket, Hashable):
                error_tpl = 'Value returned by function "{}" is not hashable'
                raise Exception(error_tpl.format(grouper.__name__))
            group[bucket].append(obj)
            return group
        return add_to_group

    def process(self, processor):
        """
        Process every 'leaf' (list of objects that have been grouped)
        with 'processor' in-place.
        """
        if type(self._group) is list:
            self._group = processor(self._group)
        else:
            for bucket in self._group:
                self._group[bucket].process(processor)

    def process_with(self, processor, *buckets):
        """
        Apply 'processor' to each group and return a list with the results.
        'processor' receives a group as a first argument and the rest of
        arguments are the "buckets" where groups are placed.
        """
        if type(self._group) is list:
            return [processor(self._group, *buckets)]
        else:
            return reduce(lambda a, b: a + b, [
                self[bucket].process_with(processor, *(buckets + (bucket,)))
                for bucket in self])

    def add(self, obj):
        """
        Add 'obj' to group by taking into account its groupers.
        """
        self._add(obj, self._groupers)

    def _add(self, obj, groupers):
        if not groupers:
            self._group.append(obj)
        else:
            bucket = groupers[0](obj)
            self._group[bucket]._add(obj, groupers[1:])

    def add_grouper(self, grouper):
        """
        Create new sub-groups in each existing group with 'grouper'.
        """
        if type(self._group) is list:
            self._group = GroupBy(self._group, [grouper])
        else:
            for bucket in self:
                self[bucket].add_grouper(grouper)

    def __getitem__(self, bucket):
        return self._group[bucket]

    def __iter__(self):
        return self._group.__iter__()

    def __len__(self):
        """
        Get total number of items in the GroupBy object.
        """
        if type(self._group) is list:
            return len(self._group)
        else:
            return sum(map(len, self._group.values()))

    def __eq__(self, obj):
        return self._group == obj

    def __repr__(self):
        return repr(self._group)

    __str__ = __repr__


class CounterBy(GroupBy):
    """
    Like 'collections.Counter', but items are counted by applying them the
    'by' function.

    >>> CounterBy(range(10), lambda item: item < 5)
    ... {False: 5, True: 5}
    """
    def __init__(self, items, by):
        super(CounterBy, self).__init__(items, [by])
        self.process(len)
