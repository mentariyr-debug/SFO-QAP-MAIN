from typing import List, Tuple


def print_random_populations(engine) -> None:
    print("\n" + "="*80)
    print("2. RANDOM SAILFISH AND SARDINES")
    print("="*80)
    engine.sailfish_random_values = engine.generate_random_values(engine.n_sailfish)
    engine.sardine_random_values = engine.generate_random_values(engine.n_sardines)
    print("SAILFISH Random Values:")
    print(f"{'ID':<8}", end="")
    for loc in range(engine.problem_size):
        print(f"{'Loc ' + str(loc+1):>8}", end="")
    print()
    for i in range(engine.n_sailfish):
        print(f"SF{i+1:<7}", end="")
        for val in engine.sailfish_random_values[i]:
            print(f"{val:8.3f}", end="")
        print()
    print("\nSARDINE Random Values:")
    print(f"{'ID':<8}", end="")
    for loc in range(engine.problem_size):
        print(f"{'Loc ' + str(loc+1):>8}", end="")
    print()
    for i in range(engine.n_sardines):
        print(f"S{i+1:<7}", end="")
        for val in engine.sardine_random_values[i]:
            print(f"{val:8.3f}", end="")
        print()


def save_original_positions(engine) -> None:
    engine.original_sailfish_positions = [pos.copy() for pos in engine.sailfish_random_values]
    engine.original_sardine_positions = [pos.copy() for pos in engine.sardine_random_values]
    if engine.current_iteration == 0:
        print(f"\n" + "="*80)
        print("SAVING ORIGINAL POSITIONS FOR NEXT ITERATION")
        print("="*80)
        print("IMPORTANT: These original positions will be used for position updates")
        print("in the next iteration, NOT the positions after sorting/replacement!")
        print()
        print("Original Sailfish Positions (before sorting/replacement):")
        for i, pos in enumerate(engine.original_sailfish_positions):
            print(f"  SF{i+1}: {[f'{x:.3f}' for x in pos]}")
        print("\nOriginal Sardine Positions (before sorting/replacement):")
        for i, pos in enumerate(engine.original_sardine_positions):
            print(f"  S{i+1}: {[f'{x:.3f}' for x in pos]}")


def print_sorted_arrays_and_solutions(engine) -> None:
    print("\n" + "="*80)
    if engine.current_iteration == 0:
        print("3. SORTED ARRAYS FOR EACH SAILFISH AND SARDINE")
    else:
        print(f"ITERATION {engine.current_iteration} - STEP 1: SORTING NEW POSITIONS")
    print("="*80)
    engine.sailfish_solutions = []
    engine.sardine_solutions = []
    print("SAILFISH Sorted Arrays and Solutions:")
    for i in range(engine.n_sailfish):
        print(f"\n===== SF{i+1} ====================================================")
        random_vals = engine.sailfish_random_values[i]
        solution, sorted_array = engine.convert_random_to_solution(random_vals)
        engine.sailfish_solutions.append(solution)
        sorted_values = sorted(random_vals)
        print(f"Original: {random_vals}")
        print(f"Sorted  : {sorted_values} -> {sorted_array}")
        facility_assignments = []
        for loc, facility in enumerate(sorted_array, 1):
            facility_assignments.append(f"Facility {facility} for Loc {loc}")
        print(f"Assignment: {', '.join(facility_assignments)}")
    print(f"\nSARDINE Sorted Arrays and Solutions:")
    for i in range(engine.n_sardines):
        print(f"\n===== S{i+1} ====================================================")
        random_vals = engine.sardine_random_values[i]
        solution, sorted_array = engine.convert_random_to_solution(random_vals)
        engine.sardine_solutions.append(solution)
        sorted_values = sorted(random_vals)
        print(f"Original: {random_vals}")
        print(f"Sorted  : {sorted_values} -> {sorted_array}")
        facility_assignments = []
        for loc, facility in enumerate(sorted_array, 1):
            facility_assignments.append(f"Facility {facility} for Loc {loc}")
        print(f"Assignment: {', '.join(facility_assignments)}")



