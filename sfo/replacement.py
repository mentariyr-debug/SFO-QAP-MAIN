def perform_sailfish_sardine_replacement(engine) -> None:
    print(f"\n" + "="*80)
    print(f"ITERATION {engine.current_iteration} - STEP 4: SAILFISH-SARDINE REPLACEMENT")
    print("="*80)
    print("REPLACEMENT MECHANISM:")
    print("- Sardines with better fitness than any sailfish will replace the worst sailfish")
    print("- Replaced sardines are removed from sardine population")
    print("- No sailfish are demoted")
    print("- NEW: Replaced sailfish will use the sardine's sorted position for future updates")
    print()
    worst_sailfish_fitness = max(engine.sailfish_fitness)
    better_sardines = []
    for i, sardine_fitness in enumerate(engine.sardine_fitness):
        if sardine_fitness < worst_sailfish_fitness:
            better_sardines.append((i, sardine_fitness))
    print(f"Analysis:")
    print(f"- Worst sailfish fitness: {worst_sailfish_fitness}")
    print(f"- Sardines better than worst sailfish: {len(better_sardines)}")
    if not better_sardines:
        print("- No sardines are better than the worst sailfish")
        print("- No replacement will occur")
        return
    better_sardines.sort(key=lambda x: x[1])
    print(f"\nSardines eligible for replacement:")
    for sardine_idx, fitness in better_sardines:
        print(f"- S{sardine_idx+1}: fitness = {fitness}")
    sardines_to_remove = []
    replacements_made = []
    
    # NEW: Track which sailfish positions need to use sardine sorted positions
    sailfish_using_sardine_positions = {}
    
    for sardine_idx, sardine_fitness in better_sardines:
        worst_sf_idx = engine.sailfish_fitness.index(max(engine.sailfish_fitness))
        worst_sf_fitness = engine.sailfish_fitness[worst_sf_idx]
        if sardine_fitness < worst_sf_fitness:
            print(f"\nReplacement {len(replacements_made) + 1}:")
            print(f"- Sardine S{sardine_idx+1} (fitness: {sardine_fitness}) -> Sailfish SF{worst_sf_idx+1} (fitness: {worst_sf_fitness})")
            
            # Store the original sailfish data for reference
            old_sf_values = engine.sailfish_random_values[worst_sf_idx].copy()
            old_sf_solution = engine.sailfish_solutions[worst_sf_idx].copy()
            old_sf_fitness = engine.sailfish_fitness[worst_sf_idx]
            
            # Store the sardine's sorted position for future updates
            sardine_sorted_position = sorted(engine.sardine_random_values[sardine_idx])
            sailfish_using_sardine_positions[worst_sf_idx] = sardine_sorted_position
            
            # Perform the replacement
            engine.sailfish_random_values[worst_sf_idx] = engine.sardine_random_values[sardine_idx].copy()
            engine.sailfish_solutions[worst_sf_idx] = engine.sardine_solutions[sardine_idx].copy()
            engine.sailfish_fitness[worst_sf_idx] = engine.sardine_fitness[sardine_idx]
            
            print(f"  Old SF{worst_sf_idx+1}: values={old_sf_values}, solution={old_sf_solution}, fitness={old_sf_fitness}")
            print(f"  New SF{worst_sf_idx+1}: values={engine.sailfish_random_values[worst_sf_idx]}, solution={engine.sailfish_solutions[worst_sf_idx]}, fitness={engine.sailfish_fitness[worst_sf_idx]}")
            print(f"  NEW: SF{worst_sf_idx+1} will use sardine S{sardine_idx+1}'s sorted position for future updates: {[f'{x:.3f}' for x in sardine_sorted_position]}")
            
            sardines_to_remove.append(sardine_idx)
            replacements_made.append({
                'sardine_idx': sardine_idx,
                'sailfish_idx': worst_sf_idx,
                'new_fitness': sardine_fitness,
                'old_fitness': worst_sf_fitness,
                'sardine_sorted_position': sardine_sorted_position
            })
            
            if sardine_fitness < engine.best_fitness:
                engine.best_fitness = sardine_fitness
                engine.best_solution = engine.sardine_solutions[sardine_idx].copy()
                print(f"  NEW OVERALL BEST SOLUTION! Fitness: {sardine_fitness}")
        else:
            break
    
    # NEW: Store the replacement information in the engine for use in position updates
    if replacements_made:
        engine.sailfish_using_sardine_positions = sailfish_using_sardine_positions
        print(f"\nReplacement Position Tracking:")
        print("The following sailfish will use their original sardine sorted positions for future updates:")
        for sf_idx, sardine_pos in sailfish_using_sardine_positions.items():
            print(f"  SF{sf_idx+1}: Using sardine sorted position {[f'{x:.3f}' for x in sardine_pos]}")
    else:
        engine.sailfish_using_sardine_positions = {}
    
    sardines_to_remove.sort(reverse=True)
    print(f"\nRemoving replaced sardines from sardine population:")
    for sardine_idx in sardines_to_remove:
        print(f"- Removing S{sardine_idx+1} (now SF{[r['sailfish_idx']+1 for r in replacements_made if r['sardine_idx'] == sardine_idx][0]})")
        del engine.sardine_random_values[sardine_idx]
        del engine.sardine_solutions[sardine_idx]
        del engine.sardine_fitness[sardine_idx]
        del engine.original_sardine_positions[sardine_idx]
        engine.n_sardines -= 1
    
    print(f"\nReplacement Summary:")
    print(f"- Total replacements made: {len(replacements_made)}")
    print(f"- New sailfish population size: {engine.n_sailfish}")
    print(f"- New sardine population size: {engine.n_sardines}")
    
    if replacements_made:
        print(f"\nUpdated populations after replacement:")
        print("SAILFISH (after replacement):")
        for i in range(engine.n_sailfish):
            marker = " (NEW)" if any(r['sailfish_idx'] == i for r in replacements_made) else ""
            print(f"  SF{i+1}: fitness = {engine.sailfish_fitness[i]}{marker}")
        print("SARDINES (after removal):")
        for i in range(engine.n_sardines):
            print(f"  S{i+1}: fitness = {engine.sardine_fitness[i]}")
    
    engine.elite_sailfish_fitness_score = min(engine.sailfish_fitness)
    if engine.sardine_fitness:
        engine.injured_sardine_fitness_score = min(engine.sardine_fitness)
    else:
        engine.injured_sardine_fitness_score = engine.elite_sailfish_fitness_score



