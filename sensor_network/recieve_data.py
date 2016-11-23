import sys
import time

def main_loop():
    a = 1
    print("insert receive data file here")


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)