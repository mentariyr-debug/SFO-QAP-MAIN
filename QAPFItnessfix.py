from typing import Tuple, List

from io_utils import DEFAULT_CSV_PATH, read_matrices_from_csv, NullWriter
from optimizer import SailfishOptimizer
import sys
import numpy as np


def main() -> None:
    """Main function to run the Sailfish Optimizer"""
    # Data size selection with validation
    while True:
        print("Select data size: [S]mall, [M]edium, [B]ig")
        size_choice = input().strip().lower()
        if size_choice in ['s', 'm', 'b']:
            break
        else:
            print("Please enter 'S', 'M', or 'B' for data size selection.")
    
    if size_choice == 's':
        csv_path = r"qap_matrices.csv"
    elif size_choice == 'm':
        csv_path = r"qap_matrices2.csv"
    elif size_choice == 'b':
        csv_path = r"qap_matrices3.csv"

    freq_matrix, distance_matrix = read_matrices_from_csv(csv_path)

    # Logging mode selection with validation
    while True:
        print("Log all process in the txt file? [Y/N]")
        log_choice = input().strip().lower()
        if log_choice in ['y', 'n']:
            full_log = log_choice == 'y'
            break
        else:
            print("Please enter 'Y' or 'N' for logging selection.")

    # Parameter customization selection with validation
    while True:
        print("Use default parameters or customize? [D]efault / [C]ustom")
        param_choice = input().strip().lower()
        if param_choice in ['d', 'c']:
            break
        else:
            print("Please enter 'D' for default or 'C' for custom parameters.")
    
    # Default parameters
    n_sailfish = 5
    n_sardines = 95
    max_iter = 100
    A = 4
    epsilon = 0.001
    
    if param_choice == 'c':
        print("Enter custom parameters:")
        
        # Get number of sailfish with validation
        while True:
            try:
                n_sailfish = int(input("Number of sailfish (default: 5): ").strip())
                if n_sailfish <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Get number of sardines with validation
        while True:
            try:
                n_sardines = int(input("Number of sardines (default: 95): ").strip())
                if n_sardines <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Get maximum iterations with validation
        while True:
            try:
                max_iter = int(input("Maximum iterations (default: 100): ").strip())
                if max_iter <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Get A parameter with validation
        while True:
            try:
                A = float(input("A parameter (default: 4.0): ").strip())
                if A <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Get epsilon parameter with validation
        while True:
            try:
                epsilon = float(input("Epsilon parameter (default: 0.001): ").strip())
                if epsilon <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"Using custom parameters: SF={n_sailfish}, SD={n_sardines}, MaxIter={max_iter}, A={A}, Epsilon={epsilon}")
    else:
        print("Using default parameters: SF=5, SD=95, MaxIter=100, A=4, Epsilon=0.001")

    optimizer = SailfishOptimizer(
        n_sailfish=n_sailfish,
        n_sardines=n_sardines,
        freq_matrix=freq_matrix,
        distance_matrix=distance_matrix,
        max_iter=max_iter,
        A=A,
        epsilon=epsilon,
        log_to_file=full_log,
    )

    if full_log:
        optimizer.run_optimization()
    else:
        original_stdout = sys.stdout
        sys.stdout = NullWriter()
        try:
            optimizer.run_optimization()
        finally:
            sys.stdout = original_stdout
        print(f"Best fitness: {optimizer.best_fitness}")


if __name__ == "__main__":
    main()



