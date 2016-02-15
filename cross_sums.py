#!/usr/bin/env python3.4

class Sums:
    def __init__(self, base=10, sums=None):
        self._base = base

        if sums is None:
            sums = [(0, set()), (1, {1})]
            for d in range(2, base):
                sums += [(total + d, digits | {d}) for total, digits in sums]

            sums = sums[1:]
            for d in range(1, base):
                sums.remove((d, {d}))

        self._sums = sorted(sums)

    def convert(self, s):
        return s[0], tuple(sorted(s[1]))

    def with_total(self, total):
        return Sums(self._base, [s for s in self._sums if s[0] == total])

    def with_digits(self, digits):
        return Sums(self._base, [s for s in self._sums
                                     if s[1].issuperset(digits)])

    def with_addends(self, addends):
        return Sums(self._base, [s for s in self._sums
                                     if len(s[1]) == addends])

    def __iter__(self):
        return self._sums.__iter__()

    def __len__(self):
        return len(self._sums)


if __name__ == '__main__':
    sums = Sums(12)

    print('Sums with total of 15:')

    for s in sums.with_total(15):
        print('  ', sums.convert(s))

    print('\nSums containing digits 2-9 inclusive:')

    for s in sums.with_digits(range(2, 10)):
        print('  ', sums.convert(s))

    print('\nSums containing 10 addends:')

    for s in sums.with_addends(10):
        print('  ', sums.convert(s))

    print('\nSums totaling 20 with 5 addends including 2 and 3:')
    for s in sums.with_total(20).with_digits({2,3}).with_addends(5):
        print('  ', sums.convert(s))
