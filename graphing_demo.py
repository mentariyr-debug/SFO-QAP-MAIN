#!/usr/bin/env python3
"""
Example script demonstrating the graphing capabilities of the Sailfish Optimization Algorithm.
This script shows how to use the new graphing features to visualize fitness scores and population dynamics.
"""

import sys
import os
from typing import List

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimizer import SailfishOptimizer
from io_utils import load_matrix_from_csv


def create_sample_matrices(size: int = 5) -> tuple[List[List[float]], List[List[float]]]:
    """Create sample frequency and distance matrices for testing."""
    import random
    
    # Set seed for reproducible results
    random.seed(42)
    
    # Create frequency matrix (facility-to-facility flow)
    freq_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0.0)  # No flow from facility to itself
            else:
                row.append(round(random.uniform(1, 10), 2))
        freq_matrix.append(row)
    
    # Create distance matrix (location-to-location distance)
    distance_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0.0)  # No distance from location to itself
            else:
                row.append(round(random.uniform(1, 20), 2))
        distance_matrix.append(row)
    
    return freq_matrix, distance_matrix


def main():
    """Main function to demonstrate the graphing capabilities."""
    print("="*80)
    print("SAILFISH OPTIMIZATION ALGORITHM - GRAPHING DEMONSTRATION")
    print("="*80)
    
    # Create sample matrices
    print("Creating sample frequency and distance matrices...")
    freq_matrix, distance_matrix = create_sample_matrices(5)
    
    print(f"Frequency matrix size: {len(freq_matrix)}x{len(freq_matrix[0])}")
    print(f"Distance matrix size: {len(distance_matrix)}x{len(distance_matrix[0])}")
    
    # Initialize the optimizer with graphing enabled
    print("\nInitializing Sailfish Optimizer with graphing enabled...")
    optimizer = SailfishOptimizer(
        n_sailfish=3,
        n_sardines=8,
        freq_matrix=freq_matrix,
        distance_matrix=distance_matrix,
        max_iter=20,  # Reduced iterations for demo
        A=4.0,
        epsilon=0.001,
        log_to_file=False,  # Disable file logging for cleaner demo
        enable_graphing=True  # Enable graphing
    )
    
    print("Graphing is ENABLED - plots will be generated automatically!")
    print("="*80)
    
    # Run the optimization
    print("Starting optimization...")
    optimizer.run_optimization()
    
    # The plots should be generated automatically at the end
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETED")
    print("="*80)
    print("The following plots should have been generated:")
    print("1. Fitness Evolution Plot - Shows best fitness, averages, and ranges")
    print("2. Population Dynamics Plot - Shows population sizes and ratios")
    print("3. Individual Fitness Plot - Shows individual fish fitness values")
    print("4. Summary Statistics Plot - Shows convergence, efficiency, and diversity")
    print("\nYou can also generate plots manually using:")
    print("- optimizer.create_fitness_plot()")
    print("- optimizer.create_population_plot()")
    print("- optimizer.generate_optimization_plots()")


if __name__ == "__main__":
    main()
