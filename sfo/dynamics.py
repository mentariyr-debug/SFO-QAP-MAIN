import random
from typing import List


def calculate_pd_and_lambda_values(engine) -> None:
    print(f"\n" + "="*80)
    if engine.current_iteration == 0:
        print("5. CALCULATE PD AND LAMBDA VALUES (CORRECTED)")
    else:
        print(f"ITERATION {engine.current_iteration} - STEP 5: CALCULATE PD AND LAMBDA VALUES (CORRECTED)")
    print("="*80)
    total_population = engine.n_sailfish + engine.n_sardines
    engine.PD = 1 - (engine.n_sailfish / total_population)
    print(f"Population Decline (PD) Calculation:")
    print(f"PD = 1 - (num_sailfish / total_population)")
    print(f"PD = 1 - ({engine.n_sailfish} / {total_population})")
    print(f"PD = 1 - {engine.n_sailfish / total_population:.6f}")
    print(f"PD = {engine.PD:.6f}")
    print()
    engine.lambda_k_values = []
    print("Lambda Calculations (CORRECTED):")
    print("-" * 50)
    for k in range(engine.n_sailfish):
        random_val = round(random.random(), 3)
        lambda_k = (2 * random_val * engine.PD) - engine.PD
        engine.lambda_k_values.append(lambda_k)
        print(f"SF{k+1}:")
        print(f"  Random = {random_val}")
        print(f"  λ_{k+1} = (2 × {random_val} × {engine.PD:.6f}) - {engine.PD:.6f}")
        print(f"       = {2 * random_val * engine.PD:.6f} - {engine.PD:.6f}")
        print(f"       = {lambda_k:.6f}")
        print()
    print(f"Lambda Summary: {[f'{val:.6f}' for val in engine.lambda_k_values]}")


