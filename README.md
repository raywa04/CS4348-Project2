# CS4348 Project 2 — Multithreaded Bank Simulation

## Overview

This project simulates a multithreaded banking environment in Python, involving:

- 3 Tellers  
- Up to 50 Customers  
- Access-controlled resources: Manager (1 at a time), Safe (2 at a time)  
- Maximum 2 customers allowed in the bank concurrently  
- Full concurrency using Python's `threading` and `queue` modules  

The simulation demonstrates synchronization, semaphore usage, thread communication, and graceful shutdown of concurrent systems.

## How to Run

1. Ensure you're using Python 3:

   ```bash
   python3 --version

2. How to run:

   ```bash
   python3 main.py

## File Descriptions

| **File** | **Description** |
|------------|---------------|
| `README.md` | Description of the project |
| `devlog.md` | Report of my progress through the project |
| `main.py` | The project itself of the bank simulation |
