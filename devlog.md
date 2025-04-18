# Devlog Entry - [04-09-2025, 2:30PM] 

### What I Know
This project is a multi-threaded **bank simulation** where 50 customers interact with 3 tellers. It involves synchronizing threads using semaphores in Python via the `threading` module. Each teller and customer is a thread. Shared resources like the **safe** (max 2 tellers), **manager** (1 teller), and **door** (2 customers at a time) must be protected using semaphores.

The program will simulate a real bank scenario:
- Customers choose to **deposit or withdraw**.
- Tellers must interact with **manager** (for withdrawals only) and then access the **safe** to complete transactions.
- The output must be **detailed logging of all actions**, showing both thread IDs and the action in progress.

Synchronization is critical here to ensure:
- No race conditions when multiple tellers interact with the manager or safe.
- Customers only enter when tellers are ready.
- Proper blocking and waking up when resources are busy.

### My Overall Plan
1. **Start small** — I'll begin with 3 tellers and maybe 3 customers to visualize output and get interaction structure down.
2. **Build incrementally**:
   - Phase 1: Setup basic threading and output formatting.
   - Phase 2: Customer-teller handshake (introductions and transaction communication).
   - Phase 3: Manager and safe interaction with semaphores.
   - Phase 4: Add constraints like max 2 customers in door, proper queueing, etc.
3. **Use Semaphores wisely** to prevent deadlocks. Each key part (manager, safe, teller-customer handshake, door) will likely need its own semaphore.
4. **Create a clean output log** that mirrors the format provided in the spec.
5. **Document all my findings and work** here in the devlog.

# Devlog Entry - [04-09-2025, 2:40PM] (Session Begins)

## Thoughts So Far:

This project simulates a bank environment with threading and semaphores. It involves three tellers and fifty customers, where synchronization is essential to manage access to shared resources: the bank manager, the safe, and the bank entrance. Only two customers can be in the bank at once, only two tellers can be in the safe at a time, and only one teller can talk to the manager at once.

Right now, the focus is just making sure the threading system is wired up and logging is working properly.

## Plan for This Session:

### Goal:
- Set up the initial Python project structure.
- Create a basic simulation with 3 teller threads and 5 customer threads.
- Ensure each thread prints an identifying message when it starts running.
- Verify that thread spawning, running, and joining works properly.

### Steps:
1. Create `main.py` and define teller and customer thread functions.
2. Spawn 3 teller threads, each with a unique ID.
3. Spawn 5 customer threads (starting small for testing).
4. Each thread prints a formatted line like: `"Customer 1 [Teller 0]: selects teller"`.
5. Confirm all threads run and complete execution without issue.

# Devlog Entry - [04-09-2025, 3:00PM] (Session Ends)

## Accomplishments:
- Successfully created the initial project structure.
- Implemented `main.py` with teller and customer thread functions.
- Verified correct startup, printing, and joining of all threads.
- Output is clean and matches expected format. Threading basics are confirmed functional.

## Problems Encountered:
- None during this session — everything worked on the first attempt since this part was basic setup.

## Additional Accomplishments:
- Confirmed thread IDs are passed properly to distinguish each teller and customer.

## Goals for Next Session:
- Implement the “bank open” condition — customers can’t enter until all tellers are ready.
- Introduce a semaphore to simulate only two customers being allowed through the door at once.
- Begin wiring basic interaction between customer and teller — customer chooses a transaction type and notifies a teller.

# Devlog Entry - [04-09-2025, 8:30PM] (Session Begins)

## Thoughts So Far:

Thread spawning and identification for customers and tellers is working great. Output formatting is in place and verified. Now, it's time to implement some of the bank’s constraints and the actual customer-teller interaction. This is where synchronization starts becoming important.

## Plan for This Session:

### Goal:
- Ensure the bank does not open until all 3 tellers are ready.
- Add a semaphore to control access through the door (max 2 customers in the bank).
- Add basic handshake: customer waits until teller is ready, then announces transaction.

