import random
import sys
from datetime import datetime
from typing import List, Tuple, Optional

from io_utils import OutputLogger
from sfo.reporting import print_initial_parameters as _print_initial_parameters, print_comprehensive_results_table as _print_comprehensive_results_table, print_final_results as _print_final_results, report_sardine_population_extinction as _report_sardine_population_extinction
from sfo.population import print_random_populations as _print_random_populations, save_original_positions as _save_original_positions, print_sorted_arrays_and_solutions as _print_sorted_arrays_and_solutions
from sfo.fitness import calculate_detailed_fitness as _calculate_detailed_fitness, print_fitness_summary as _print_fitness_summary
from sfo.replacement import perform_sailfish_sardine_replacement as _perform_sailfish_sardine_replacement
from sfo.dynamics import calculate_pd_and_lambda_values as _calculate_pd_and_lambda_values, update_sailfish_positions as _update_sailfish_positions, calculate_ap_and_update_sardines as _calculate_ap_and_update_sardines
from sfo.graphing import OptimizationTracker


class SailfishOptimizer:
    def __init__(
        self,
        n_sailfish: int,
        n_sardines: int,
        freq_matrix: List[List[float]],
        distance_matrix: List[List[float]],
        max_iter: int = 100,
        A: float = 4,
        epsilon: float = 0.001,
        log_to_file: bool = True,
        enable_graphing: bool = True,
    ) -> None:
        if n_sardines <= n_sailfish:
            raise ValueError("Number of sardines must be greater than number of sailfish")
        self.original_n_sailfish: int = n_sailfish
        self.original_n_sardines: int = n_sardines
        self.n_sailfish: int = n_sailfish
        self.n_sardines: int = n_sardines
        self.freq_matrix: List[List[float]] = freq_matrix
        self.distance_matrix: List[List[float]] = distance_matrix
        self.max_iter: int = max_iter
        self.A: float = A
        self.epsilon: float = epsilon
        self.problem_size: int = len(freq_matrix)
        self.log_to_file: bool = log_to_file
        self.logger: Optional[OutputLogger] = None
        if log_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sailfish_output_SF{n_sailfish}_S{n_sardines}_{timestamp}.txt"
            self.logger = OutputLogger(filename)
            sys.stdout = self.logger
            print(f"Output will be logged to: {filename}")
            print(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Parameters: {n_sailfish} sailfish, {n_sardines} sardines, A={A}, epsilon={epsilon}")
            print(f"NOTE: Convergence checking is DISABLED - will run for full {max_iter} iterations")
            print("="*80 + "\n")
        self.sailfish_random_values: List[List[float]] = []
        self.sailfish_solutions: List[List[int]] = []
        self.sailfish_fitness: List[float] = []
        self.sardine_random_values: List[List[float]] = []
        self.sardine_solutions: List[List[int]] = []
        self.sardine_fitness: List[float] = []
        self.original_sailfish_positions: List[List[float]] = []
        self.original_sardine_positions: List[List[float]] = []
        self.best_solution: Optional[List[int]] = None
        self.best_fitness: float = float('inf')
        self.best_sardine_fitness: float = float('inf')
        self.fitness_history: List[float] = []
        self.elite_sailfish_fitness_score: Optional[float] = None
        self.injured_sardine_fitness_score: Optional[float] = None
        self.sf_elite: Optional[int] = None
        self.s_injured: Optional[int] = None
        self.lambda_k_values: List[float] = []
        self.PD: Optional[float] = None
        self.AP: Optional[float] = None
        self.current_iteration: int = 0
        # NEW: Track which sailfish should use sardine sorted positions for updates
        self.sailfish_using_sardine_positions: dict = {}
        # NEW: Graphing and tracking capabilities
        self.enable_graphing: bool = enable_graphing
        self.tracker: Optional[OptimizationTracker] = OptimizationTracker() if enable_graphing else None

    def __del__(self) -> None:
        if self.log_to_file and self.logger:
            print(f"\nRun completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*80)
            sys.stdout = self.logger.terminal
            self.logger.close()

    def save_original_positions(self) -> None:
        _save_original_positions(self)

    def print_initial_parameters(self) -> None:
        _print_initial_parameters(self)

    def generate_random_values(self, n_individuals: int) -> List[List[float]]:
        random_values: List[List[float]] = []
        for i in range(n_individuals):
            individual_values = [round(random.random(), 3) for _ in range(self.problem_size)]
            random_values.append(individual_values)
        return random_values

    def print_random_populations(self) -> None:
        _print_random_populations(self)

    def convert_random_to_solution(self, random_values: List[float]) -> Tuple[List[int], List[int]]:
        n = len(random_values)
        value_index_pairs: List[Tuple[float, int]] = [(random_values[i], i+1) for i in range(n)]
        sorted_pairs: List[Tuple[float, int]] = sorted(value_index_pairs)
        sorted_array = [pos for val, pos in sorted_pairs]
        solution = sorted_array.copy()
        return solution, sorted_array

    def print_sorted_arrays_and_solutions(self) -> None:
        _print_sorted_arrays_and_solutions(self)

    def calculate_detailed_fitness(self) -> None:
        _calculate_detailed_fitness(self)

    def print_fitness_summary(self) -> None:
        _print_fitness_summary(self)

    def perform_sailfish_sardine_replacement(self) -> None:
        _perform_sailfish_sardine_replacement(self)

    def print_comprehensive_results_table(self) -> None:
        _print_comprehensive_results_table(self)

    def calculate_pd_and_lambda_values(self) -> None:
        _calculate_pd_and_lambda_values(self)

    def update_sailfish_positions(self) -> None:
        _update_sailfish_positions(self)

    def calculate_ap_and_update_sardines(self) -> None:
        _calculate_ap_and_update_sardines(self)

    def update_all_sardines(self) -> None:
        from sfo.dynamics import update_all_sardines as __update_all
        __update_all(self)

    def update_partial_sardines(self) -> None:
        from sfo.dynamics import update_partial_sardines as __update_partial
        __update_partial(self)

    def run_iteration_zero(self) -> None:
        self.current_iteration = 0
        self.print_initial_parameters()
        self.print_random_populations()
        self.save_original_positions()
        self.print_sorted_arrays_and_solutions()
        self.calculate_detailed_fitness()
        self.print_fitness_summary()
        self.print_comprehensive_results_table()
        self.calculate_pd_and_lambda_values()
        self.update_sailfish_positions()
        self.calculate_ap_and_update_sardines()
        self.fitness_history.append(self.best_fitness)
        self.record_iteration_metrics()  # Record metrics for graphing
        print(f"\n" + "="*80)
        print("ITERATION 0 COMPLETED")
        print("="*80)
        print(f"Best fitness so far: {self.best_fitness}")
        print(f"Best solution: {self.best_solution}")
        print(f"Current populations: {self.n_sailfish} sailfish, {self.n_sardines} sardines")

    def run_iteration(self, iteration_num: int) -> None:
        self.current_iteration = iteration_num
        print(f"\n" + "="*100)
        print(f"STARTING ITERATION {iteration_num}")
        print("="*100)
        print("CRITICAL FIX: Saving original positions from previous iteration for position updates...")
        self.save_original_positions()
        self.print_sorted_arrays_and_solutions()
        self.calculate_detailed_fitness()
        self.print_fitness_summary()
        self.perform_sailfish_sardine_replacement()
        self.print_comprehensive_results_table()
        self.calculate_pd_and_lambda_values()
        self.update_sailfish_positions()
        self.calculate_ap_and_update_sardines()
        self.fitness_history.append(self.best_fitness)
        self.record_iteration_metrics()  # Record metrics for graphing
        print(f"\n" + "="*80)
        print(f"ITERATION {iteration_num} COMPLETED")
        print("="*80)
        print(f"Best fitness so far: {self.best_fitness}")
        print(f"Best solution: {self.best_solution}")
        print(f"Current populations: {self.n_sailfish} sailfish, {self.n_sardines} sardines")

    def run_optimization(self) -> None:
        print("STARTING SAILFISH OPTIMIZATION ALGORITHM (NO CONVERGENCE CHECK)")
        print("="*80)
        print("NOTE: Algorithm will run for the full number of specified iterations")
        print("regardless of improvement rate between iterations.")
        print()
        self.run_iteration_zero()
        for iteration in range(1, self.max_iter + 1):
            # Check if sardines were eliminated during the previous iteration
            if self.n_sardines == 0:
                print(f"\nNo sardines remaining after iteration {iteration-1}. Stopping optimization.")
                break
            self.run_iteration(iteration)
            # Check if sardines were eliminated during this iteration (after replacement)
            if self.n_sardines == 0:
                print(f"\nSardine population eliminated during iteration {iteration}. Stopping optimization.")
                break
        self.print_final_results()
        
        # Generate plots if graphing is enabled
        if self.enable_graphing and self.tracker:
            print(f"\n" + "="*80)
            print("GENERATING OPTIMIZATION VISUALIZATION PLOTS")
            print("="*80)
            self.generate_optimization_plots()

    def print_final_results(self) -> None:
        _print_final_results(self)

    def report_sardine_population_extinction(self, iteration_when_extinct: int) -> None:
        _report_sardine_population_extinction(self, iteration_when_extinct)
    
    def record_iteration_metrics(self) -> None:
        """Record metrics for the current iteration for graphing."""
        if self.enable_graphing and self.tracker:
            self.tracker.record_iteration(self.current_iteration, self)
    
    def generate_optimization_plots(self, base_filename: Optional[str] = None) -> None:
        """Generate all optimization visualization plots."""
        if not self.enable_graphing or not self.tracker:
            print("Graphing is disabled. Enable graphing during initialization to use this feature.")
            return
        
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"sailfish_optimization_SF{self.original_n_sailfish}_S{self.original_n_sardines}_{timestamp}"
        
        from sfo.graphing import generate_all_plots
        generate_all_plots(self.tracker, base_filename)
    
    def create_fitness_plot(self, save_path: Optional[str] = None) -> None:
        """Create fitness evolution plot."""
        if not self.enable_graphing or not self.tracker:
            print("Graphing is disabled. Enable graphing during initialization to use this feature.")
            return
        
        from sfo.graphing import create_fitness_evolution_plot
        create_fitness_evolution_plot(self.tracker, save_path)
    
    def create_population_plot(self, save_path: Optional[str] = None) -> None:
        """Create population dynamics plot."""
        if not self.enable_graphing or not self.tracker:
            print("Graphing is disabled. Enable graphing during initialization to use this feature.")
            return
        
        from sfo.graphing import create_population_dynamics_plot
        create_population_dynamics_plot(self.tracker, save_path)


__all__ = [
    "SailfishOptimizer",
]


