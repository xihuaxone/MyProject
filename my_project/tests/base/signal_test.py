import signal
import time


def signal_handler(signum, frame):
    print("got signal", signum)
    if signum == signal.SIGINT:
        print("got Ctrl+C, will do exit(1)")
        exit(1)


signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    while True:
        time.sleep(2)
