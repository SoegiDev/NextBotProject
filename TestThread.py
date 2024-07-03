from time import sleep
from threading import Event, Thread

condition = False


def do_sth():
    print("truckin' ...")


def check_sth():
    while True:
        if condition:
            print("Condition met, ending")
            break
        else:
            sleep(0.25)
            do_sth()  # Do something everytime the condition is not met

Thread(target=check_sth).start()
sleep(2)
condition = True