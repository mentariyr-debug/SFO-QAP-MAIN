"""
Graphing module for Sailfish Optimization Algorithm.
Provides visualization capabilities for tracking fitness scores and population dynamics.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Optional, Tuple
import numpy as np


class OptimizationTracker:
    """Tracks optimization metrics for visualization."""
    
    def __init__(self):
        self.iterations: List[int] = []
        self.best_fitness_history: List[float] = []
        self.sailfish_fitness_history: List[List[float]] = []
        self.sardine_fitness_history: List[List[float]] = []
        self.sailfish_population_history: List[int] = []
        self.sardine_population_history: List[int] = []
        self.avg_sailfish_fitness_history: List[float] = []
        self.avg_sardine_fitness_history: List[float] = []
        self.worst_sailfish_fitness_history: List[float] = []
        self.worst_sardine_fitness_history: List[float] = []
    
    def record_iteration(self, iteration: int, engine) -> None:
        """Record metrics for the current iteration."""
        self.iterations.append(iteration)
        self.best_fitness_history.append(engine.best_fitness)
        
        # Record sailfish metrics
        if engine.sailfish_fitness:
            self.sailfish_fitness_history.append(engine.sailfish_fitness.copy())
            self.sailfish_population_history.append(engine.n_sailfish)
            self.avg_sailfish_fitness_history.append(sum(engine.sailfish_fitness) / len(engine.sailfish_fitness))
            self.worst_sailfish_fitness_history.append(max(engine.sailfish_fitness))
        else:
            self.sailfish_fitness_history.append([])
            self.sailfish_population_history.append(0)
            self.avg_sailfish_fitness_history.append(0)
            self.worst_sailfish_fitness_history.append(0)
        
        # Record sardine metrics
        if engine.sardine_fitness:
            self.sardine_fitness_history.append(engine.sardine_fitness.copy())
            self.sardine_population_history.append(engine.n_sardines)
            self.avg_sardine_fitness_history.append(sum(engine.sardine_fitness) / len(engine.sardine_fitness))
            self.worst_sardine_fitness_history.append(max(engine.sardine_fitness))
        else:
            self.sardine_fitness_history.append([])
            self.sardine_population_history.append(0)
            self.avg_sardine_fitness_history.append(0)
            self.worst_sardine_fitness_history.append(0)


def create_fitness_evolution_plot(tracker: OptimizationTracker, save_path: Optional[str] = None) -> None:
    """Create a comprehensive fitness evolution plot."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Sailfish Optimization Algorithm - Fitness Evolution', fontsize=16, fontweight='bold')
    
    # Plot 1: Best fitness over iterations
    ax1.plot(tracker.iterations, tracker.best_fitness_history, 'b-', linewidth=2, marker='o', markersize=4)
    ax1.set_title('Best Fitness Evolution', fontweight='bold')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Best Fitness')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Plot 2: Average fitness comparison
    ax2.plot(tracker.iterations, tracker.avg_sailfish_fitness_history, 'r-', linewidth=2, marker='s', markersize=4, label='Sailfish Avg')
    ax2.plot(tracker.iterations, tracker.avg_sardine_fitness_history, 'g-', linewidth=2, marker='^', markersize=4, label='Sardine Avg')
    ax2.set_title('Average Fitness Comparison', fontweight='bold')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Average Fitness')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    # Plot 3: Population dynamics
    ax3.plot(tracker.iterations, tracker.sailfish_population_history, 'r-', linewidth=2, marker='s', markersize=4, label='Sailfish')
    ax3.plot(tracker.iterations, tracker.sardine_population_history, 'g-', linewidth=2, marker='^', markersize=4, label='Sardines')
    ax3.set_title('Population Dynamics', fontweight='bold')
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('Population Size')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Fitness range (best vs worst)
    ax4.plot(tracker.iterations, tracker.best_fitness_history, 'b-', linewidth=2, marker='o', markersize=4, label='Best Overall')
    ax4.plot(tracker.iterations, tracker.worst_sailfish_fitness_history, 'r--', linewidth=1, marker='s', markersize=3, label='Worst Sailfish')
    ax4.plot(tracker.iterations, tracker.worst_sardine_fitness_history, 'g--', linewidth=1, marker='^', markersize=3, label='Worst Sardine')
    ax4.set_title('Fitness Range Analysis', fontweight='bold')
    ax4.set_xlabel('Iteration')
    ax4.set_ylabel('Fitness')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Fitness evolution plot saved to: {save_path}")
    
    plt.show()


