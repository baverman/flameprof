import time


def f1(count):
    time.sleep(0.001)
    for r in range(count):
        pass


def f2():
    time.sleep(0.005)
    f1(100000)
    for r in range(100000):
        pass


def f3():
    time.sleep(0.007)
    f2()
    f1(200000)
    for r in range(100000):
        pass


def main():
    for r in range(100):
        f3()


if __name__ == '__main__':
    main()
