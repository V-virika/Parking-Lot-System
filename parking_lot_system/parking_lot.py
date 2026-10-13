import heapq
import sys


class Car:
    def __init__(self, registration, colour):
        self.registration = registration
        self.colour = colour


class ParkingLot:
    def __init__(self, rows, cols, grid):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.entrance = None

        # Find the entrance.
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "E":
                    self.entrance = (r, c)

        # Calculate distances using BFS.
        self.dist = [[-1] * cols for _ in range(rows)]
        er, ec = self.entrance
        self.dist[er][ec] = 0
        queue = [(er, ec)]
        index = 0

        while index < len(queue):
            r, c = queue[index]
            index += 1

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr = r + dr
                nc = c + dc

                if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                    continue
                if self.dist[nr][nc] != -1:
                    continue
                if grid[nr][nc] not in [".", "E"]:
                    continue

                self.dist[nr][nc] = self.dist[r][c] + 1
                queue.append((nr, nc))

        # Store each reachable slot as (distance, row, column).
        self.slot_dist = {}
        self.free_slots = []

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "P":
                    continue

                nearby = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if self.dist[nr][nc] >= 0:
                            nearby.append(self.dist[nr][nc])

                if nearby:
                    distance = min(nearby) + 1
                    self.slot_dist[(r, c)] = distance
                    self.free_slots.append((distance, r, c))

        heapq.heapify(self.free_slots)
        self.parked_cars = {}
        self.registration_to_slot = {}

    def park(self, registration, colour):
        if registration in self.registration_to_slot:
            return "Invalid command"
        if not self.free_slots:
            return "Sorry, parking lot is full"

        distance, r, c = heapq.heappop(self.free_slots)
        car = Car(registration, colour)
        self.parked_cars[(r, c)] = car
        self.registration_to_slot[registration] = (r, c)
        return "Allocated slot: (" + str(r + 1) + ", " + str(c + 1) + ")"

    def leave(self, row, col):
        slot = (row - 1, col - 1)

        if slot not in self.parked_cars:
            return "Invalid command"

        car = self.parked_cars.pop(slot)
        del self.registration_to_slot[car.registration]

        distance = self.slot_dist[slot]
        heapq.heappush(self.free_slots, (distance, slot[0], slot[1]))
        return "Slot (" + str(row) + ", " + str(col) + ") is free"

    def status(self):
        if not self.parked_cars:
            return "Parking lot is empty"

        result = ["Slot      Registration No   Colour"]
        for r, c in sorted(self.parked_cars):
            car = self.parked_cars[(r, c)]
            result.append(
                "(" + str(r + 1) + ", " + str(c + 1) + ")    "
                + car.registration.ljust(17) + " " + car.colour
            )
        return "\n".join(result)

    def registrations_by_colour(self, colour):
        result = []
        for slot in sorted(self.parked_cars):
            car = self.parked_cars[slot]
            if car.colour.lower() == colour.lower():
                result.append(car.registration)
        return ", ".join(result) if result else "Not found"

    def slots_by_colour(self, colour):
        result = []
        for r, c in sorted(self.parked_cars):
            car = self.parked_cars[(r, c)]
            if car.colour.lower() == colour.lower():
                result.append("(" + str(r + 1) + ", " + str(c + 1) + ")")
        return ", ".join(result) if result else "Not found"

    def slot_by_registration(self, registration):
        if registration not in self.registration_to_slot:
            return "Not found"
        r, c = self.registration_to_slot[registration]
        return "(" + str(r + 1) + ", " + str(c + 1) + ")"


def run_program(lines):
    lot = None
    output = []
    i = 0

    while i < len(lines):
        command_line = lines[i].strip()
        i += 1

        if command_line == "":
            continue

        parts = command_line.split()
        command = parts[0]

        if command == "create_parking_lot":
            try:
                rows = int(parts[1])
                cols = int(parts[2])
                grid = [lines[i + r].strip() for r in range(rows)]
                i += rows
                lot = ParkingLot(rows, cols, grid)
                output.append("Created a parking lot with "
                              + str(len(lot.slot_dist)) + " usable slots")
            except (ValueError, IndexError):
                lot = None

        elif lot is None:
            continue

        elif command == "park" and len(parts) == 3:
            output.append(lot.park(parts[1], parts[2]))

        elif command == "leave" and len(parts) == 3:
            try:
                output.append(lot.leave(int(parts[1]), int(parts[2])))
            except ValueError:
                continue

        elif command == "status":
            output.append(lot.status())

        elif command == "registration_numbers_for_cars_with_colour" and len(parts) == 2:
            output.append(lot.registrations_by_colour(parts[1]))

        elif command == "slot_numbers_for_cars_with_colour" and len(parts) == 2:
            output.append(lot.slots_by_colour(parts[1]))

        elif command == "slot_number_for_registration_number" and len(parts) == 2:
            output.append(lot.slot_by_registration(parts[1]))

        # Unknown or incomplete commands are ignored.

    return output


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        file = open(filename, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
    except OSError:
        print("Could not open " + filename)
        return

    results = run_program(lines)
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
