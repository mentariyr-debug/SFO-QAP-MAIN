from typing import List, Any
from qap_core import print_matrices


def print_terminal_data_info(engine) -> None:
    """Print data information for terminal output"""
    print("\n" + "="*60)
    print("📊 DATA INFORMATION")
    print("="*60)
    print(f"Data file: {getattr(engine, 'data_file', 'Unknown')}")
    print(f"Problem size: {engine.problem_size}x{engine.problem_size}")
    print()
    print("Frequency Matrix:")
    print_matrices(engine.freq_matrix, engine.distance_matrix)


def print_terminal_parameters(engine) -> None:
    """Print parameters for terminal output"""
    print("\n" + "="*60)
    print("⚙️ ALGORITHM PARAMETERS")
    print("="*60)
    print(f"Number of Sailfish: {engine.n_sailfish}")
    print(f"Number of Sardines: {engine.n_sardines}")
    print(f"Maximum Iterations: {engine.max_iter}")
    print(f"Parameter A: {engine.A}")
    print(f"Epsilon: {engine.epsilon}")
    print(f"Convergence Check: DISABLED")


def print_terminal_iteration_summary(engine, iteration: int) -> None:
    """Print iteration summary for terminal output"""
    print(f"\n🔄 ITERATION {iteration}")
    print("-" * 40)
    print(f"Best Fitness: {engine.best_fitness}")
    
    # Find which sailfish has the best solution
    best_sailfish = None
    for i, solution in enumerate(engine.sailfish_solutions):
        if solution == engine.best_solution:
            best_sailfish = i + 1
            break
    
    if best_sailfish:
        print(f"Best Solution by: Sailfish {best_sailfish}")
    else:
        # Check sardines if not found in sailfish
        for i, solution in enumerate(engine.sardine_solutions):
            if solution == engine.best_solution:
                print(f"Best Solution by: Sardine {i + 1}")
                break


def print_terminal_final_results(engine) -> None:
    """Print final results table for terminal output"""
    print("\n" + "="*80)
    print("📋 FINAL RESULTS TABLE")
    print("="*80)
    print(f"{'Iteration':<10} {'Best Fitness':<15} {'Best Solution':<20} {'Best Sailfish':<15}")
    print("-" * 80)
    
    for i, fitness in enumerate(engine.fitness_history):
        # Find which sailfish had the best solution at this iteration
        # For simplicity, we'll show the current best solution
        if i == len(engine.fitness_history) - 1:  # Last iteration
            best_sailfish = "Current"
            for j, solution in enumerate(engine.sailfish_solutions):
                if solution == engine.best_solution:
                    best_sailfish = f"SF{j+1}"
                    break
            if best_sailfish == "Current":
                for j, solution in enumerate(engine.sardine_solutions):
                    if solution == engine.best_solution:
                        best_sailfish = f"S{j+1}"
                        break
        else:
            best_sailfish = "N/A"
        
        solution_str = str(engine.best_solution) if engine.best_solution else "N/A"
        print(f"{i:<10} {fitness:<15} {solution_str:<20} {best_sailfish:<15}")
    
    print("-" * 80)
    print(f"Final Best Solution: {engine.best_solution}")
    print(f"Final Best Fitness: {engine.best_fitness}")
    print(f"Total Iterations: {len(engine.fitness_history)}")
    print("="*80)


def print_terminal_optimization_start(engine) -> None:
    """Print optimization start information for terminal"""
    print("\n" + "="*60)
    print("🚀 SAILFISH OPTIMIZATION STARTED")
    print("="*60)
    print("Running optimization with detailed logging to file...")
    print("Terminal will show summary information only.")
    print("="*60)