def update_sailfish_positions(engine) -> None:
    print(f"\n" + "="*80)
    if engine.current_iteration == 0:
        print("6. UPDATE SAILFISH POSITIONS (CORRECTED - USING FITNESS SCORES)")
    else:
        print(f"ITERATION {engine.current_iteration} - STEP 6: UPDATE SAILFISH POSITIONS (CORRECTED - USING FITNESS SCORES)")
    print("="*80)
    print("CORRECTED Sailfish Position Update Formula:")
    print("SF_i_location[j] = elite_sailfish_fitness_score - λ_k × ((random(0,1) × (elite_sailfish_fitness_score + injured_sardine_fitness_score)/2) - old_sailfish)")
    print()
    print("IMPORTANT: Using FITNESS SCORES instead of position values!")
    print()
    print(f"Elite sailfish fitness score: {engine.elite_sailfish_fitness_score}")
    print(f"Injured sardine fitness score: {engine.injured_sardine_fitness_score}")
    print()
    
    # NEW: Check if any sailfish should use sardine sorted positions from replacements
    sailfish_using_sardine_positions = getattr(engine, 'sailfish_using_sardine_positions', {})
    
    if sailfish_using_sardine_positions:
        print("REPLACEMENT POSITION TRACKING ACTIVE:")
        print("Some sailfish will use their original sardine sorted positions for updates:")
        for sf_idx, sardine_pos in sailfish_using_sardine_positions.items():
            print(f"  SF{sf_idx+1}: Using sardine sorted position {[f'{x:.3f}' for x in sardine_pos]}")
        print()
    
    # Use SORTED positions as the base for updates, with replacement position tracking
    print("Using SORTED positions for updates (with replacement position tracking):")
    sorted_sailfish_positions: List[List[float]] = []
    
    for i in range(engine.n_sailfish):
        if i in sailfish_using_sardine_positions:
            # This sailfish was replaced by a sardine - use the stored sardine sorted position
            sorted_pos = sailfish_using_sardine_positions[i]
            print(f"  SF{i+1} (REPLACED): Using stored sardine sorted position: {[f'{x:.3f}' for x in sorted_pos]}")
        else:
            # Regular sailfish - use current sorted position
            sorted_pos = sorted(engine.sailfish_random_values[i])
            print(f"  SF{i+1}: Using current sorted position: {[f'{x:.3f}' for x in sorted_pos]}")
        sorted_sailfish_positions.append(sorted_pos)
    
    print()
    new_sailfish_positions: List[List[float]] = []
    for k in range(engine.n_sailfish):
        print(f"Updating SF{k+1}:")
        
        # Determine which position to use for updates
        if k in sailfish_using_sardine_positions:
            update_position = sailfish_using_sardine_positions[k]
            position_source = "STORED SARDINE SORTED"
        else:
            update_position = sorted_sailfish_positions[k]
            position_source = "CURRENT SORTED"
        
        print(f"Using {position_source} position: {[f'{x:.3f}' for x in update_position]}")
        print(f"Using λ_{k+1} = {engine.lambda_k_values[k]:.6f}")
        
        new_position = []
        for j in range(engine.problem_size):
            rand = round(random.random(), 3)
            elite_sf_fitness = engine.elite_sailfish_fitness_score
            injured_sardine_fitness = engine.injured_sardine_fitness_score
            # Base on the appropriate position (sardine sorted for replaced sailfish, current sorted for others)
            old_sailfish_j = update_position[j]
            avg_fitness = (elite_sf_fitness + injured_sardine_fitness) / 2
            bracket_term = (rand * avg_fitness) - old_sailfish_j
            lambda_term = engine.lambda_k_values[k] * bracket_term
            new_val = elite_sf_fitness - lambda_term
            new_position.append(new_val)
            print(f"  Pos[{j+1}]: {elite_sf_fitness} - {engine.lambda_k_values[k]:.6f} × (({rand:.3f} × ({elite_sf_fitness} + {injured_sardine_fitness})/2) - {old_sailfish_j:.3f})")
            print(f"         = {elite_sf_fitness} - {engine.lambda_k_values[k]:.6f} × (({rand:.3f} × {avg_fitness:.3f}) - {old_sailfish_j:.3f})")
            print(f"         = {elite_sf_fitness} - {engine.lambda_k_values[k]:.6f} × ({rand * avg_fitness:.6f} - {old_sailfish_j:.3f})")
            print(f"         = {elite_sf_fitness} - {engine.lambda_k_values[k]:.6f} × {bracket_term:.6f}")
            print(f"         = {elite_sf_fitness} - {lambda_term:.6f} = {new_val:.3f}")
        
        new_sailfish_positions.append(new_position)
        print(f"New position: {[f'{x:.3f}' for x in new_position]}")
        print()
    
    engine.sailfish_random_values = new_sailfish_positions
    print("All sailfish positions updated successfully!")
    
    # NEW: Clear the replacement position tracking after use (positions are now updated)
    if sailfish_using_sardine_positions:
        print("Replacement position tracking cleared - positions have been updated.")
        engine.sailfish_using_sardine_positions = {}


def calculate_ap_and_update_sardines(engine) -> None:
    print(f"\n" + "="*80)
    if engine.current_iteration == 0:
        print("7. CALCULATE AP AND UPDATE SARDINE POSITIONS (CORRECTED - USING FITNESS SCORES)")
    else:
        print(f"ITERATION {engine.current_iteration} - STEP 7: CALCULATE AP AND UPDATE SARDINE POSITIONS (CORRECTED - USING FITNESS SCORES)")
    print("="*80)
    if engine.n_sardines == 0:
        print("No sardines remaining in population. Skipping sardine position update.")
        return
    engine.AP = engine.A * (1 - (2 * (engine.current_iteration + 1) * engine.epsilon))
    print(f"Attack Power (AP) Calculation:")
    print(f"AP = A × (1 - (2 × (current_iteration + 1) × epsilon))")
    print(f"AP = {engine.A} × (1 - (2 × ({engine.current_iteration} + 1) × {engine.epsilon}))")
    print(f"AP = {engine.A} × (1 - (2 × {engine.current_iteration + 1} × {engine.epsilon}))")
    print(f"AP = {engine.A} × {1 - (2 * (engine.current_iteration + 1) * engine.epsilon):.6f}")
    print(f"AP = {engine.AP:.6f}")
    print()
    print("CORRECTED Sardine Position Update Formula:")
    print("S_i_location[j] = random[0,1] × (elite_sailfish_fitness_score - old_sardine + AP)")
    print()
    print("IMPORTANT: Using FITNESS SCORES instead of position values!")
    print()
    print("Using SORTED sardine positions (current values after any replacements) for updates:")
    sorted_sardine_positions = [sorted(pos) for pos in engine.sardine_random_values]
    for i, pos in enumerate(sorted_sardine_positions):
        print(f"  Sorted S{i+1}: {[f'{x:.3f}' for x in pos]}")
    print()
    if engine.AP >= 0.5:
        print(f"AP ({engine.AP:.6f}) >= 0.5: Update ALL sardine positions")
        update_all_sardines(engine)
    else:
        print(f"AP ({engine.AP:.6f}) < 0.5: Partial sardine update")
        update_partial_sardines(engine)


