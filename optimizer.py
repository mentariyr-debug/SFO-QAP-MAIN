import random
import sys
from datetime import datetime
from typing import List, Tuple, Optional

from io_utils import OutputLogger, DualOutputLogger
from terminal_output import print_terminal_data_info, print_terminal_parameters, print_terminal_iteration_summary, print_terminal_final_results, print_terminal_optimization_start
from sfo.reporting import print_initial_parameters as _print_initial_parameters, print_comprehensive_results_table as _print_comprehensive_results_table, print_final_results as _print_final_results, report_sardine_population_extinction as _report_sardine_population_extinction
from sfo.population import print_random_populations as _print_random_populations, save_original_positions as _save_original_positions, print_sorted_arrays_and_solutions as _print_sorted_arrays_and_solutions
from sfo.fitness import calculate_detailed_fitness as _calculate_detailed_fitness, print_fitness_summary as _print_fitness_summary
from sfo.replacement import perform_sailfish_sardine_replacement as _perform_sailfish_sardine_replacement
from sfo.dynamics import calculate_pd_and_lambda_values as _calculate_pd_and_lambda_values, update_sailfish_positions as _update_sailfish_positions, calculate_ap_and_update_sardines as _calculate_ap_and_update_sardines


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
        dual_output: bool = False,
        data_file: str = "Unknown",
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
        self.dual_output: bool = dual_output
        self.data_file: str = data_file
        self.logger: Optional[OutputLogger] = None
        self.dual_logger: Optional[DualOutputLogger] = None
        
        if dual_output:
            # Dual output mode - separate terminal and file output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sailfish_detailed_SF{n_sailfish}_S{n_sardines}_{timestamp}.txt"
            self.dual_logger = DualOutputLogger(filename)
            # Show terminal info only
            print_terminal_optimization_start(self)
            print_terminal_data_info(self)
            print_terminal_parameters(self)
            # Log detailed info to file
            self.dual_logger.write_to_file(f"Output will be logged to: {filename}\n")
            self.dual_logger.write_to_file(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.dual_logger.write_to_file(f"Parameters: {n_sailfish} sailfish, {n_sardines} sardines, A={A}, epsilon={epsilon}\n")
            self.dual_logger.write_to_file(f"NOTE: Convergence checking is DISABLED - will run for full {max_iter} iterations\n")
            self.dual_logger.write_to_file("="*80 + "\n\n")
            # Redirect all print statements to file only
            sys.stdout = self.dual_logger
        elif log_to_file:
            # Original single output mode
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

    def __del__(self) -> None:
        if self.dual_output and self.dual_logger:
            self.dual_logger.write_to_file(f"\nRun completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.dual_logger.write_to_file("="*80 + "\n")
            # Restore terminal output
            sys.stdout = self.dual_logger.terminal
            self.dual_logger.close()
        elif self.log_to_file and self.logger:
            print(f"\nRun completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*80)
            sys.stdout = self.logger.terminal
            self.logger.close()

    def _redirect_to_file(self, func, *args, **kwargs):
        """Helper function to redirect output to file in dual output mode"""
        if self.dual_output and self.dual_logger:
            # stdout is already redirected to dual_logger, just call the function
            func(*args, **kwargs)
        else:
            func(*args, **kwargs)

    def save_original_positions(self) -> None:
        self._redirect_to_file(_save_original_positions, self)

    def print_initial_parameters(self) -> None:
        self._redirect_to_file(_print_initial_parameters, self)

    def generate_random_values(self, n_individuals: int) -> List[List[float]]:
        random_values: List[List[float]] = []
        for i in range(n_individuals):
            individual_values = [round(random.random(), 3) for _ in range(self.problem_size)]
            random_values.append(individual_values)
        return random_values

    def print_random_populations(self) -> None:
        self._redirect_to_file(_print_random_populations, self)

    def convert_random_to_solution(self, random_values: List[float]) -> Tuple[List[int], List[int]]:
        n = len(random_values)
        value_index_pairs: List[Tuple[float, int]] = [(random_values[i], i+1) for i in range(n)]
        sorted_pairs: List[Tuple[float, int]] = sorted(value_index_pairs)
        sorted_array = [pos for val, pos in sorted_pairs]
        solution = sorted_array.copy()
        return solution, sorted_array

    def print_sorted_arrays_and_solutions(self) -> None:
        self._redirect_to_file(_print_sorted_arrays_and_solutions, self)

    def calculate_detailed_fitness(self) -> None:
        self._redirect_to_file(_calculate_detailed_fitness, self)

    def print_fitness_summary(self) -> None:
        self._redirect_to_file(_print_fitness_summary, self)

    def perform_sailfish_sardine_replacement(self) -> None:
        _perform_sailfish_sardine_replacement(self)

    def print_comprehensive_results_table(self) -> None:
        self._redirect_to_file(_print_comprehensive_results_table, self)

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
        
        # File output
        self._redirect_to_file(lambda: print(f"\n" + "="*80))
        self._redirect_to_file(lambda: print("ITERATION 0 COMPLETED"))
        self._redirect_to_file(lambda: print("="*80))
        self._redirect_to_file(lambda: print(f"Best fitness so far: {self.best_fitness}"))
        self._redirect_to_file(lambda: print(f"Best solution: {self.best_solution}"))
        self._redirect_to_file(lambda: print(f"Current populations: {self.n_sailfish} sailfish, {self.n_sardines} sardines"))
        
        # Terminal output
        if self.dual_output:
            # Restore terminal output temporarily for iteration summary
            original_stdout = sys.stdout
            sys.stdout = self.dual_logger.terminal
            print_terminal_iteration_summary(self, 0)
            sys.stdout = original_stdout

    def run_iteration(self, iteration_num: int) -> None:
        self.current_iteration = iteration_num
        
        # File output
        self._redirect_to_file(lambda: print(f"\n" + "="*100))
        self._redirect_to_file(lambda: print(f"STARTING ITERATION {iteration_num}"))
        self._redirect_to_file(lambda: print("="*100))
        self._redirect_to_file(lambda: print("CRITICAL FIX: Saving original positions from previous iteration for position updates..."))
        
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
        
        # File output
        self._redirect_to_file(lambda: print(f"\n" + "="*80))
        self._redirect_to_file(lambda: print(f"ITERATION {iteration_num} COMPLETED"))
        self._redirect_to_file(lambda: print("="*80))
        self._redirect_to_file(lambda: print(f"Best fitness so far: {self.best_fitness}"))
        self._redirect_to_file(lambda: print(f"Best solution: {self.best_solution}"))
        self._redirect_to_file(lambda: print(f"Current populations: {self.n_sailfish} sailfish, {self.n_sardines} sardines"))
        
        # Terminal output
        if self.dual_output:
            # Restore terminal output temporarily for iteration summary
            original_stdout = sys.stdout
            sys.stdout = self.dual_logger.terminal
            print_terminal_iteration_summary(self, iteration_num)
            sys.stdout = original_stdout

    def run_optimization(self) -> None:
        # File output
        self._redirect_to_file(lambda: print("STARTING SAILFISH OPTIMIZATION ALGORITHM (NO CONVERGENCE CHECK)"))
        self._redirect_to_file(lambda: print("="*80))
        self._redirect_to_file(lambda: print("NOTE: Algorithm will run for the full number of specified iterations"))
        self._redirect_to_file(lambda: print("regardless of improvement rate between iterations."))
        self._redirect_to_file(lambda: print())
        
        self.run_iteration_zero()
        for iteration in range(1, self.max_iter + 1):
            # Check if sardines were eliminated during the previous iteration
            if self.n_sardines == 0:
                self._redirect_to_file(lambda: print(f"\nNo sardines remaining after iteration {iteration-1}. Stopping optimization."))
                break
            self.run_iteration(iteration)
            # Check if sardines were eliminated during this iteration (after replacement)
            if self.n_sardines == 0:
                self._redirect_to_file(lambda: print(f"\nSardine population eliminated during iteration {iteration}. Stopping optimization."))
                break
        
        # Show final results
        if self.dual_output:
            # Restore terminal output temporarily for final results
            original_stdout = sys.stdout
            sys.stdout = self.dual_logger.terminal
            print_terminal_final_results(self)
            sys.stdout = original_stdout
        self.print_final_results()

    def print_final_results(self) -> None:
        self._redirect_to_file(_print_final_results, self)

    def report_sardine_population_extinction(self, iteration_when_extinct: int) -> None:
        _report_sardine_population_extinction(self, iteration_when_extinct)


__all__ = [
    "SailfishOptimizer",
]


