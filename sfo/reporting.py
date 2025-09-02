from qap_core import print_matrices, calculate_qap_fitness


def print_initial_parameters(engine) -> None:
    print("\n" + "="*80)
    print("1. INITIAL VARIABLES AND QAP MATRICES")
    print("="*80)
    print(f"Initial Parameters:")
    print(f"- Problem size: {engine.problem_size}x{engine.problem_size}")
    print(f"- Sailfish population: {engine.n_sailfish}")
    print(f"- Sardine population: {engine.n_sardines}")
    print(f"- Total population: {engine.n_sailfish + engine.n_sardines}")
    print(f"- Maximum iterations: {engine.max_iter}")
    print(f"- Parameter A: {engine.A}")
    print(f"- Epsilon (for AP calculation): {engine.epsilon}")
    print(f"- Convergence checking: DISABLED")
    if engine.log_to_file:
        print(f"- Logging to file: ENABLED")
    print()
    print_matrices(engine.freq_matrix, engine.distance_matrix)


def print_comprehensive_results_table(engine) -> None:
    print(f"\n" + "="*120)
    if engine.current_iteration == 0:
        print("COMPREHENSIVE RESULTS TABLE")
    else:
        print(f"ITERATION {engine.current_iteration} - COMPREHENSIVE RESULTS TABLE")
    print("="*120)
    print(f"{'ID':<4} {'Random Values':<25} {'Sorted Array':<15} {'Solution':<15} {'Fitness':<8}")
    print("-" * 120)
    for i in range(engine.n_sailfish):
        random_vals = engine.sailfish_random_values[i]
        value_pos_pairs = [(random_vals[j], j+1) for j in range(len(random_vals))]
        sorted_pairs = sorted(value_pos_pairs)
        sorted_array = [pos for val, pos in sorted_pairs]
        random_str = str([f"{x:.3f}" for x in random_vals])
        solution_str = str(engine.sailfish_solutions[i])
        fitness = engine.sailfish_fitness[i]
        marker = "🎯" if engine.sailfish_solutions[i] == engine.best_solution else ""
        print(f"SF{i+1:<2} {random_str:<25} {str(sorted_array):<15} {solution_str:<15} {fitness:<8} {marker}")
    for i in range(engine.n_sardines):
        random_vals = engine.sardine_random_values[i]
        value_pos_pairs = [(random_vals[j], j+1) for j in range(len(random_vals))]
        sorted_pairs = sorted(value_pos_pairs)
        sorted_array = [pos for val, pos in sorted_pairs]
        random_str = str([f"{x:.3f}" for x in random_vals])
        solution_str = str(engine.sardine_solutions[i])
        fitness = engine.sardine_fitness[i]
        marker = "🎯" if engine.sardine_solutions[i] == engine.best_solution else ""
        print(f"S{i+1:<3} {random_str:<25} {str(sorted_array):<15} {solution_str:<15} {fitness:<8} {marker}")
    print(f"\nBest Overall Solution: {engine.best_solution} with fitness: {engine.best_fitness}")


def print_final_results(engine) -> None:
    print(f"\n" + "="*100)
    print("FINAL OPTIMIZATION RESULTS (NO CONVERGENCE CHECK VERSION)")
    print("="*100)
    print(f"Algorithm Parameters:")
    print(f"- Initial Sailfish: {engine.original_n_sailfish}")
    print(f"- Initial Sardines: {engine.original_n_sardines}")
    print(f"- Final Sailfish: {engine.n_sailfish}")
    print(f"- Final Sardines: {engine.n_sardines}")
    print(f"- Iterations Run: {len(engine.fitness_history)}")
    print(f"- Total Iterations Requested: {engine.max_iter}")
    print(f"- Parameter A: {engine.A}")
    print(f"- Epsilon (used in AP calculation): {engine.epsilon}")
    print(f"- Convergence Check: DISABLED")
    print()
    print(f"Best Solution Found:")
    print(f"- Solution: {engine.best_solution}")
    print(f"- Fitness: {engine.best_fitness}")
    print()
    if engine.best_solution:
        print("Detailed Best Solution Analysis:")
        calculate_qap_fitness(engine.best_solution, engine.freq_matrix, engine.distance_matrix, show_details=True)
    print(f"\nFitness Evolution:")
    print(f"- Initial fitness: {engine.fitness_history[0]}")
    print(f"- Final fitness: {engine.fitness_history[-1]}")
    print(f"- Total improvement: {engine.fitness_history[0] - engine.fitness_history[-1]}")
    if engine.fitness_history[0] > 0:
        print(f"- Improvement percentage: {((engine.fitness_history[0] - engine.fitness_history[-1]) / engine.fitness_history[0] * 100):.2f}%")
    print(f"\nFitness History: {engine.fitness_history}")
    print("\n" + "="*100)
    print("OPTIMIZATION COMPLETED SUCCESSFULLY!")
    print("Algorithm ran for all requested iterations without convergence checking.")
    print("="*100)