def update_all_sardines(engine) -> None:
    print("\nUpdating ALL sardines:")
    print("CORRECTED Sardine Position Update Formula:")
    print("S_i_location[j] = random[0,1] × (elite_sailfish_fitness_score - old_sardine + AP)")
    print()
    new_sardine_positions = []
    # Use SORTED sardine positions as base
    sorted_sardine_positions = [sorted(pos) for pos in engine.sardine_random_values]
    for i in range(engine.n_sardines):
        print(f"Updating S{i+1}:")
        print(f"Using SORTED position: {[f'{x:.3f}' for x in sorted_sardine_positions[i]]}")
        new_position = []
        for j in range(engine.problem_size):
            rand = round(random.random(), 3)
            elite_sf_fitness = engine.elite_sailfish_fitness_score
            old_sardine_j = sorted_sardine_positions[i][j]
            bracket_term = elite_sf_fitness - old_sardine_j + engine.AP
            new_val = rand * bracket_term
            new_position.append(new_val)
            print(f"  Pos[{j+1}]: {rand:.3f} × ({elite_sf_fitness} - {old_sardine_j:.3f} + {engine.AP:.6f})")
            print(f"         = {rand:.3f} × {bracket_term:.6f} = {new_val:.3f}")
        new_sardine_positions.append(new_position)
        print(f"New position: {[f'{x:.3f}' for x in new_position]}")
        print()
    engine.sardine_random_values = new_sardine_positions
    print("All sardine positions updated successfully!")


def update_partial_sardines(engine) -> None:
    print("\nPartial sardine update:")
    alpha = int(engine.n_sardines * engine.AP)
    beta = int(engine.problem_size * engine.AP)
    print(f"alpha = num_sardines × AP = {engine.n_sardines} × {engine.AP:.6f} = {alpha}")
    print(f"beta = problem_size × AP = {engine.problem_size} × {engine.AP:.6f} = {beta}")
    print()
    print(f"Will update {alpha} sardines with {beta} variables each")
    print()
    if alpha == 0 or beta == 0:
        print("Alpha or beta is 0, no sardines will be updated.")
        return
    sardines_to_update = random.sample(range(engine.n_sardines), min(alpha, engine.n_sardines))
    print(f"Selected sardines to update: {[f'S{i+1}' for i in sardines_to_update]}")
    print()
    # Use SORTED sardine positions as base
    sorted_sardine_positions = [sorted(pos) for pos in engine.sardine_random_values]
    for i in sardines_to_update:
        print(f"Updating S{i+1} (partial):")
        print(f"Using SORTED position: {[f'{x:.3f}' for x in sorted_sardine_positions[i]]}")
        positions_to_update = random.sample(range(engine.problem_size), min(beta, engine.problem_size))
        print(f"Updating positions: {[j+1 for j in positions_to_update]}")
        new_position = sorted_sardine_positions[i].copy()
        for j in positions_to_update:
            rand = round(random.random(), 3)
            elite_sf_fitness = engine.elite_sailfish_fitness_score
            old_sardine_j = sorted_sardine_positions[i][j]
            bracket_term = elite_sf_fitness - old_sardine_j + engine.AP
            new_val = rand * bracket_term
            new_val = max(0, min(1, new_val))
            new_val = round(new_val, 3)
            new_position[j] = new_val
            print(f"  Pos[{j+1}]: {rand:.3f} × ({elite_sf_fitness} - {old_sardine_j:.3f} + {engine.AP:.6f})")
            print(f"         = {rand:.3f} × {bracket_term:.6f} = {new_val:.3f}")
        engine.sardine_random_values[i] = new_position
        print(f"New position: {[f'{x:.3f}' for x in new_position]}")
        print()
    print(f"Partial sardine update completed! Updated {len(sardines_to_update)} sardines.")



