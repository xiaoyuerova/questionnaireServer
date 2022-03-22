class A:
    aA = 1

    def __init__(self, a):
        self.aA = a + 1
        print('aA', self.aA)

    def add(self, x):
        y = x + 1
        print(y)


class B(A):
    def add(self, x):
        x = x + 2
        print('b:', x)
        # super().add(x)

    def __init__(self, a):
        a = a + 1
        print('aB', a)
        if a < 0:
            super().__init__(a)
            print(self.aA)


def add(nums):
    if len(nums) > 2:
        return 0, sum(nums)
    else:
        return 1


def main():
    a = True
    b = False
    c = True
    d = False
    if a == b:
        print('a,ok')
    if b == d:
        print('b,ok')


if __name__ == "__main__":
    main()
