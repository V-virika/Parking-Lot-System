# Parking Lot System

An automated parking lot management simulation system written in Python.

## Overview

The system simulates a multi-slot parking lot grid where:
- The lot is initialized with a custom grid dimension, entrance point (`E`), paths (`.`), parking slots (`P`), and obstacles (`#`).
- Reachable parking slots and shortest walking distances from the entrance are calculated using Breadth-First Search (BFS).
- Nearest available slots are allocated using a min-heap (`heapq`).
- Supports vehicle allocation, departure, status listing, and queries by vehicle color or registration number.
