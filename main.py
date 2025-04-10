import threading
import time
import random
import queue

NUM_TELLERS = 3
NUM_CUSTOMERS = 50  

bank_open = threading.Event()
door_semaphore = threading.Semaphore(2)

teller_ready = []
teller_ready_lock = threading.Lock()

ready_tellers = queue.Queue()
teller_available = threading.Condition()

manager_lock = threading.Semaphore(1)
safe_lock = threading.Semaphore(2)

class Teller(threading.Thread):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid
        self.customer_sem = threading.Semaphore(0)
        self.transaction_sem = threading.Semaphore(0)
        self.done_sem = threading.Semaphore(0)
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
                print(f"Teller {self.tid} [Teller {self.tid}]: shutting down")
                break

            print(f"Teller {self.tid} [Teller {self.tid}]: asks for transaction")
            self.transaction_sem.release()
            self.done_sem.acquire()

            if self.customer_id is None or self.transaction_type is None:
                print(f"Teller {self.tid} [Teller {self.tid}]: shutting down")
                break

            print(f"Teller {self.tid} [Teller {self.tid}]: received transaction: {self.transaction_type}")

            if self.transaction_type == "Withdraw":
                print(f"Teller {self.tid} [Teller {self.tid}]: going to manager")
                manager_lock.acquire()
                print(f"Teller {self.tid} [Teller {self.tid}]: speaking with manager")
                time.sleep(random.uniform(0.005, 0.03))
                print(f"Teller {self.tid} [Teller {self.tid}]: done with manager")
                manager_lock.release()

            print(f"Teller {self.tid} [Teller {self.tid}]: going to safe")
            safe_lock.acquire()
            print(f"Teller {self.tid} [Teller {self.tid}]: using safe")
            time.sleep(random.uniform(0.01, 0.05))
            print(f"Teller {self.tid} [Teller {self.tid}]: done using safe")
            safe_lock.release()

            if self.customer_id is not None:
                print(f"Teller {self.tid} [Teller {self.tid}]: transaction with Customer {self.customer_id} complete\n")

            self.customer_id = None
            self.transaction_type = None

class Customer(threading.Thread):
    def __init__(self, cid):
        super().__init__()
        self.cid = cid

    def run(self):
        bank_open.wait()
        time.sleep(random.uniform(0, 0.1))  # Simulate staggered arrival
        door_semaphore.acquire()

        print(f"Customer {self.cid} [Customer {self.cid}]: enters the bank")

        with teller_available:
            while ready_tellers.empty():
                teller_available.wait()
            teller = ready_tellers.get()

        print(f"Customer {self.cid} [Customer {self.cid}]: selects Teller {teller.tid}")
        teller.customer_id = self.cid
        teller.customer_sem.release()

        teller.transaction_sem.acquire()
        transaction = random.choice(["Deposit", "Withdraw"])
        teller.transaction_type = transaction
        print(f"Customer {self.cid} [Customer {self.cid}]: says {transaction}")
        teller.done_sem.release()

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

    
    for t in tellers:
        t.customer_id = None
        t.transaction_type = None  
        t.customer_sem.release()
    for t in tellers:
        t.join()

    print("Simulation complete.")

if __name__ == "__main__":
    main()
