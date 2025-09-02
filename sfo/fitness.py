from typing import List
from qap_core import calculate_qap_fitness


def calculate_detailed_fitness(engine) -> None:
    print("\n" + "="*80)
    if engine.current_iteration == 0:
        print("4. DETAILED FITNESS CALCULATION FOR EACH INDIVIDUAL")
    else:
        print(f"ITERATION {engine.current_iteration} - STEP 2: DETAILED FITNESS CALCULATION")
    print("="*80)
    engine.sailfish_fitness = []
    engine.sardine_fitness = []
    print("SAILFISH Fitness Calculations:")
    print("=" * 50)
    for i, solution in enumerate(engine.sailfish_solutions):
        print(f"\nFISH CALCULATING FITNESS FOR SAILFISH SF{i+1}")
        fitness = calculate_qap_fitness(solution, engine.freq_matrix, engine.distance_matrix, show_details=True)
        engine.sailfish_fitness.append(fitness)
        if fitness < engine.best_fitness:
            engine.best_fitness = fitness
            engine.best_solution = solution.copy()
            print(f"     NEW BEST SOLUTION! Fitness: {fitness}")
    print("\n" + "=" * 50)
    print("SARDINE Fitness Calculations:")
    print("=" * 50)
    for i, solution in enumerate(engine.sardine_solutions):
        print(f"\nFISH CALCULATING FITNESS FOR SARDINE S{i+1}")
        fitness = calculate_qap_fitness(solution, engine.freq_matrix, engine.distance_matrix, show_details=True)
        engine.sardine_fitness.append(fitness)
        if fitness < engine.best_sardine_fitness:
            engine.best_sardine_fitness = fitness
        if fitness < engine.best_fitness:
            engine.best_fitness = fitness
            engine.best_solution = solution.copy()
            print(f"     NEW BEST SOLUTION! Fitness: {fitness}")


def print_fitness_summary(engine) -> None:
    print(f"\n" + "="*80)
    if engine.current_iteration == 0:
        print("FITNESS SUMMARY")
    else:
        print(f"ITERATION {engine.current_iteration} - STEP 3: FITNESS SUMMARY")
    print("="*80)
    print("SAILFISH FITNESS SCORES:")
    print("-" * 30)
    for i, fitness in enumerate(engine.sailfish_fitness):
        marker = " STAR BEST" if fitness == min(engine.sailfish_fitness) else ""
        print(f"SF{i+1}: {fitness}{marker}")
    print("\nSARDINE FITNESS SCORES:")
    print("-" * 25)
    for i, fitness in enumerate(engine.sardine_fitness):
        marker = " STAR BEST" if fitness == min(engine.sardine_fitness) else ""
        print(f"S{i+1}: {fitness}{marker}")
    print(f"\nOVERALL SUMMARY:")
    print("-" * 20)
    print(f"Best Sailfish Fitness: {min(engine.sailfish_fitness)}")
    print(f"Best Sardine Fitness: {min(engine.sardine_fitness)}")
    print(f"Overall Best Fitness: {engine.best_fitness}")
    print(f"Best Solution: {engine.best_solution}")
    engine.elite_sailfish_fitness_score = min(engine.sailfish_fitness)
    if engine.sardine_fitness:
        engine.injured_sardine_fitness_score = min(engine.sardine_fitness)
    else:
        engine.injured_sardine_fitness_score = engine.elite_sailfish_fitness_score
    print(f"\nFITNESS SCORES FOR POSITION UPDATES:")
    print(f"- Elite Sailfish Fitness Score: {engine.elite_sailfish_fitness_score}")
    print(f"- Injured Sardine Fitness Score: {engine.injured_sardine_fitness_score}")



