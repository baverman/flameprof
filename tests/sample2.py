import time


def f1(n):
    time.sleep(0.1)
    if n:
        f2(n-1)


def f2(n):
    time.sleep(0.1)
    if n:
        f1(n-1)


def main():
    f1(10)


if __name__ == '__main__':
    main()
