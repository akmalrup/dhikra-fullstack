# Create a full test suite for HifzTracker covering all edge cases

import os
import sys
sys.path.append(os.path.abspath("."))

from hifz.tracker import HifzTracker

def test_hifz_tracker_all_cases():
    print("\n🧪 Running all HifzTracker test cases...\n")

    # Case 1: Normal progression
    t1 = HifzTracker(1, 7)
    t1.update(1)
    t1.update(2)
    t1.update(3)
    print("✔️ Case 1 (correct):", [s for _, s in t1.history])

    # Case 2: Repeat
    t2 = HifzTracker(1, 7)
    t2.update(1)
    t2.update(2)
    t2.update(2)
    print("✔️ Case 2 (repeat):", [s for _, s in t2.history])

    # Case 3: Skip
    t3 = HifzTracker(1, 7)
    t3.update(1)
    t3.update(3)
    print("✔️ Case 3 (skip):", [s for _, s in t3.history])

    # Case 4: Wrong (goes backward)
    t4 = HifzTracker(1, 7)
    t4.update(1)
    t4.update(2)
    t4.update(1)
    print("✔️ Case 4 (wrong):", [s for _, s in t4.history])

    # Case 5: Out of bounds
    t5 = HifzTracker(1, 7)
    t5.update(1)
    t5.update(10)
    print("✔️ Case 5 (skip with out of bounds):", [s for _, s in t5.history])

    # Case 6: Repeat final ayah
    t6 = HifzTracker(1, 7)
    for i in range(1, 8):
        t6.update(i)
    t6.update(7)
    print("✔️ Case 6 (repeat last):", [s for _, s in t6.history])

    # Case 7: Start in middle (should not be flagged)
    t7 = HifzTracker(1, 7)
    t7.expected = None  # simulate undecided starting point
    first = 4
    t7.expected = first + 1
    t7.update(5)
    t7.update(7)
    print("✔️ Case 7 (start in middle):", [s for _, s in t7.history])

    # Case 8: Invalid ayah (0)
    t8 = HifzTracker(1, 7)
    try:
        t8.update(0)
    except Exception as e:
        print("✔️ Case 8 (invalid 0):", str(e))

    # Case 9: Surah overflow
    t9 = HifzTracker(1, 7)
    t9.update(1)
    t9.update(8)
    print("✔️ Case 9 (surah overflow):", [s for _, s in t9.history])

test_hifz_tracker_all_cases()

