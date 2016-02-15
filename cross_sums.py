#!/usr/bin/env python3.4

import functools


@functools.total_ordering
class CrossSum:
    def __init__(self, total, addends, digits):
        self.total = total
        self.addends = addends
        self._digits = digits
        self._base = len(digits)

    def convert_total(self):
        num_total = self.total

        total_digits = []
        while num_total:
            total_digits.append(self._digits[num_total % self._base])
            num_total //= self._base

        return ''.join(total_digits[::-1])

    @property
    def num_addends(self):
        return len(self.addends)

    def _is_valid_operand(self, other):
        return (hasattr(other, 'total') and hasattr(other, 'addends'))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return (
            (self.total, self.addends) == (other.total, other.addends)
        )

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return (
            (self.total, self.addends) < (other.total, other.addends)
        )

    def __repr__(self):
        return (
            "<CrossSum(total='%s', addends='%s', digits='%s')>"
            % (self.convert_total(), self.addends, self._digits)
        )

    def __str__(self):
        total_str = self.convert_total()

        return '%s = %s' % (total_str, ' + '.join(self.addends))


class CrossSums:
    def __init__(self, digits='0123456789', cross_sums=None):
        self._digits = digits
        self._base = len(digits)
        self._cross_sums = cross_sums

        if cross_sums is None:
            cross_sums = [
                CrossSum(0, '', self._digits),
                CrossSum(1, self._digits[1], self._digits)
            ]
            for d, digit in enumerate(self._digits[2:], 2):
                cross_sums += [
                    CrossSum(cs.total + d, cs.addends + digit, self._digits)
                    for cs in cross_sums
                ]

            cross_sums = cross_sums[1:]
            for cross_sum in cross_sums:
                if cross_sum.num_addends == 1:
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

            cross_sums = [
                s for s in cross_sums if s.total == total
            ]

        if addends:
            cross_sums = [
                s for s in cross_sums if len(s.addends) == addends
            ]

        if digits:
            digits = set(digits)
            cross_sums = [
                s for s in cross_sums
                if set(s.addends).issuperset(digits)
            ]

        return CrossSums(self._digits, cross_sums=cross_sums)

    @property
    def max_sum(self):
        return self._cross_sums[-1].total

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
