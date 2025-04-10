import threading
import time
import random

NUM_TELLERS = 3
NUM_CUSTOMERS = 5  # Start small

bank_open = threading.Event()
door_semaphore = threading.Semaphore(2)

teller_ready = []
teller_ready_lock = threading.Lock()

class Teller(threading.Thread):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid

    def run(self):
        print(f"Teller {self.tid} [Teller {self.tid}]: is ready to serve")
        with teller_ready_lock:
            teller_ready.append(self.tid)
            if len(teller_ready) == NUM_TELLERS:
                print("All tellers ready. Bank is now open.")
                bank_open.set()
        # For now, teller just waits — no customer interaction yet
        time.sleep(1)

class Customer(threading.Thread):
    def __init__(self, cid):
        super().__init__()
        self.cid = cid

    def run(self):
        bank_open.wait()
        transaction = random.choice(["Deposit", "Withdraw"])
        time.sleep(random.uniform(0, 0.1))  # wait 0–100ms before entering

        door_semaphore.acquire()
        print(f"Customer {self.cid} [Customer {self.cid}]: enters the bank")
        print(f"Customer {self.cid} [Customer {self.cid}]: chooses transaction: {transaction}")
        print(f"Customer {self.cid} [Customer {self.cid}]: leaving the bank")
        door_semaphore.release()

def main():
    tellers = [Teller(i) for i in range(NUM_TELLERS)]
    customers = [Customer(i) for i in range(NUM_CUSTOMERS)]

    for t in tellers:
        t.start()
    for c in customers:
        c.start()

    for t in tellers + customers:
        t.join()

    print("Simulation complete.")

if __name__ == "__main__":
    main()