def create_population_dynamics_plot(tracker: OptimizationTracker, save_path: Optional[str] = None) -> None:
    """Create a detailed population dynamics plot."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Population Dynamics Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Population sizes over time
    ax1.plot(tracker.iterations, tracker.sailfish_population_history, 'r-', linewidth=3, marker='s', markersize=6, label='Sailfish Population')
    ax1.plot(tracker.iterations, tracker.sardine_population_history, 'g-', linewidth=3, marker='^', markersize=6, label='Sardine Population')
    ax1.fill_between(tracker.iterations, tracker.sailfish_population_history, alpha=0.3, color='red')
    ax1.fill_between(tracker.iterations, tracker.sardine_population_history, alpha=0.3, color='green')
    ax1.set_title('Population Size Evolution', fontweight='bold')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Population Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Population ratio
    total_population = [sf + sar for sf, sar in zip(tracker.sailfish_population_history, tracker.sardine_population_history)]
    sailfish_ratio = [sf / total if total > 0 else 0 for sf, total in zip(tracker.sailfish_population_history, total_population)]
    sardine_ratio = [sar / total if total > 0 else 0 for sar, total in zip(tracker.sardine_population_history, total_population)]
    
    ax2.plot(tracker.iterations, sailfish_ratio, 'r-', linewidth=3, marker='s', markersize=6, label='Sailfish Ratio')
    ax2.plot(tracker.iterations, sardine_ratio, 'g-', linewidth=3, marker='^', markersize=6, label='Sardine Ratio')
    ax2.fill_between(tracker.iterations, sailfish_ratio, alpha=0.3, color='red')
    ax2.fill_between(tracker.iterations, sardine_ratio, alpha=0.3, color='green')
    ax2.set_title('Population Ratio Evolution', fontweight='bold')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Population Ratio')
    ax2.set_ylim(0, 1)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Population dynamics plot saved to: {save_path}")
    
    plt.show()


def create_individual_fitness_plot(tracker: OptimizationTracker, save_path: Optional[str] = None) -> None:
    """Create a plot showing individual fitness values for each fish."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Individual Fish Fitness Evolution', fontsize=16, fontweight='bold')
    
    # Plot sailfish individual fitness
    for i in range(len(tracker.iterations)):
        sailfish_fitness = tracker.sailfish_fitness_history[i]
        if sailfish_fitness:
            for j, fitness in enumerate(sailfish_fitness):
                ax1.scatter(tracker.iterations[i], fitness, alpha=0.6, s=20, c='red')
    
    ax1.set_title('Sailfish Individual Fitness Values', fontweight='bold')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Fitness')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Plot sardine individual fitness
    for i in range(len(tracker.iterations)):
        sardine_fitness = tracker.sardine_fitness_history[i]
        if sardine_fitness:
            for j, fitness in enumerate(sardine_fitness):
                ax2.scatter(tracker.iterations[i], fitness, alpha=0.6, s=20, c='green')
    
    ax2.set_title('Sardine Individual Fitness Values', fontweight='bold')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Fitness')
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Individual fitness plot saved to: {save_path}")
    
    plt.show()


