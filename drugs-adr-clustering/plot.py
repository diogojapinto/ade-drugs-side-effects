import re
import matplotlib.pyplot as plt

def main():
    x = []
    y = []
    for line in open("data/svd_ref.log"):

        m = re.match(r'Iteration ([\d]+): \t([\d\.]+)', line)

        if m:
            x.append(int(m.group(1)))
            y.append(float(m.group(2)))

    plt.plot(x, y)
    plt.savefig("learning1.png")

    plt.plot(x, y)
    plt.axis([0, 2000, 0, 4000000])
    plt.savefig("learning2.png")

    plt.plot(x[29:], y[29:])
    plt.axis([0, 500, 0, 4000000])
    plt.savefig("learning3.png")


if __name__ == '__main__':
    main()