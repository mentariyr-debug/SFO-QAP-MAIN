from typing import List, Any
from qap_core import print_matrices


def print_header() -> None:
    """Print header with student information"""
    print("="*60)
    print("PENERAPAN SAILFISH OPTIMIZER ALGORITHM")
    print("(SFO) UNTUK MENYELESAIKAN QUADRATIC")
    print("ASSIGNMENT PROBLEM (QAP)")
    print()
    print("MENTARI YANI ROFANDI")
    print("082111233064")
    print("="*60)


def print_terminal_data_info(engine) -> None:
    """Print data information for terminal output"""
    print_header()
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
    print("\n" + "="*100)
    print("📋 FINAL RESULTS TABLE")
    print("="*100)
    
    # Print table header with better formatting
    print(f"{'Iteration':<12} {'Best Fitness':<18} {'Best Solution':<35} {'Best Agent':<15}")
    print("-" * 100)
    
    # Show only key iterations for terminal (first 5, last 5, and some middle ones)
    total_iterations = len(engine.fitness_history)
    if total_iterations <= 10:
        # Show all iterations if 10 or fewer
        iterations_to_show = list(range(total_iterations))
    else:
        # Show first 3, last 3, and some middle ones
        iterations_to_show = list(range(3))  # First 3
        middle_start = total_iterations // 2 - 1
        iterations_to_show.extend(range(middle_start, middle_start + 2))  # 2 middle
        iterations_to_show.extend(range(total_iterations - 3, total_iterations))  # Last 3
        iterations_to_show = sorted(set(iterations_to_show))
    
    prev_shown = -1
    for i in iterations_to_show:
        # Add ellipsis if there's a gap
        if i > prev_shown + 1:
            print(f"{'...':<12} {'...':<18} {'...':<35} {'...':<15}")
        
        fitness = engine.fitness_history[i]
        
        # Find which agent had the best solution at this iteration
        if i == len(engine.fitness_history) - 1:  # Last iteration
            best_agent = "Current"
            for j, solution in enumerate(engine.sailfish_solutions):
                if solution == engine.best_solution:
                    best_agent = f"SF{j+1}"
                    break
            if best_agent == "Current":
                for j, solution in enumerate(engine.sardine_solutions):
                    if solution == engine.best_solution:
                        best_agent = f"S{j+1}"
                        break
        else:
            best_agent = "N/A"
        
        # Format solution string (truncate if too long)
        solution_str = str(engine.best_solution) if engine.best_solution else "N/A"
        if len(solution_str) > 32:
            solution_str = solution_str[:29] + "..."
        
        print(f"{i:<12} {fitness:<18.2f} {solution_str:<35} {best_agent:<15}")
        prev_shown = i
    
    print("-" * 100)
    print(f"{'SUMMARY':<12}")
    print(f"{'Final Best Solution:':<20} {engine.best_solution}")
    print(f"{'Final Best Fitness:':<20} {engine.best_fitness:.2f}")
    print(f"{'Total Iterations:':<20} {len(engine.fitness_history)}")
    print(f"{'Algorithm:':<20} Sailfish Optimizer (SFO)")
    print("="*100)


def print_terminal_optimization_start(engine) -> None:
    """Print optimization start information for terminal"""
    print("\n" + "="*60)
    print("🚀 SAILFISH OPTIMIZATION STARTED")
    print("="*60)
    print("Running optimization with detailed logging to file...")
    print("Terminal will show summary information only.")
    print("="*60)

