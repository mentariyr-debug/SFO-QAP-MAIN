from typing import Tuple, List

from io_utils import DEFAULT_CSV_PATH, read_matrices_from_csv, NullWriter
from optimizer import SailfishOptimizer
import sys
import numpy as np


def main() -> None:
    """Main function to run the Sailfish Optimizer"""
    # Data size selection with validation
    print("DATA SIZE SELECTION")
    print("Choose the size of data to use for optimization:")
    print("1. Small data (kecil.csv) - 4 facilities")
    print("2. Medium data (sedang.csv) - 16 facilities")
    print("3. Big data (besar.csv) - 32 facilities")
    
    while True:
        size_choice = input("Enter your choice (1/2/3): ").strip()
        if size_choice in ['1', '2', '3']:
            break
        else:
            print("Please enter '1', '2', or '3' for data size selection.")
    
    if size_choice == '1':
        csv_path = r"kecil.csv"
    elif size_choice == '2':
        csv_path = r"sedang.csv"
    elif size_choice == '3':
        csv_path = r"besar.csv"

    freq_matrix, distance_matrix = read_matrices_from_csv(csv_path)

    # Logging mode selection with validation
    print("\n📝 LOGGING OPTIONS")
    print("Select output mode:")
    print("1. Steps to file, summary to terminal (recommended)")
    print("2. Summary only")
    
    while True:
        log_choice = input("Enter your choice (1/2): ").strip()
        if log_choice in ['1', '2']:
            full_log = log_choice == '1'
            break
        else:
            print("Please enter '1' or '2' for logging selection.")

    # Parameter customization selection with validation
    print("\n⚙️ PARAMETER CONFIGURATION")
    print("Select parameter mode:")
    print("1. Use default parameters")
    print("2. Customize parameters")
    
    while True:
        param_choice = input("Enter your choice (1/2): ").strip()
        if param_choice in ['1', '2']:
            break
        else:
            print("❌ Please enter '1' or '2' for parameter configuration.")
    
    # Fixed constants (cannot be changed)
    A = 4  # Constant value
    epsilon = 0.001  # Constant value
    
    # Default parameters
    n_sailfish = 5
    n_sardines = 95
    max_iter = 100
    
    if param_choice == '2':
        print("Enter custom parameters (A=4 and epsilon=0.001 are fixed constants):")
        
        # Get number of sailfish with validation
        while True:
            try:
                n_sailfish = int(input("Number of sailfish (default: 5): ").strip())
                if n_sailfish <= 0:
                    print("❌ Error: Number of sailfish must be a positive integer. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Error: Please enter a valid positive integer for sailfish count.")
        
        # Get number of sardines with validation
        while True:
            try:
                n_sardines = int(input("Number of sardines (default: 95): ").strip())
                if n_sardines <= 0:
                    print("❌ Error: Number of sardines must be a positive integer. Please try again.")
                    continue
                if n_sardines <= n_sailfish:
                    print("❌ Error: Number of sardines must be greater than number of sailfish (SF < SD). Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Error: Please enter a valid positive integer for sardine count.")
        
        # Get maximum iterations with validation
        while True:
            try:
                max_iter = int(input("Maximum iterations (default: 100): ").strip())
                if max_iter <= 0:
                    print("❌ Error: Maximum iterations must be a positive integer. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Error: Please enter a valid positive integer for maximum iterations.")
        
        print(f"✅ Using custom parameters: SF={n_sailfish}, SD={n_sardines}, MaxIter={max_iter}, A={A}, Epsilon={epsilon}")
    else:
        print(f"✅ Using default parameters: SF={n_sailfish}, SD={n_sardines}, MaxIter={max_iter}, A={A}, Epsilon={epsilon}")

    optimizer = SailfishOptimizer(
        n_sailfish=n_sailfish,
        n_sardines=n_sardines,
        freq_matrix=freq_matrix,
        distance_matrix=distance_matrix,
        max_iter=max_iter,
        A=A,
        epsilon=epsilon,
        log_to_file=full_log,
        dual_output=full_log,  # Enable dual output when logging to file
        data_file=csv_path,
    )

    if full_log:
        # Dual output mode - terminal shows summary, file gets detailed output
        optimizer.run_optimization()
    else:
        # Summary only mode - suppress all output except final result
        original_stdout = sys.stdout
        sys.stdout = NullWriter()
        try:
            optimizer.run_optimization()
        finally:
            sys.stdout = original_stdout
        print(f"Best fitness: {optimizer.best_fitness}")


if __name__ == "__main__":
    main()