def create_summary_statistics_plot(tracker: OptimizationTracker, save_path: Optional[str] = None) -> None:
    """Create a summary statistics plot with key metrics."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Optimization Summary Statistics', fontsize=16, fontweight='bold')
    
    # Plot 1: Convergence analysis
    if len(tracker.best_fitness_history) > 1:
        improvement_rate = []
        for i in range(1, len(tracker.best_fitness_history)):
            improvement = (tracker.best_fitness_history[i-1] - tracker.best_fitness_history[i]) / tracker.best_fitness_history[i-1] * 100
            improvement_rate.append(improvement)
        
        ax1.plot(tracker.iterations[1:], improvement_rate, 'b-', linewidth=2, marker='o', markersize=4)
        ax1.set_title('Improvement Rate (%)', fontweight='bold')
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Improvement Rate (%)')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    # Plot 2: Population efficiency (fitness per individual)
    sailfish_efficiency = [avg_fit / pop if pop > 0 else 0 for avg_fit, pop in zip(tracker.avg_sailfish_fitness_history, tracker.sailfish_population_history)]
    sardine_efficiency = [avg_fit / pop if pop > 0 else 0 for avg_fit, pop in zip(tracker.avg_sardine_fitness_history, tracker.sardine_population_history)]
    
    ax2.plot(tracker.iterations, sailfish_efficiency, 'r-', linewidth=2, marker='s', markersize=4, label='Sailfish Efficiency')
    ax2.plot(tracker.iterations, sardine_efficiency, 'g-', linewidth=2, marker='^', markersize=4, label='Sardine Efficiency')
    ax2.set_title('Population Efficiency (Avg Fitness / Population)', fontweight='bold')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Efficiency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Fitness diversity (standard deviation)
    sailfish_diversity = []
    sardine_diversity = []
    
    for i in range(len(tracker.iterations)):
        if tracker.sailfish_fitness_history[i]:
            sailfish_diversity.append(np.std(tracker.sailfish_fitness_history[i]))
        else:
            sailfish_diversity.append(0)
        
        if tracker.sardine_fitness_history[i]:
            sardine_diversity.append(np.std(tracker.sardine_fitness_history[i]))
        else:
            sardine_diversity.append(0)
    
    ax3.plot(tracker.iterations, sailfish_diversity, 'r-', linewidth=2, marker='s', markersize=4, label='Sailfish Diversity')
    ax3.plot(tracker.iterations, sardine_diversity, 'g-', linewidth=2, marker='^', markersize=4, label='Sardine Diversity')
    ax3.set_title('Fitness Diversity (Standard Deviation)', fontweight='bold')
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('Fitness Standard Deviation')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Total population and best fitness
    total_population = [sf + sar for sf, sar in zip(tracker.sailfish_population_history, tracker.sardine_population_history)]
    
    ax4_twin = ax4.twinx()
    line1 = ax4.plot(tracker.iterations, total_population, 'purple', linewidth=2, marker='o', markersize=4, label='Total Population')
    line2 = ax4_twin.plot(tracker.iterations, tracker.best_fitness_history, 'orange', linewidth=2, marker='s', markersize=4, label='Best Fitness')
    
    ax4.set_title('Total Population vs Best Fitness', fontweight='bold')
    ax4.set_xlabel('Iteration')
    ax4.set_ylabel('Total Population', color='purple')
    ax4_twin.set_ylabel('Best Fitness', color='orange')
    ax4.grid(True, alpha=0.3)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Summary statistics plot saved to: {save_path}")
    
    plt.show()


def generate_all_plots(tracker: OptimizationTracker, base_filename: str = "sailfish_optimization") -> None:
    """Generate all available plots and save them."""
    print("\n" + "="*80)
    print("GENERATING OPTIMIZATION VISUALIZATION PLOTS")
    print("="*80)
    
    # Create fitness evolution plot
    create_fitness_evolution_plot(tracker, f"{base_filename}_fitness_evolution.png")
    
    # Create population dynamics plot
    create_population_dynamics_plot(tracker, f"{base_filename}_population_dynamics.png")
    
    # Create individual fitness plot
    create_individual_fitness_plot(tracker, f"{base_filename}_individual_fitness.png")
    
    # Create summary statistics plot
    create_summary_statistics_plot(tracker, f"{base_filename}_summary_statistics.png")
    
    print(f"\nAll plots have been generated and saved with base filename: {base_filename}")
    print("="*80)
