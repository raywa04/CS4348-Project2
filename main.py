import threading
import time
from queue import Queue
import random

# Number of tellers and customers
tellers = 3
customers = 50

# Semaphores to control access to resources
bank_door = threading.Semaphore(2)  # Max two customers in the bank door
bank_safe = threading.Semaphore(2)  # Max two tellers at the safe
manager = threading.Semaphore(1)    # Max one teller with the manager
teller_ready = threading.Semaphore(0)  # Indicates if a teller is ready for the next customer
lock = threading.Lock()  # General lock for thread safety

# Queues for tellers and customers
teller_queue = Queue()
customer_queue = Queue()

# Counter for the number of customers served
numCustomerServed = 0
numCustomerServed_lock = threading.Lock()  # Lock for thread-safe access to the counter

# Teller class representing a bank teller
class Teller(threading.Thread):
    def __init__(self, tid):
        super().__init__()
        self.id = tid
        self.customerAvailability = threading.Semaphore(0)  # Semaphore to indicate teller availability
        self.customer = None  # Current customer being served
        self.transaction = None  # Current transaction type

    def run(self):
        global numCustomerServed
        while True:
            # Teller is ready for a customer
            print(f"Teller {self.id} [Teller {self.id}]: Ready for Customer")
            teller_queue.put(self)  # Add teller to the queue
            teller_ready.release()  # Signal that a teller is ready

            self.customerAvailability.acquire()  # Wait for a customer to approach

            if self.customer is None:  # Exit condition
                break

            # Interact with the customer
            print(f"Teller {self.id} [Customer {self.customer.id}]: What is the transaction?")
            self.transaction = self.customer.getTransaction()

            # Handle "Withdraw" transactions by interacting with the manager
            if self.transaction == "Withdraw":
                print(f"Teller {self.id} [Teller {self.id}]: Go to Manager")
                manager.acquire()
                print(f"Teller {self.id} [Teller {self.id}]: Interact with Manager")
                time.sleep(random.uniform(0.005, 0.03))  # Simulate interaction time
                print(f"Teller {self.id} [Teller {self.id}]: Manager complete")
                manager.release()

            # Access the bank safe
            print(f"Teller {self.id} [Teller {self.id}]: Going to Safe")
            bank_safe.acquire()
            print(f"Teller {self.id} [Teller {self.id}]: In the Safe")
            time.sleep(random.uniform(0.01, 0.05))  # Simulate time in the safe
            print(f"Teller {self.id} [Teller {self.id}]: Done in safe")
            bank_safe.release()

            # Complete the transaction
            print(f"Teller {self.id} [Customer {self.customer.id}]: Transaction Complete")
            self.customer.complete.release()  # Notify the customer that the transaction is complete

            self.customer.leave.acquire()  # Wait for the customer to leave

            # Update the number of customers served
            with numCustomerServed_lock:
                numCustomerServed += 1
                if numCustomerServed >= customers:  # Exit condition
                    break

# Customer class representing a bank customer
class Customer(threading.Thread):
    def __init__(self, cid):
        super().__init__()
        self.id = cid
        self.transaction = random.choice(["Deposit", "Withdraw"])  # Randomly choose a transaction type
        self.complete = threading.Semaphore(0)  # Semaphore to indicate transaction completion
        self.leave = threading.Semaphore(0)  # Semaphore to indicate customer leaving

    def getTransaction(self):
        # Customer provides the transaction type
        print(f"Customer {self.id} [Teller {self.teller.id}]: gives transaction")
        return self.transaction

    def run(self):
        # Simulate customer arriving at the bank
        time.sleep(random.uniform(0, 0.1))
        bank_door.acquire()  # Enter the bank
        print(f"Customer {self.id} [Customer {self.id}]: enters bank")

        # Select a teller
        teller_ready.acquire()
        teller = teller_queue.get()
        self.teller = teller
        teller.customer = self
        print(f"Customer {self.id} [Teller {teller.id}]: selects teller")
        teller.customerAvailability.release()  # Notify the teller

        self.complete.acquire()  # Wait for the transaction to complete
        print(f"Customer {self.id} [Teller {teller.id}]: leaving bank")
        self.leave.release()  # Notify the teller that the customer is leaving
        bank_door.release()  # Exit the bank

# Create teller and customer threads
tellers_thread = [Teller(i) for i in range(tellers)]
customers_thread = [Customer(i) for i in range(customers)]

# Start all teller threads
for t in tellers_thread:
    t.start()

# Start all customer threads
for c in customers_thread:
    c.start()

# Wait for all customer threads to finish
for c in customers_thread:
    c.join()

# Signal all tellers to stop
for t in tellers_thread:
    t.customer = None
    t.customerAvailability.release()

# Wait for all teller threads to finish
for t in tellers_thread:
    t.join()