### Steps:
1. Add an event or barrier to synchronize the tellers — customers wait until all tellers are ready.
2. Create a `threading.Semaphore(2)` to simulate door access (2 customers max).
3. Allow each customer to choose a random transaction (deposit or withdraw).
4. Print appropriate log messages showing each step: entering, choosing a teller, etc.

# Devlog Entry - [04-09-2025, 9:25PM] (Session Ends)

## Accomplishments:
- Successfully implemented the condition that the **bank does not open** until all three tellers are ready.
- Created a `bank_open` event that customers wait on before entering.
- Added a `door_semaphore` to simulate only two customers being able to enter the bank at a time.
- Each customer randomly chooses a transaction (either "Deposit" or "Withdraw") and logs it.
- Verified through output that:
  - Tellers start and notify readiness.
  - Customers wait until the bank is open before entering.
  - No more than two customers are inside at once.
  - Output format and sequencing remain clean and consistent.

## Problems Encountered:
- None major. There was a small race condition when all tellers were checking in, but wrapping that logic inside a lock (`teller_ready_lock`) solved it cleanly.

## Additional Accomplishments:
- Simulated realistic customer delays before entering (random 0–100ms wait).
- Used OOP (`Customer` and `Teller` subclasses of `threading.Thread`) to cleanly organize thread behavior for future expansion.

## Goals for Next Session:
- Implement actual customer-teller **interaction logic**.
  - Allow customers to find an available teller or wait in line.
  - Simulate teller requesting transaction, and customer responding.
  - Add logging to trace the interaction flow.
- Begin implementing manager and safe logic (semaphores) in parallel if time allows.

# Devlog Entry - [04-09-2025, 9:50PM] (Session Begins)

## Thoughts So Far:

The simulation is shaping up well. We’ve got the core threading infrastructure working, and basic synchronization is in place — the bank opens only when all tellers are ready, and only two customers can enter at a time. Each customer currently picks a transaction and prints logs, but there’s no real interaction between customers and tellers yet.

The next big piece is to simulate that interaction:
- Customers need to be paired with available tellers.
- Tellers should wait for customers, receive transactions, and respond accordingly.

This part will require careful use of semaphores, per-thread communication, and possibly queues.

## Plan for This Session:

### Goal:
- Create a system where customers wait for available tellers and then engage in a transaction.
- Tellers should be idle until signaled by a customer.
- Implement the back-and-forth where:
  - Customer introduces themselves
  - Teller asks for the transaction
  - Customer responds with the transaction type
  - Teller acknowledges

### Steps:
1. Set up a shared queue or structure to pair customers with tellers.
2. Use condition variables or per-thread semaphores for signaling.
3. Simulate a full interaction between a customer and a teller.
4. Ensure output logs reflect this step-by-step communication.

# Devlog Entry - [04-10-2025, 1:20AM] (Session Ends)

## Accomplishments:

- Implemented full **customer-teller interaction flow**.
- Set up a global `ready_tellers` queue protected by a `Condition` variable (`teller_available`) so customers can wait until a teller is available.
- Each `Teller` thread registers itself as ready and waits for a customer.
- Each `Customer` waits for a ready teller, introduces itself, waits for the teller to ask for a transaction, responds with "Deposit" or "Withdraw", and then leaves the bank.
- All interactions are synchronized using `Semaphore`s:
  - `customer_sem` to signal the teller a customer has arrived.
  - `transaction_sem` to let the customer know the teller is ready for the transaction.
  - `done_sem` to notify the teller the transaction has been provided.
- Verified clean and ordered output that matches project logging format.

## Problems Encountered:

- Needed to prevent customers from attempting to interact with a teller that wasn't ready. Solved this by wrapping the `ready_tellers` queue with a `Condition` that blocks until a teller is present.
- Needed to ensure clean exit for tellers after customers finish. Added a shutdown mechanism by sending a `None` customer and signaling via semaphore.

## Additional Accomplishments:

