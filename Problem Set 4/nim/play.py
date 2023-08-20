from nim import train, play
import sys


def main():
    if len(sys.argv) not in [1,2]:
        sys.exit('Usage python play.py [training games n=10000]')
    elif len(sys.argv) == 2:
        try:
            n = int(sys.argv[1])
        except ValueError:
            sys.exit('Value must be a int')
    else:
        n = 10000
    ai = train(n)
    play(ai)

if __name__ == '__main__':
    main()
