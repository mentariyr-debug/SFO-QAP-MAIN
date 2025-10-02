from typing import List, Tuple


def get_default_matrices() -> Tuple[List[List[float]], List[List[float]]]:
    """Return the default matrices from the problem."""
    freq_matrix = [
        [0, 60, 50, 10],
        [60, 0, 30, 20],  
        [50, 30, 0, 50],
        [10, 20, 50, 0]
    ]
    
    distance_matrix = [
        [0, 1, 2, 3],
        [1, 0, 4, 5],
        [2, 4, 0, 6], 
        [3, 5, 6, 0]
    ]
    
    return freq_matrix, distance_matrix


def calculate_qap_fitness(
    permutation: List[int],
    freq_matrix: List[List[float]],
    distance_matrix: List[List[float]],
    show_details: bool = False,
) -> float:
    """
    Calculate the Quadratic Assignment Problem (QAP) fitness value.
    """
    n = len(permutation)
    assignment_matrix: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]
    for location in range(n):
        facility = permutation[location] - 1
        assignment_matrix[facility][location] = 1
    non_zero_positions: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(n):
            if assignment_matrix[i][j] == 1:
                non_zero_positions.append((i, j))
    total_cost: float = 0
    calculation_details: List[dict] = []
    if show_details:
        print(f"\n" + "="*80)
        print(f"DETAILED QAP CALCULATION FOR PERMUTATION {permutation}")
        print("="*80)
        print_assignment_matrix(permutation)
        print("="*80)
    for i, (facility_i, location_j) in enumerate(non_zero_positions):
        if show_details:
            print(f"\nLoop {i+1} - x{facility_i+1}{location_j+1} with all other non-zero positions:")
        loop_total = 0
        for k, (facility_k, location_l) in enumerate(non_zero_positions):
            freq_ik = freq_matrix[facility_i][facility_k]
            dist_jl = distance_matrix[location_j][location_l]
            term_value = freq_ik * dist_jl
            if show_details:
                print(f"  x{facility_i+1}{location_j+1} × x{facility_k+1}{location_l+1} × f{facility_i+1}{facility_k+1} × d{location_j+1}{location_l+1} = (1)(1)({freq_ik})({dist_jl}) = {term_value}")
            calculation_details.append({
                'x_ij': f'x{facility_i+1}{location_j+1}',
                'x_kl': f'x{facility_k+1}{location_l+1}',
                'f_ik': freq_ik,
                'd_jl': dist_jl,
                'value': term_value
            })
            loop_total += term_value
            total_cost += term_value
        if show_details:
            print(f"  Loop {i+1} subtotal: {loop_total}")
    if show_details:
        print(f"\n" + "="*80)
        print(f"CALCULATION SUMMARY:")
        print("="*80)
        print(f"All terms: {' + '.join([str(detail['value']) for detail in calculation_details])}")
        print(f"TOTAL COST = {total_cost}")
        print("="*80)
    return total_cost


def print_assignment_matrix(permutation: List[int]) -> None:
    """Print the assignment matrix for visualization."""
    n = len(permutation)
    assignment_matrix: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]
    for location in range(n):
        facility = permutation[location] - 1
        assignment_matrix[facility][location] = 1
    print("\nAssignment Matrix:")
    print("Facilities\\Locations ", end="")
    for j in range(n):
        print(f"{j+1:2}", end=" ")
    print()
    for i in range(n):
        print(f"Facility {i+1}        ( ", end="")
        for j in range(n):
            print(f"{assignment_matrix[i][j]:2}", end=" ")
        print(")")
    print(f"\nPermutation {permutation} interpretation:")
    for location in range(n):
        facility = permutation[location]
        print(f"  Location {location+1} → Facility {facility}")


def print_matrices(freq_matrix: List[List[float]], distance_matrix: List[List[float]]) -> None:
    """Print the frequency and distance matrices in a clear, readable format."""
    n = len(freq_matrix)
    
    print("\n📊 FREQUENCY MATRIX (Flow between facilities)")
    print("=" * 60)
    print("    ", end="")
    for j in range(n):
        print(f"F{j+1:>6}", end="")
    print()
    print("    " + "-" * (7 * n))
    
    for i in range(n):
        print(f"F{i+1} |", end="")
        for j in range(n):
            if freq_matrix[i][j] == int(freq_matrix[i][j]):
                print(f"{int(freq_matrix[i][j]):>6}", end="")
            else:
                print(f"{freq_matrix[i][j]:>6.1f}", end="")
        print()
    
    print("\n📍 DISTANCE MATRIX (Distance between locations)")
    print("=" * 60)
    print("    ", end="")
    for j in range(n):
        print(f"L{j+1:>6}", end="")
    print()
    print("    " + "-" * (7 * n))
    
    for i in range(n):
        print(f"L{i+1} |", end="")
        for j in range(n):
            if distance_matrix[i][j] == int(distance_matrix[i][j]):
                print(f"{int(distance_matrix[i][j]):>6}", end="")
            else:
                print(f"{distance_matrix[i][j]:>6.1f}", end="")
        print()
    
    print("\n💡 Matrix Interpretation:")
    print("   • Frequency Matrix: Shows interaction frequency between facilities")
    print("   • Distance Matrix: Shows physical distances between locations")
    print("   • Goal: Minimize total cost = Σ(frequency × distance) for all pairs")


__all__ = [
    "get_default_matrices",
    "calculate_qap_fitness",
    "print_assignment_matrix",
    "print_matrices",
]



