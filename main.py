import threading
import time
import random
import queue

NUM_TELLERS = 3
NUM_CUSTOMERS = 5  # Start small

bank_open = threading.Event()
door_semaphore = threading.Semaphore(2)

teller_ready = []
teller_ready_lock = threading.Lock()

ready_tellers = queue.Queue()
teller_available = threading.Condition()

class Teller(threading.Thread):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid
        self.customer_sem = threading.Semaphore(0)  # Signaled when a customer arrives
        self.transaction_sem = threading.Semaphore(0)  # Used to prompt customer for transaction
        self.done_sem = threading.Semaphore(0)  # Used when teller finishes
        self.customer_id = None
        self.transaction_type = None

    def run(self):
        print(f"Teller {self.tid} [Teller {self.tid}]: is ready to serve")
        with teller_ready_lock:
            teller_ready.append(self.tid)
            if len(teller_ready) == NUM_TELLERS:
                print("All tellers ready. Bank is now open.")
                bank_open.set()

        while True:
            with teller_available:
                ready_tellers.put(self)
                teller_available.notify()

            self.customer_sem.acquire()
            if self.customer_id is None:
                break  # simulation over

            print(f"Teller {self.tid} [Teller {self.tid}]: asks for transaction")
            self.transaction_sem.release()  # Prompt customer to respond
            self.done_sem.acquire()  # Wait until customer provides transaction

            print(f"Teller {self.tid} [Teller {self.tid}]: received transaction: {self.transaction_type}")
            print(f"Teller {self.tid} [Teller {self.tid}]: transaction with Customer {self.customer_id} complete\n")

            self.customer_id = None
            self.transaction_type = None

class Customer(threading.Thread):
    def __init__(self, cid):
        super().__init__()
        self.cid = cid

    def run(self):
        bank_open.wait()
        time.sleep(random.uniform(0, 0.1))
        door_semaphore.acquire()

        print(f"Customer {self.cid} [Customer {self.cid}]: enters the bank")

        # Wait for a ready teller
        with teller_available:
            while ready_tellers.empty():
                teller_available.wait()
            teller = ready_tellers.get()

        print(f"Customer {self.cid} [Customer {self.cid}]: selects Teller {teller.tid}")
        teller.customer_id = self.cid
        teller.customer_sem.release()  # Notify teller customer has arrived

        teller.transaction_sem.acquire()  # Wait for teller to ask for transaction
        transaction = random.choice(["Deposit", "Withdraw"])
        teller.transaction_type = transaction
        print(f"Customer {self.cid} [Customer {self.cid}]: says {transaction}")
        teller.done_sem.release()  # Inform teller transaction sent

        print(f"Customer {self.cid} [Customer {self.cid}]: leaving the bank\n")
        door_semaphore.release()

def main():
    tellers = [Teller(i) for i in range(NUM_TELLERS)]
    customers = [Customer(i) for i in range(NUM_CUSTOMERS)]

    for t in tellers:
        t.start()
    for c in customers:
        c.start()

    for c in customers:
        c.join()

    # Tell all tellers to exit
    for t in tellers:
        t.customer_id = None
        t.customer_sem.release()
    for t in tellers:
        t.join()

    print("Simulation complete.")

if __name__ == "__main__":
    main()
