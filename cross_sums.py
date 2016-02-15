#!/usr/bin/env python3.4


class Sums:
    def __init__(self, digits='0123456789', sums=None):
        self._digits = digits
        self._base = len(digits)

        if sums is None:
            sums = [(0, ''), (1, digits[1])]
            for d, digit in enumerate(digits[2:], 2):
                sums += [
                    (total + d, addends + digit) for total, addends in sums
                ]

            sums = sums[1:]
            for d, digit in enumerate(digits[1:], 1):
                sums.remove((d, digit))

        self._sums = sorted(sums)

    def filter(self, total=None, addends=None, digits=None):
        sums = self._sums

        if total:
            if isinstance(total, str):
                total_digits = total
                total = 0
                for d in total_digits:
                    total = total * self._base + self._digits.index(d)

            sums = [s for s in sums if s[0] == total]

        if addends:
            sums = [s for s in sums if len(s[1]) == addends]

        if digits:
            digits = set(digits)
            sums = [s for s in sums if set(s[1]).issuperset(digits)]

        return Sums(self._digits, sums=sums)

    def convert(self, s):
        total, addends = s

        total_digits = []
        while total:
            total_digits.append(self._digits[total % self._base])
            total //= self._base

        return ''.join(total_digits[::-1]), addends

    @property
    def max_sum(self):
        return self._sums[-1][0]

    def __iter__(self):
        return self._sums.__iter__()

    def __len__(self):
        return len(self._sums)


if __name__ == '__main__':
    doz_sums = Sums('0123456789XE')

    print('Sums totalling 15:')

    for ds in doz_sums.filter(total='15'):
        print('  ', doz_sums.convert(ds))

    print('\nSums containing digits 3-X inclusive:')

    for ds in doz_sums.filter(digits='3456789X'):
        print('  ', doz_sums.convert(ds))

    print('\nSums containing ten addends:')

    for ds in doz_sums.filter(addends=10):
        print('  ', doz_sums.convert(ds))

    print('\nSums totaling 1X with five addends including 2 and 3:')
    for ds in doz_sums.filter(total='1X', addends=5, digits='23'):
        print('  ', doz_sums.convert(ds))
