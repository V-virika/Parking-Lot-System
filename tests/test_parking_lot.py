import os
import sys
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parking_lot_system.parking_lot import ParkingLot, run_program


class TestParkingLot(unittest.TestCase):
    def test_sample_workflow(self):
        sample_input = [
            "create_parking_lot 5 7",
            "E.....P",
            "P#P#P.P",
            "P.....#",
            "PP#P#.P",
            "P####.P",
            "park KA-01-HH-1234 White",
            "park KA-01-HH-9999 White",
            "park KA-01-BB-0001 Black",
            "park KA-01-HH-7777 Red",
            "park KA-01-HH-2701 Blue",
            "park KA-01-HH-3141 Black",
            "park KA-01-HH-5555 Grey",
            "park KA-01-HH-6666 White",
            "park KA-01-HH-8888 Red",
            "park KA-01-HH-1111 Blue",
            "leave 1 7",
            "leave 2 1",
            "status",
            "park KA-01-P-333 White",
            "park DL-12-AA-9999 White",
            "park MH-04-AY-1111 Black",
            "registration_numbers_for_cars_with_colour White",
            "slot_numbers_for_cars_with_colour White",
            "slot_number_for_registration_number KA-01-HH-3141",
            "slot_number_for_registration_number MH-04-AY-1111",
            "slot_number_for_registration_number TN-07-ZZ-0000",
        ]
        expected_output = [
            "Created a parking lot with 10 usable slots",
            "Allocated slot: (2, 1)",
            "Allocated slot: (2, 3)",
            "Allocated slot: (2, 5)",
            "Allocated slot: (1, 7)",
            "Allocated slot: (2, 7)",
            "Allocated slot: (4, 7)",
            "Allocated slot: (4, 4)",
            "Allocated slot: (5, 7)",
            "Allocated slot: (3, 1)",
            "Allocated slot: (4, 2)",
            "Slot (1, 7) is free",
            "Slot (2, 1) is free",
            "Slot      Registration No   Colour\n"
            "(2, 3)    KA-01-HH-9999     White\n"
            "(2, 5)    KA-01-BB-0001     Black\n"
            "(2, 7)    KA-01-HH-2701     Blue\n"
            "(3, 1)    KA-01-HH-8888     Red\n"
            "(4, 2)    KA-01-HH-1111     Blue\n"
            "(4, 4)    KA-01-HH-5555     Grey\n"
            "(4, 7)    KA-01-HH-3141     Black\n"
            "(5, 7)    KA-01-HH-6666     White",
            "Allocated slot: (2, 1)",
            "Allocated slot: (1, 7)",
            "Sorry, parking lot is full",
            "DL-12-AA-9999, KA-01-P-333, KA-01-HH-9999, KA-01-HH-6666",
            "(1, 7), (2, 1), (2, 3), (5, 7)",
            "(4, 7)",
            "Not found",
            "Not found",
        ]
        output = run_program(sample_input)
        self.assertEqual(output, expected_output)

    def test_edge_cases(self):
        # 1. Unreachable slots are ignored
        grid = [
            "E.",
            "##",
            "P.",  # unreachable due to wall
        ]
        lot = ParkingLot(3, 2, grid)
        self.assertEqual(len(lot.slot_dist), 0)

        # 2. Empty lot status
        grid2 = ["E.P"]
        lot2 = ParkingLot(1, 3, grid2)
        self.assertEqual(lot2.status(), "Parking lot is empty")

        # 3. Allocation and full lot
        self.assertEqual(lot2.park("KA-01", "White"), "Allocated slot: (1, 3)")
        self.assertEqual(lot2.park("KA-02", "Black"), "Sorry, parking lot is full")

        # 4. Case-insensitive color query
        self.assertEqual(lot2.registrations_by_colour("white"), "KA-01")
        self.assertEqual(lot2.registrations_by_colour("WHITE"), "KA-01")
        self.assertEqual(lot2.slots_by_colour("white"), "(1, 3)")

        # 5. Not found queries
        self.assertEqual(lot2.registrations_by_colour("Red"), "Not found")
        self.assertEqual(lot2.slot_by_registration("KA-99"), "Not found")

        # 6. Leave and re-park
        self.assertEqual(lot2.leave(1, 3), "Slot (1, 3) is free")
        self.assertEqual(lot2.park("KA-03", "Red"), "Allocated slot: (1, 3)")


if __name__ == "__main__":
    unittest.main()
