#!/usr/bin/env python3.4

import functools


class SumInfo:
    def __init__(self, digits):
        self.digits = digits
        self.base = len(digits)


@functools.total_ordering
class CrossSum:
    def __init__(self, cross_sum, sum_info):
        self._cross_sum = cross_sum
        self._digits = sum_info.digits
        self._base = sum_info.base

    def convert(self):
        total, addends = self._cross_sum

        total_digits = []
        while total:
            total_digits.append(self._digits[total % self._base])
            total //= self._base

        return ''.join(total_digits[::-1]), addends

    def __eq__(self, other):
        return (
            self._cross_sum == other._cross_sum
        )

    def __lt__(self, other):
        return (
            self._cross_sum < other._cross_sum
        )

    def __repr__(self):
        return self.convert()

    def __str__(self):
        total_str, addends = self.convert()

        return '%s = %s' % (total_str, ' + '.join(addends))

    def __iter__(self):
        return self._cross_sum.__iter__()

    def __len__(self):
        return len(self._cross_sum[1])


class CrossSums:
    def __init__(self, digits='0123456789', cross_sums=None):
        self._sum_info = SumInfo(digits)
        self._digits = self._sum_info.digits
        self._base = self._sum_info.base
        self._cross_sums = cross_sums

        if cross_sums is None:
            cross_sums = [
                CrossSum((0, ''), self._sum_info),
                CrossSum((1, self._digits[1]), self._sum_info)
            ]
            for d, digit in enumerate(self._digits[2:], 2):
                cross_sums += [
                    CrossSum((total + d, addends + digit), self._sum_info)
                    for total, addends in cross_sums
                ]

            cross_sums = cross_sums[1:]
            for cross_sum in cross_sums:
                if len(cross_sum) == 1:
                    cross_sums.remove(cross_sum)

        self._cross_sums = sorted(cross_sums)

    def filter(self, total=None, addends=None, digits=None):
        cross_sums = self._cross_sums

        if total:
            if isinstance(total, str):
                total_digits = total
                total = 0
                for d in total_digits:
                    total = total * self._base + self._digits.index(d)

            cross_sums = [s for s in cross_sums if s._cross_sum[0] == total]

        if addends:
            cross_sums = [
                s for s in cross_sums if len(s._cross_sum[1]) == addends
            ]

        if digits:
            digits = set(digits)
            cross_sums = [
                s for s in cross_sums
                if set(s._cross_sum[1]).issuperset(digits)
            ]

        return CrossSums(self._digits, cross_sums=cross_sums)

    @property
    def max_sum(self):
        return self._cross_sums[-1][0]

    def __iter__(self):
        return self._cross_sums.__iter__()

    def __len__(self):
        return len(self._cross_sums)


if __name__ == '__main__':
    doz_sums = CrossSums('0123456789XE')

    print('Sums totalling 15:')

    for ds in doz_sums.filter(total='15'):
        print('  ', ds)

    print('\nSums containing digits 3-X inclusive:')

    for ds in doz_sums.filter(digits='3456789X'):
        print('  ', ds)

    print('\nSums containing ten addends:')

    for ds in doz_sums.filter(addends=10):
        print('  ', ds)

    print('\nSums totaling 1X with five addends including 2 and 3:')
    for ds in doz_sums.filter(total='1X', addends=5, digits='23'):
        print('  ', ds)
