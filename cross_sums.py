#!/usr/bin/env python3.4

class Sums:
    def __init__(self, base=10, sums=None):
        self._base = base

        if not sums:
            sums = [0, self._digit(1)]
            for d in range(2, base):
                sums.extend([sum + self._digit(d) for sum in sums])

            sums = sums[1:]
            for d in range(1, base):
                sums.remove(self._digit(d))

        self._sums = sorted(sums)

    def _digit(self, d):
        return (d << (self._base-1)) + (1 << (d-1))

    def convert(self, total):
        return (total >> (self._base-1),
                tuple(d for d in range(1, self._base)
                          if total & (1 << (d-1))))

    def with_total(self, total):
        return Sums(self._base, [s for s in self._sums
                                     if s >> (self._base-1) == total])

    def with_digits(self, digits):
        if not isinstance(digits, int):
            digits = sum((1 << (d-1)) for d in range(1, self._base)
                             if d in digits)

        return Sums(self._base, [s for s in self._sums
                                     if s & digits == digits])

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
