import sched
import time

s = sched.scheduler(time.time, time.sleep)

def main(sc):
    # Do something
    print("driver.title")

    # Intervals for function in sec
    sc.enter(10, 1, main, (sc,))


if __name__ == '__main__':
    # Initial sched starter
    s.enter(1, 1, main, (s,))
    s.run()
