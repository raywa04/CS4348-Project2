import threading
import time
import random
import queue

# Constants for the number of tellers and customers
NUM_TELLERS = 3
NUM_CUSTOMERS = 50  

# Event to signal when the bank is open
bank_open = threading.Event()

# Semaphore to limit the number of customers entering the bank at the same time
door_semaphore = threading.Semaphore(2)

# Shared resources for teller management
teller_ready = []  # List to track ready tellers
teller_ready_lock = threading.Lock()  # Lock for accessing teller_ready list

ready_tellers = queue.Queue()  # Queue to hold available tellers
teller_available = threading.Condition()  # Condition variable for teller availability

# Semaphores for manager and safe access
manager_lock = threading.Semaphore(1)  # Only one teller can interact with the manager at a time
safe_lock = threading.Semaphore(2)  # Up to two tellers can use the safe simultaneously

# Class representing a Teller
class Teller(threading.Thread):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid  # Teller ID
        self.customer_sem = threading.Semaphore(0)  # Semaphore to wait for a customer
        self.transaction_sem = threading.Semaphore(0)  # Semaphore to wait for a transaction
        self.done_sem = threading.Semaphore(0)  # Semaphore to signal transaction completion
        self.customer_id = None  # ID of the current customer
        self.transaction_type = None  # Type of transaction (Deposit/Withdraw)

    def run(self):
        # Mark the teller as ready and notify when all tellers are ready
        print(f"Teller {self.tid} [Teller {self.tid}]: is ready to serve")
        with teller_ready_lock:
            teller_ready.append(self.tid)
            if len(teller_ready) == NUM_TELLERS:
                print("All tellers ready. Bank is now open.")
                bank_open.set()

        while True:
            # Add the teller to the ready queue and notify customers
            with teller_available:
                ready_tellers.put(self)
                teller_available.notify()

            # Wait for a customer to arrive
            self.customer_sem.acquire()

            # Check if the teller should shut down
            if self.customer_id is None:
                print(f"Teller {self.tid} [Teller {self.tid}]: shutting down")
                break

            # Process the transaction
            print(f"Teller {self.tid} [Teller {self.tid}]: asks for transaction")
            self.transaction_sem.release()
            self.done_sem.acquire()

            # Check again if the teller should shut down
            if self.customer_id is None or self.transaction_type is None:
                print(f"Teller {self.tid} [Teller {self.tid}]: shutting down")
                break

            print(f"Teller {self.tid} [Teller {self.tid}]: received transaction: {self.transaction_type}")

            # Handle withdrawal transactions by interacting with the manager
            if self.transaction_type == "Withdraw":
                print(f"Teller {self.tid} [Teller {self.tid}]: going to manager")
                manager_lock.acquire()
                print(f"Teller {self.tid} [Teller {self.tid}]: speaking with manager")
                time.sleep(random.uniform(0.005, 0.03))  # Simulate manager interaction time
                print(f"Teller {self.tid} [Teller {self.tid}]: done with manager")
                manager_lock.release()

            # Use the safe for the transaction
            print(f"Teller {self.tid} [Teller {self.tid}]: going to safe")
            safe_lock.acquire()
            print(f"Teller {self.tid} [Teller {self.tid}]: using safe")
            time.sleep(random.uniform(0.01, 0.05))  # Simulate safe usage time
            print(f"Teller {self.tid} [Teller {self.tid}]: done using safe")
            safe_lock.release()

            # Complete the transaction
            if self.customer_id is not None:
                print(f"Teller {self.tid} [Teller {self.tid}]: transaction with Customer {self.customer_id} complete\n")

            # Reset teller state
            self.customer_id = None
            self.transaction_type = None

# Class representing a Customer
class Customer(threading.Thread):
    def __init__(self, cid):
        super().__init__()
        self.cid = cid  # Customer ID

    def run(self):
        # Wait for the bank to open
        bank_open.wait()
        time.sleep(random.uniform(0, 0.1))  # Simulate staggered arrival
        door_semaphore.acquire()  # Enter the bank

        print(f"Customer {self.cid} [Customer {self.cid}]: enters the bank")

        # Wait for an available teller
        with teller_available:
            while ready_tellers.empty():
                teller_available.wait()
            teller = ready_tellers.get()

        # Interact with the teller
        print(f"Customer {self.cid} [Customer {self.cid}]: selects Teller {teller.tid}")
        teller.customer_id = self.cid
        teller.customer_sem.release()

        teller.transaction_sem.acquire()
        transaction = random.choice(["Deposit", "Withdraw"])  # Randomly choose a transaction type
        teller.transaction_type = transaction
        print(f"Customer {self.cid} [Customer {self.cid}]: says {transaction}")
        teller.done_sem.release()

        # Leave the bank
        print(f"Customer {self.cid} [Customer {self.cid}]: leaving the bank\n")
        door_semaphore.release()

# Main function to start the simulation
def main():
    # Create tellers and customers
    tellers = [Teller(i) for i in range(NUM_TELLERS)]
    customers = [Customer(i) for i in range(NUM_CUSTOMERS)]

    # Start all teller threads
    for t in tellers:
        t.start()
    # Start all customer threads
    for c in customers:
        c.start()

    # Wait for all customers to finish
    for c in customers:
        c.join()

    # Signal all tellers to shut down
    for t in tellers:
        t.customer_id = None
        t.transaction_type = None  
        t.customer_sem.release()
    # Wait for all tellers to finish
    for t in tellers:
        t.join()

    print("Simulation complete.")

# Entry point of the program
if __name__ == "__main__":
    main()