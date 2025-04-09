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
