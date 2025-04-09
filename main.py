import threading
import time
import random

NUM_TELLERS = 3
NUM_CUSTOMERS = 5  # Start small for initial testing

def teller_thread(tid):
    print(f"Teller {tid} [Teller {tid}]: is ready to serve")

def customer_thread(cid):
    print(f"Customer {cid} [Customer {cid}]: has entered the bank")

def main():
    tellers = []
    customers = []

    # Start teller threads
    for i in range(NUM_TELLERS):
        t = threading.Thread(target=teller_thread, args=(i,))
        tellers.append(t)
        t.start()

    # Start customer threads
    for i in range(NUM_CUSTOMERS):
        t = threading.Thread(target=customer_thread, args=(i,))
        customers.append(t)
        t.start()

    # Wait for all threads to finish
    for t in tellers + customers:
        t.join()

    print("Simulation complete.")

if __name__ == "__main__":
    main()

