# Parking Lot System

An automated parking lot management simulation system written in Python.

## Overview

The system simulates a multi-slot parking lot grid where:
- The lot is initialized with a custom grid dimension, entrance point (`E`), paths (`.`), parking slots (`P`), and obstacles (`#`).
- Reachable parking slots and shortest walking distances from the entrance are calculated using Breadth-First Search (BFS).
- Nearest available slots are allocated using a min-heap (`heapq`).
- Supports vehicle allocation, departure, status listing, and queries by vehicle color or registration number.

## Supported Commands

- `create_parking_lot <rows> <cols>`: Initialize grid layout and usable slots.
- `park <reg_no> <color>`: Park car in nearest available slot.
- `leave <row> <col>`: Free slot at given coordinates.
- `status`: Show occupied slots, car registrations, and colors.
- `registration_numbers_for_cars_with_colour <color>`: Find registration numbers matching color.
- `slot_numbers_for_cars_with_colour <color>`: Find slot coordinates matching color.
- `slot_number_for_registration_number <reg_no>`: Find slot coordinates for specific vehicle.

## Getting Started

### Prerequisites

- Python 3.x

### Running the System

Navigate to the project directory and run:

```bash
cd parking_lot_system
python parking_lot.py input.txt
```