- Output logs now simulate realistic bank interactions and show both teller and customer actions step by step.
- Modular structure (OOP) is holding up well and ready for next layers of complexity (manager and safe).

## Goals for Next Session:

- Implement **interaction with the manager** for "Withdraw" transactions:
  - Only one teller can interact with the manager at a time.
  - Manager interaction is simulated with a sleep (5–30ms).
- Implement **safe access logic**:
  - Only two tellers can enter the safe at once.
  - Simulate transaction inside safe with a second sleep (10–50ms).
- Continue to follow logging format for manager/safe interactions (3 lines: going to, using, done).

# Devlog Entry - [04-10-2025, 1:30AM] (Session Begins)

## Thoughts So Far:

With teller-customer communication now working smoothly, it's time to move forward with the next two shared resources: **the manager and the safe**.

Both require semaphores to limit access:
- **Manager**: Only 1 teller can interact with the manager at a time, and only when the customer transaction is a "Withdraw".
- **Safe**: Max 2 tellers can be in the safe at once, for all transactions.

We’ll simulate each interaction with appropriate logging and a sleep to represent time spent.

## Plan for This Session:

### Goal:
- Add manager and safe access to the teller transaction flow.
- Use semaphores to control access:
  - 1-teller `manager_lock`
  - 2-teller `safe_lock`
- Simulate manager interaction (withdrawals only) with sleep (5–30ms).
- Simulate safe transaction with sleep (10–50ms).
- Log each access with 3 lines: going to, using, done using.

### Steps:
1. Create `manager_lock = Semaphore(1)` and `safe_lock = Semaphore(2)`.
2. Inside each teller’s transaction logic:
   - If transaction is "Withdraw", acquire manager, sleep, release.
   - Regardless of transaction, acquire safe, sleep, release.
3. Add logging before, during, and after each access to the manager and safe.
4. Test that only 1 teller talks to the manager at a time, and no more than 2 use the safe simultaneously.

# Devlog Entry - [04-10-2025, 2:00AM] (Session End) FINAL

## Accomplishments

- Successfully completed and stress-tested a multi-threaded bank simulation in Python, involving:
  - 3 concurrent teller threads
  - Up to 50 customer threads
  - Manager and safe access constraints enforced via semaphores
  - Door semaphore limiting bank occupancy to 2 customers at a time

- Implemented full customer-teller interaction with:
  - Randomized arrival times
  - Randomized transaction types (`Deposit` or `Withdraw`)
  - Realistic delays and output messages for manager/safe access

- Ensured proper inter-thread communication using:
  - `Semaphore`, `Condition`, and `Queue` objects
  - Custom signaling between each customer and their selected teller
  - Clean shutdown of all tellers after the last customer exits

- Resolved the following technical challenges:
  - Tellers logging transactions with `Customer None` on shutdown ➝ **Fixed** via conditional checks before and after transaction phase
  - Infinite loop from improperly queued tellers ➝ **Fixed** by shifting `ready_tellers.put()` to the start of the loop before shutdown check
  - Race conditions around shutdown ➝ **Avoided** by explicitly nullifying `transaction_type` and guarding all transaction logic

- Final version passed multiple test runs including:
  - Small-scale tests (5 customers)
  - Large-scale stress test with 50 customers
  - All output logs match the required format and thread-safe sequencing

## Key Design Decisions

- Used **dedicated semaphores per teller** for transaction handshakes:
  - `customer_sem`, `transaction_sem`, `done_sem`

- Used a **shared queue (`ready_tellers`)** with `Condition` lock for customer-teller selection

- Implemented a **centralized shutdown mechanism** from the main thread after all customers have exited

# Devlog Entry - [04-13-2025, 9:30PM] (Session End) ACTUAL FINAL

## Accomplishments

- Had to rework some of the code because I spotted some mistakes when testing on the CS1 server. 

## Issues 

- Not all of the customers 0-49 (50 customers) are being logged. Issue has been resolved now though. 

