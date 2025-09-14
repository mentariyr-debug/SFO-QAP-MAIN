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
    
    # Add conclusion explanation
    print("\n" + "="*100)
    print("CONCLUSION AND ANALYSIS")
    print("="*100)
    print("The Sailfish Optimizer algorithm has successfully completed the optimization process.")
    print("The algorithm utilized a population-based metaheuristic approach inspired by the")
    print("hunting behavior of sailfish and sardines in nature.")
    print()
    print("Key Findings:")
    print(f"• The most optimal facility assignment found is: {engine.best_solution}")
    print(f"• This assignment achieves a total cost of: {engine.best_fitness}")
    print(f"• The algorithm explored {len(engine.fitness_history)} iterations")
    print(f"• Starting with {engine.original_n_sailfish} sailfish and {engine.original_n_sardines} sardines")
    print(f"• Final population: {engine.n_sailfish} sailfish and {engine.n_sardines} sardines")
    print()
    print("Algorithm Performance:")
    if engine.fitness_history[0] > 0:
        improvement_pct = ((engine.fitness_history[0] - engine.fitness_history[-1]) / engine.fitness_history[0] * 100)
        print(f"• Achieved {improvement_pct:.2f}% improvement from initial to final solution")
    print(f"• Total cost reduction: {engine.fitness_history[0] - engine.fitness_history[-1]}")
    print()
    print("The optimal solution represents the best possible arrangement of facilities")
    print("to minimize the total transportation cost, considering both the frequency")
    print("of interactions between facilities and the distances between locations.")
    print()
    print("MOST OPTIMAL ARRAY:")
    print(f"Facility Assignment: {engine.best_solution}")
    print("This array indicates which facility should be placed at each location:")
    for i, facility in enumerate(engine.best_solution):
        print(f"  Location {i+1} → Facility {facility}")
    print()
    print("="*100)
    print("OPTIMIZATION COMPLETED SUCCESSFULLY!")
    print("Algorithm ran for all requested iterations without convergence checking.")
    print("="*100)


def report_sardine_population_extinction(engine, iteration_when_extinct: int) -> None:
    """
    Reports when the sardine population reaches 0, providing detailed analysis
    of the extinction event and its implications for the optimization process.
    
    Args:
        engine: The SailfishOptimizer instance
        iteration_when_extinct: The iteration number when sardines reached 0
    """
    print(f"\n" + "="*100)
    print("🚨 SARDINE POPULATION EXTINCTION EVENT 🚨")
    print("="*100)
    print(f"CRITICAL EVENT: All sardines have been eliminated from the population!")
    print(f"Extinction occurred at: ITERATION {iteration_when_extinct}")
    print()
    
    print("📊 EXTINCTION ANALYSIS:")
    print("-" * 50)
    print(f"• Initial sardine population: {engine.original_n_sardines}")
    print(f"• Final sardine population: {engine.n_sardines}")
    print(f"• Total sardines eliminated: {engine.original_n_sardines}")
    print(f"• Iterations survived: {iteration_when_extinct}")
    print(f"• Average elimination rate: {engine.original_n_sardines / iteration_when_extinct:.2f} sardines per iteration")
    print()
    
    print("🎯 OPTIMIZATION IMPACT:")
    print("-" * 50)
    print(f"• Current sailfish population: {engine.n_sailfish}")
    print(f"• Best solution found: {engine.best_solution}")
    print(f"• Best fitness achieved: {engine.best_fitness}")
    print(f"• Total iterations completed: {len(engine.fitness_history)}")
    print()
    
    if len(engine.fitness_history) > 1:
        print("📈 FITNESS EVOLUTION:")
        print("-" * 50)
        print(f"• Initial fitness: {engine.fitness_history[0]}")
        print(f"• Final fitness: {engine.fitness_history[-1]}")
        print(f"• Total improvement: {engine.fitness_history[0] - engine.fitness_history[-1]}")
        if engine.fitness_history[0] > 0:
            improvement_pct = ((engine.fitness_history[0] - engine.fitness_history[-1]) / engine.fitness_history[0] * 100)
            print(f"• Improvement percentage: {improvement_pct:.2f}%")
        print()
    
    print("🔍 EXTINCTION CAUSE ANALYSIS:")
    print("-" * 50)
    print("The sardine population extinction occurred due to the replacement mechanism")
    print("in the Sailfish Optimizer algorithm. This happens when:")
    print("• Sardines consistently find better solutions than the worst sailfish")
    print("• The replacement process promotes all sardines to sailfish status")
    print("• No new sardines are introduced to maintain population diversity")
    print()
    
    print("⚡ ALGORITHM BEHAVIOR AFTER EXTINCTION:")
    print("-" * 50)
    print("• Sardine position updates will be skipped (no sardines to update)")
    print("• Only sailfish will continue to evolve and search for solutions")
    print("• The algorithm will rely entirely on sailfish hunting strategies")
    print("• Population diversity is significantly reduced")
    print()
    
    print("🎯 RECOMMENDATIONS:")
    print("-" * 50)
    print("• Consider this a successful convergence event - all sardines became sailfish")
    print("• The algorithm has found a highly optimized solution space")
    print("• Further iterations will focus on fine-tuning sailfish positions")
    print("• This extinction indicates strong optimization performance")
    print()
    
    print("="*100)
    print("🔄 CONTINUING OPTIMIZATION WITH SAILFISH-ONLY POPULATION")
    print("="*100)


