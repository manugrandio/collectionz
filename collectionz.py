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
