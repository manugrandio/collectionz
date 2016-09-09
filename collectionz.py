from functools import reduce
from collections import defaultdict
from collections.abc import Hashable


class GroupBy:
    def __init__(self, objects, groupers):
        self._groupers = groupers
        if not self._groupers:
            self._group = objects
        else:
            add_to_group = self._build_add_to_group(groupers[0])
            grouped = reduce(add_to_group, objects, defaultdict(list))
            self._group = {
                bucket: GroupBy(grouped[bucket], self._groupers[1:])
                for bucket in grouped}

    def _build_add_to_group(self, grouper):
        def add_to_group(group, obj):
            bucket = grouper(obj)
            if not isinstance(bucket, Hashable):
                error_tpl = 'Value returned by function "%s" is not hashable'
                raise Exception(error_tpl % grouper.__name__)
            group[bucket].append(obj)
            return group
        return add_to_group

    def __getitem__(self, bucket):
        return self._group[bucket]

    def __iter__(self):
        return self._group.__iter__()

    def add(self, obj):
        self._add(obj, self._groupers)

    def _add(self, obj, groupers):
        if not groupers:
            self._group.append(obj)
        else:
            bucket = groupers[0](obj)
            self._group[bucket]._add(obj, groupers[1:])

    def __len__(self):
        if type(self._group) is list:
            return len(self._group)
        else:
            return sum(map(len, self._group.values()))

    def __eq__(self, obj):
        return self._group == obj
