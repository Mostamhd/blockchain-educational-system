# Plan: Update Thesis Module 3 (Benchmarking)

This plan outlines the necessary steps to align the Module 3 description in `thesis/chapter5.tex` with the actual implementation in `benchmark_suite.py`.

## Context
The current thesis text describes a simple "burst" stress test (sending 500 tx in a loop). The actual code implements a more sophisticated "rate-based" load generator (sending N tx/sec for T seconds). We also need to validate the methodology of using different loads for different consensus algorithms.

## Checklist

### Phase 1: Update Task 2 Description (The Stress Test)
- [ ] **Locate** `Task 2: The Stress Test` in `thesis/chapter5.tex`.
- [ ] **Rewrite** the instructions to shift from "Loop-based burst" to "Rate-based Load Generator".
    - [ ] *Old:* "Implement a loop that generates 500... transactions."
    - [ ] *New:* "Develop a multi-threaded Load Generator that continuously broadcasts transactions at a fixed rate (e.g., 20 TPS) for a specific duration."
- [ ] **Update** the list of steps:
    - [ ] Define the target rate (TPS).
    - [ ] Use a separate thread to maintain the rate without blocking the main execution.
    - [ ] Run the test for a fixed time window (e.g., 60 seconds).

### Phase 2: Update Reference Code Snippet
- [ ] **Locate** Listing `lst:mod3_stress` in `thesis/chapter5.tex`.
- [ ] **Replace** the existing `for` loop code with a simplified version of the `load_generator` function from `benchmark_suite.py`.
    - [ ] Include the `while` loop.
    - [ ] Include the `time.sleep` logic to maintain the rate.
- [ ] **Update** the caption or description to reflect "Rate-Limited Load Generator".

### Phase 3: Update Analysis of Findings
- [ ] **Locate** `2. Stress Test Analysis` in `thesis/chapter5.tex`.
- [ ] **Clarify** the methodology: Explain that valid benchmarking requires finding the **Saturation Point** (Maximum Sustainable Throughput).
- [ ] **Justify** using different loads:
    - [ ] Explain that PoW saturates at a much lower TPS than PoS.
    - [ ] State that the goal is to observe system behavior *at limit*, which requires tuning the load for each algorithm (e.g., testing PoW at 5 TPS and PoS at 50 TPS).
- [ ] **Update** the observations to reflect rate-based metrics (Stable vs. Unstable/Backlog) rather than just "time to finish".

## Verification
- [ ] **Review** the changes to ensure the academic tone is maintained.
- [ ] **Check** that the new code snippet roughly matches the logic in `practical-part/.../benchmark_suite.py`.
