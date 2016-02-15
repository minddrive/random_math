#!/usr/bin/env python3.4

import functools


@functools.total_ordering
class CrossSum:
    def __init__(self, digits, total=0, addends=''):
        self._digits = digits
        self._base = len(digits)
        self.total = total
        self.addends = addends

    def _convert_total(self):
        num_total = self.total

        total_digits = []
        while num_total:
            total_digits.append(self._digits[num_total % self._base])
            num_total //= self._base

        return ''.join(total_digits[::-1])

    # This assumes that the new addend is larger than others in the sum
    def add_addend(self, addend):
        d = self._digits.index(addend)
        return CrossSum(self._digits, self.total + d, self.addends + addend)

    def has_total(self, total):
        if isinstance(total, str):
            total_str = total
            total = 0
            for digit in total_str:
                total = total * self._base + self._digits.index(digit)

        return self.total == total

    def has_addends(self, addends):
        if not isinstance(addends, set):
            addends = set(addends)

        return set(self.addends).issuperset(addends)

    @property
    def num_addends(self):
        return len(self.addends)

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, 'total') and hasattr(other, 'addends')

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return (self.total, self.addends) == (other.total, other.addends)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        return (self.total, self.addends) < (other.total, other.addends)

    def __repr__(self):
        return ("<CrossSum(digits='%s', total='%s', addends='%s'>"
                % (self._digits, self._convert_total(), self.addends))

    def __str__(self):
        total_str = self._convert_total()

        return '%s = %s' % (total_str, ' + '.join(self.addends))


class CrossSums:
    def __init__(self, digits='0123456789', cross_sums=None):
        self._digits = digits
        self._base = len(digits)

        if cross_sums is None:
            cross_sums = [CrossSum(digits)]

            for digit in digits[1:]:
                cross_sums += [cs.add_addend(digit) for cs in cross_sums]

            cross_sums = [cs for cs in cross_sums if cs.num_addends > 1]

        self._cross_sums = sorted(cross_sums)

    def filter(self, total=None, num_addends=None, addends=None):
        cross_sums = self._cross_sums

        if total:
            cross_sums = [cs for cs in cross_sums if cs.has_total(total)]

        if num_addends:
            cross_sums = [cs for cs in cross_sums
                          if cs.num_addends == num_addends]

        if addends:
            addends = set(addends)
            cross_sums = [cs for cs in cross_sums if cs.has_addends(addends)]

        return CrossSums(self._digits, cross_sums)

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

    print('\nSums containing addends 3-X inclusive:')

    for ds in doz_sums.filter(addends='3456789X'):
        print('  ', ds)

    print('\nSums containing ten addends:')

    for ds in doz_sums.filter(num_addends=10):
        print('  ', ds)

    print('\nSums totaling 1X with five addends including 2 and 3:')
    for ds in doz_sums.filter(total='1X', num_addends=5, addends='23'):
        print('  ', ds)
