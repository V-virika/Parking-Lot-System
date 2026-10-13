# Parking Lot System

A lightweight, high-performance command-line parking lot management system built in Python.

---

## Table of Contents

- [Problem Overview](#problem-overview)
- [Prerequisites & Setup](#prerequisites--setup)
- [How to Run](#how-to-run)
- [Running Tests](#running-tests)
- [Supported Commands](#supported-commands)
- [Design & Algorithm](#design--algorithm)

---

## Problem Overview

The system models a parking lot as a 2D grid containing:
- `E`: Entrance (exactly one)
- `.`: Road cell
- `#`: Wall / obstacle
- `P`: Parking slot

### Key Rules
1. **Movement**: Cars enter at `E` and travel only on road cells (`.`), moving up, down, left, or right (no diagonals).
2. **Accessibility**: A parking slot `P` is usable only if it is directly adjacent to a reachable road cell or the entrance. Unreachable slots are ignored.
3. **Distance Calculation**: Distance of a slot = number of road steps from `E` to the adjacent reachable cell + 1 step into the slot.
4. **Allocation Priority**: Cars are parked in the nearest available slot (smallest distance). Ties are broken by choosing the smaller row, then the smaller column.
5. **Coordinates**: 1-indexed in `(row, column)` format.

All data is kept in-memory without external database or API dependencies.

---

## Prerequisites & Setup

- **Python**: Python 3.8 or later (no third-party packages required; uses Python standard libraries: `heapq`, `sys`, `unittest`).

No installation or virtual environment configuration is needed.

---

## How to Run

To run the program with an input file:

### From the project root:
```bash
python parking_lot_system/parking_lot.py parking_lot_system/input.txt
```

### Or from inside the `parking_lot_system/` directory:
```bash
cd parking_lot_system
python parking_lot.py input.txt
```

You can pass any input file path as the first argument:
```bash
python parking_lot_system/parking_lot.py <path_to_input_file>
```

---

## Running Tests

A minimalistic test suite covering the full sample workflow and edge cases is included in [`tests/test_parking_lot.py`](tests/test_parking_lot.py).

Run the tests using Python's built-in `unittest` runner:

### From the project root:
```bash
python -m unittest discover tests
```

### Or run the test script directly:
```bash
python tests/test_parking_lot.py
```

---

## Supported Commands

| Command | Output Description |
| :--- | :--- |
| `create_parking_lot <rows> <cols>` followed by map rows | `Created a parking lot with <k> usable slots` |
| `park <registration_number> <colour>` | `Allocated slot: (r, c)` or `Sorry, parking lot is full` |
| `leave <row> <col>` | `Slot (r, c) is free` |
| `status` | Table of occupied slots in `(row, col)` order, or `Parking lot is empty` |
| `registration_numbers_for_cars_with_colour <colour>` | Comma-separated registration numbers, or `Not found` |
| `slot_numbers_for_cars_with_colour <colour>` | Comma-separated slot tuples, or `Not found` |
| `slot_number_for_registration_number <reg_no>` | Slot tuple `(r, c)`, or `Not found` |

*Notes:*
- Colour matching is case-insensitive.
- Results for `status` and colour lookups are sorted by row, then column.

---

## Design & Algorithm

- **Grid Reachability & Shortest Paths**: Breadth-First Search (BFS) computes minimum walking steps from the entrance `E` to all road cells in $O(R \times C)$ time.
- **Slot Allocation**: A min-heap (`heapq`) maintains free slots ordered by `(distance, row, column)`, enabling $O(\log K)$ allocation and release.
- **Fast Lookups**: Hash maps track vehicle registrations, occupied slots, and distances for $O(1)$ query and departure operations.
