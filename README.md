### Solution Representation

#### Random Value to Permutation Conversion
1. **Generate random values**: `[0.8, 0.2, 0.9, 0.1]`
2. **Create value-index pairs**: `[(0.8,1), (0.2,2), (0.9,3), (0.1,4)]`
3. **Sort by values**: `[(0.1,4), (0.2,2), (0.8,1), (0.9,3)]`
4. **Extract indices**: `[4, 2, 1, 3]`
5. **Result**: Facility 4 → Location 1, Facility 2 → Location 2, etc.

### Replacement Position Tracking (NEW FEATURE)

#### Enhanced Replacement Logic
When a sailfish is replaced by a sardine, the system now tracks which sailfish should use the sardine's sorted position for future updates:

**Before (Old Behavior)**:
- Sardine S3 replaces sailfish SF2
- SF2 gets S3's current position and solution
- SF2 uses its own sorted position for future updates

**After (New Behavior)**:
- Sardine S3 replaces sailfish SF2
- SF2 gets S3's current position and solution
- **NEW**: SF2 uses S3's **sorted position** for future updates
- This ensures continuity in the optimization process

#### Implementation Details
```python
# In replacement.py
sardine_sorted_position = sorted(engine.sardine_random_values[sardine_idx])
sailfish_using_sardine_positions[worst_sf_idx] = sardine_sorted_position

# In dynamics.py - sailfish position updates
if k in sailfish_using_sardine_positions:
    # Use stored sardine sorted position
    update_position = sailfish_using_sardine_positions[k]
    position_source = "STORED SARDINE SORTED"
else:
    # Use current sorted position
    update_position = sorted_sailfish_positions[k]
    position_source = "CURRENT SORTED"
```

#### Benefits
1. **Position Continuity**: Replaced sailfish maintain their "genetic memory" from their sardine origins
2. **Better Convergence**: More stable position updates for recently replaced individuals
3. **Algorithm Integrity**: Preserves the optimization trajectory of successful sardines
4. **Debugging Support**: Clear tracking of which sailfish use which position sources

#### Example Scenario
```
Iteration 5: Sardine S3 (fitness: 1200) replaces sailfish SF2 (fitness: 1500)
- SF2 now has S3's position: [0.3, 0.7, 0.1, 0.6]
- SF2's stored sorted position: [0.1, 0.3, 0.6, 0.7] (from S3)

Iteration 6: SF2 position update
- Uses stored sorted position: [0.1, 0.3, 0.6, 0.7] (S3's sorted)
- NOT current sorted position: [0.1, 0.3, 0.6, 0.7] (current SF2)
- This ensures SF2 continues evolving from S3's optimization trajectory
```

## 🔧 Detailed Function Analysis & Relationships

### 📄 `QAPFItnessfix.py` - Main Program Controller

#### Function: `main()`
**Purpose**: Orchestrates the entire program execution flow
**Internal Workflow**:
1. **Data Size Selection Loop**: 
   - Prompts user for S/M/B choice
   - Validates input with `while True` loop
   - Maps choice to specific CSV file paths
   - No fallback to defaults - requires valid input

2. **Logging Selection Loop**:
   - Prompts for Y/N logging preference
   - Validates input with `while True` loop
   - Sets `full_log` boolean flag
   - No fallback - requires valid input

3. **Parameter Customization Loop**:
   - Prompts for D/C parameter choice
   - Validates input with `while True` loop
   - If custom: enters nested validation loops for each parameter
   - If default: uses predefined values

4. **Program Execution**:
   - Calls `read_matrices_from_csv()` from `io_utils.py`
   - Creates `SailfishOptimizer` instance with chosen parameters
   - Executes optimization with or without logging
   - Handles output redirection for silent mode

**Key Relationships**:
- **Input**: User choices via `input()` function
- **Output**: Creates `SailfishOptimizer` instance
- **Dependencies**: `io_utils.py`, `optimizer.py`
- **Data Flow**: User input → Parameter validation → Matrix loading → Optimizer creation → Execution

---

### 📄 `io_utils.py` - Input/Output Management

#### Class: `OutputLogger`
**Purpose**: Manages log file creation and output redirection
**Constructor**: `__init__(filename: str)`
- Creates timestamped log file
- Stores original `sys.stdout` reference
- Redirects all output to log file

**Methods**:
- `close()`: Restores original stdout and closes log file
- `write(text)`: Writes text to log file (implements file-like interface)

**Key Relationships**:
- **Used by**: `SailfishOptimizer` when `log_to_file=True`
- **Interacts with**: `sys.stdout` redirection
- **Output**: Creates timestamped log files like `sailfish_output_SF5_S95_20250102_084530.txt`

#### Class: `NullWriter`
**Purpose**: Discards all output (implements null device)
**Methods**:
- `write(text)`: Does nothing (discards output)
- `flush()`: No-op method for file-like interface compatibility

**Key Relationships**:
- **Used by**: `SailfishOptimizer` when `log_to_file=False`
- **Purpose**: Enables silent execution mode

#### Function: `read_matrices_from_csv(csv_path: str)`
**Purpose**: Loads frequency and distance matrices from CSV files
**Internal Workflow**:
1. **File Reading**: Opens CSV file and reads lines
2. **Data Parsing**: Converts comma-separated strings to float matrices
3. **Validation**: Ensures matrices are square and same dimensions
4. **Return**: Tuple of `(freq_matrix, distance_matrix)`

**Key Relationships**:
- **Input**: CSV file path string
- **Output**: Two 2D lists of floats
- **Used by**: `main()` function in `QAPFItnessfix.py`
- **Dependencies**: Built-in Python `open()`, `split()`, `float()`

---

### 📄 `qap_core.py` - QAP Problem Implementation

#### Function: `get_default_matrices()`
**Purpose**: Provides hardcoded 4×4 test matrices for demonstration
**Return Value**: Tuple of two 4×4 matrices
- **Frequency Matrix**: Flow between facilities (symmetric)
- **Distance Matrix**: Distance between locations (symmetric)

**Key Relationships**:
- **Used by**: Testing and demonstration purposes
- **Structure**: Fixed-size matrices for small problem instances

#### Function: `calculate_qap_fitness(permutation, freq_matrix, distance_matrix, show_details=False)`
**Purpose**: Calculates total cost for a given facility-to-location assignment
**Internal Algorithm**:
1. **Assignment Matrix Creation**:
   ```python
   # Convert permutation [3,1,4,2] to assignment matrix
   # Facility 3 → Location 1, Facility 1 → Location 2, etc.
   assignment_matrix[facility][location] = 1
   ```

2. **Non-zero Position Identification**:
   - Finds all (facility, location) pairs where assignment = 1
   - Creates list of active assignments

3. **Cost Calculation Loop**:
   ```python
   for each assignment (i,j):
       for each other assignment (k,l):
           cost += freq_matrix[i][k] * distance_matrix[j][l]
   ```

4. **Detailed Output** (if `show_details=True`):
   - Shows assignment matrix visualization
   - Displays step-by-step calculation
   - Provides intermediate results and final total

**Mathematical Foundation**:
- **QAP Formula**: `Σ(i,j) Σ(k,l) F[i][k] × D[j][l] × x[i][j] × x[k][l]`
- **Where**: x[i][j] = 1 if facility i assigned to location j, 0 otherwise

**Key Relationships**:
- **Input**: Permutation list, frequency matrix, distance matrix
- **Output**: Total cost (float)
- **Used by**: `SailfishOptimizer` for fitness evaluation
- **Performance**: O(n²) complexity for n×n matrices

#### Function: `print_assignment_matrix(permutation)`
**Purpose**: Visualizes the facility-to-location assignment
**Output Format**:
```
Assignment Matrix:
Facilities\Locations  1  2  3  4
Facility 1        (  0  1  0  0 )
Facility 2        (  0  0  0  1 )
Facility 3        (  1  0  0  0 )
Facility 4        (  0  0  1  0 )
```

**Key Relationships**:
- **Used by**: `calculate_qap_fitness()` when `show_details=True`
- **Purpose**: Human-readable assignment visualization

---

### 📄 `optimizer.py` - Main SFO Algorithm Controller

#### Class: `SailfishOptimizer`
**Purpose**: Main orchestrator for the entire SFO optimization process

#### Constructor: `__init__(n_sailfish, n_sardines, freq_matrix, distance_matrix, max_iter, A, epsilon, log_to_file)`
**Initialization Process**:
1. **Parameter Validation**:
   - Ensures `n_sardines > n_sailfish` (algorithm constraint)
   - Sets all instance variables
   - Calculates problem size from matrix dimensions

2. **Logging Setup**:
   - If `log_to_file=True`: Creates `OutputLogger` instance
   - Redirects `sys.stdout` to log file
   - Prints initialization header with parameters

3. **Population Arrays Initialization**:
   - `sailfish_random_values`: Continuous position vectors [0,1]
   - `sailfish_solutions`: Integer permutations
   - `sailfish_fitness`: Cost values for each solution
   - Similar arrays for sardines

4. **Best Solution Tracking**:
   - `best_solution`: Global best permutation found
   - `best_fitness`: Global best cost value
   - `fitness_history`: List of best fitness per iteration

**Key Relationships**:
- **Input**: All algorithm parameters and problem data
- **Output**: Initialized optimizer ready for execution
- **Dependencies**: `io_utils.OutputLogger`, `sfo.*` modules

#### Method: `generate_random_values(n_individuals: int)`
**Purpose**: Creates random continuous position vectors for population initialization
**Algorithm**:
```python
for each individual:
    position = [random.random() for _ in range(problem_size)]
    # Example: [0.8, 0.2, 0.9, 0.1] for 4×4 problem
```

**Key Relationships**:
- **Used by**: Population initialization in `run_optimization()`
- **Output**: List of random position vectors
- **Purpose**: Provides starting positions for optimization

#### Method: `convert_random_to_solution(random_values: List[float])`
**Purpose**: Converts continuous random values to valid facility permutations
**Algorithm**:
1. **Create Value-Index Pairs**: `[(0.8,1), (0.2,2), (0.9,3), (0.1,4)]`
2. **Sort by Values**: `[(0.1,4), (0.2,2), (0.8,1), (0.9,3)]`
3. **Extract Indices**: `[4, 2, 1, 3]`
4. **Interpret**: Facility 4→Location 1, Facility 2→Location 2, etc.

**Key Relationships**:
- **Input**: Random continuous values [0,1]
- **Output**: Valid permutation of facility numbers
- **Used by**: Solution generation and position updates
- **Mathematical**: Implements argsort operation

#### Method: `run_optimization()`
**Purpose**: Executes the complete SFO optimization process
**Main Loop Structure**:
```python
for iteration in range(max_iter):
    # Update sailfish positions
    # Update sardine positions  
    # Recalculate fitness
    # Perform population replacement
    # Update best solutions
```

**Key Relationships**:
- **Calls**: All SFO component functions from `sfo/` modules
- **Coordinates**: Entire optimization workflow
- **Output**: Final best solution and fitness

---

### 📁 `sfo/` - Algorithm Component Modules

#### 📄 `sfo/population.py` - Population Management

#### Function: `print_random_populations(engine)`
**Purpose**: Displays initial random populations for debugging
**Output Format**:
```
Sailfish Random Values:
SF1: [0.8, 0.2, 0.9, 0.1]
SF2: [0.3, 0.7, 0.1, 0.6]
...

Sardine Random Values:
SD1: [0.4, 0.8, 0.2, 0.9]
SD2: [0.1, 0.5, 0.7, 0.3]
...
```

**Key Relationships**:
- **Used by**: `SailfishOptimizer.print_random_populations()`
- **Purpose**: Initial population visualization

#### Function: `save_original_positions(engine)`
**Purpose**: Stores initial positions for comparison and analysis
**Storage**:
- `original_sailfish_positions`: Initial sailfish random values
- `original_sardine_positions`: Initial sardine random values

**Key Relationships**:
- **Used by**: `SailfishOptimizer.save_original_positions()`
- **Purpose**: Position tracking for analysis

#### Function: `print_sorted_arrays_and_solutions(engine)`
**Purpose**: Shows conversion from random values to solutions
**Output Format**:
```
SF1 Random: [0.8, 0.2, 0.9, 0.1] → Solution: [4, 2, 3, 1]
SF2 Random: [0.3, 0.7, 0.1, 0.6] → Solution: [3, 1, 4, 2]
...
```

**Key Relationships**:
- **Used by**: `SailfishOptimizer.print_sorted_arrays_and_solutions()`
- **Purpose**: Solution generation verification

---

#### 📄 `sfo/fitness.py` - Fitness Evaluation

#### Function: `calculate_detailed_fitness(engine)`
**Purpose**: Evaluates fitness for all individuals in both populations
**Process**:
1. **Sailfish Fitness**:
   - Converts random positions to solutions
   - Calls `calculate_qap_fitness()` for each solution
   - Updates `sailfish_fitness` array

2. **Sardine Fitness**:
   - Same process for sardine population
   - Updates `sardine_fitness` array

3. **Best Solution Tracking**:
   - Identifies best sailfish and worst sardine
   - Updates global best solution if improved

**Key Relationships**:
- **Calls**: `qap_core.calculate_qap_fitness()`
- **Updates**: All fitness arrays and best solution tracking
- **Used by**: Initial fitness calculation and iteration updates

#### Function: `print_fitness_summary(engine)`
**Purpose**: Displays fitness statistics for current iteration
**Output Format**:
```
Fitness Summary:
Best Sailfish: SF3 with fitness 1234.56
Worst Sardine: SD45 with fitness 5678.90
Global Best: 1234.56
```

**Key Relationships**:
- **Used by**: `SailfishOptimizer.print_fitness_summary()`
- **Purpose**: Iteration progress monitoring

---

#### 📄 `sfo/dynamics.py` - Position Updates

#### Function: `calculate_pd_and_lambda_values(engine)`
**Purpose**: Calculates Predator Distance (PD) and lambda parameters for sailfish updates
**Mathematical Implementation**:
```python
# PD calculation
distance_vector = elite_position - current_position
distance_magnitude = sqrt(sum(d² for d in distance_vector))
PD = 2 * random() * distance_vector / distance_magnitude

# Lambda calculation  
lambda_val = random()  # Random value [0,1]
```

**Key Relationships**:
- **Input**: Current and elite sailfish positions
- **Output**: PD vector and lambda scalar
- **Used by**: Sailfish position update calculations

#### Function: `update_sailfish_positions(engine)`
**Purpose**: Updates all sailfish positions using SFO hunting strategy
**Algorithm**:
```python
for each sailfish:
    # Calculate PD and lambda
    PD, lambda_val = calculate_pd_and_lambda_values()
    
    # Update position using SFO equation
    new_position = old_position + lambda_val * (elite - old_position) + PD * (elite - old_position)
    
    # Apply bounds [0,1]
    new_position = clip(new_position, 0, 1)
```

**Key Relationships**:
- **Calls**: `calculate_pd_and_lambda_values()`
- **Updates**: `sailfish_random_values` array
- **Mathematical**: Implements core SFO sailfish movement equation

#### Function: `calculate_ap_and_update_sardines(engine)`
**Purpose**: Calculates Attack Power (AP) and updates sardine positions
**Mathematical Implementation**:
```python
# AP calculation (decreases over iterations)
AP = A * (1 - 2 * random() * iteration / max_iter)

# Sardine position update
for each sardine:
    new_position = old_position + AP * (elite - old_position) + random_factor
    new_position = clip(new_position, 0, 1)
```

**Key Relationships**:
- **Input**: Current iteration number and A parameter
- **Output**: Updated sardine positions
- **Mathematical**: Implements SFO sardine escape strategy

---

#### 📄 `sfo/replacement.py` - Solution Replacement

#### Function: `perform_sailfish_sardine_replacement(engine)`
**Purpose**: Manages population replacement and evolution
**Replacement Logic**:
```python
if best_sardine_fitness < worst_sailfish_fitness:
    # Replace worst sailfish with best sardine
    worst_sf_index = argmin(sailfish_fitness)
    sailfish_random_values[worst_sf_index] = best_sardine_position
    sailfish_solutions[worst_sf_index] = best_sardine_solution
    sailfish_fitness[worst_sf_index] = best_sardine_fitness
    
    # Update population counts
    n_sailfish += 1
    n_sardines -= 1
```

**Key Relationships**:
- **Input**: Current fitness values and solutions
- **Output**: Updated populations and counts
- **Purpose**: Population evolution and solution improvement

---

#### 📄 `sfo/reporting.py` - Results Output

#### Function: `print_initial_parameters(engine)`
**Purpose**: Displays initial algorithm parameters and problem setup
**Output Format**:
```
==========================================
SAILFISH OPTIMIZER INITIALIZATION
==========================================
Problem Size: 4×4
Sailfish Count: 5
Sardine Count: 95
Maximum Iterations: 100
A Parameter: 4.0
Epsilon: 0.001
==========================================
```

**Key Relationships**:
- **Used by**: `SailfishOptimizer.print_initial_parameters()`
- **Purpose**: Parameter verification and documentation

#### Function: `print_comprehensive_results_table(engine)`
**Purpose**: Generates detailed iteration-by-iteration results table
**Output Format**:
```
Iteration | Best Fitness | SF Count | SD Count | Elite SF | Injured SD
----------|--------------|----------|----------|----------|------------
    1     |   1500.25    |    5     |    95    |   SF3    |    SD45
    2     |   1450.10    |    5     |    95    |   SF3    |    SD23
    ...
```

**Key Relationships**:
- **Used by**: `SailfishOptimizer.print_comprehensive_results_table()`
- **Purpose**: Performance analysis and convergence monitoring

#### Function: `print_final_results(engine)`
**Purpose**: Displays final optimization results and statistics
**Output Format**:
```
==========================================
FINAL OPTIMIZATION RESULTS
==========================================
Best Solution: [3, 1, 4, 2]
Best Fitness: 1234.56
Total Iterations: 100
Final Population: 5 sailfish, 95 sardines
Convergence: Achieved at iteration 87
==========================================
```

**Key Relationships**:
- **Used by**: `SailfishOptimizer.print_final_results()`
- **Purpose**: Final result presentation

---

## 🔄 Function Call Flow & Data Relationships

### **Main Execution Flow**:
```
main() [QAPFItnessfix.py]
    ↓
read_matrices_from_csv() [io_utils.py]
    ↓
SailfishOptimizer.__init__() [optimizer.py]
    ↓
run_optimization() [optimizer.py]
    ├── save_original_positions() [population.py]
    ├── print_initial_parameters() [reporting.py]
    ├── generate_random_values() [optimizer.py]
    ├── calculate_detailed_fitness() [fitness.py]
    │   └── calculate_qap_fitness() [qap_core.py]
    └── Main Loop:
        ├── calculate_pd_and_lambda_values() [dynamics.py]
        ├── update_sailfish_positions() [dynamics.py]
        ├── calculate_ap_and_update_sardines() [dynamics.py]
        ├── calculate_detailed_fitness() [fitness.py]
        └── perform_sailfish_sardine_replacement() [replacement.py]
    ↓
print_final_results() [reporting.py]
```

### **Data Flow Between Functions**:
1. **Matrix Data**: `io_utils.py` → `optimizer.py` → `qap_core.py`
2. **Random Values**: `optimizer.py` → `population.py` → `fitness.py`
3. **Solutions**: `fitness.py` → `qap_core.py` → `optimizer.py`
4. **Fitness Values**: `qap_core.py` → `fitness.py` → `reporting.py`
5. **Position Updates**: `dynamics.py` → `fitness.py` → `replacement.py`

### **Key Data Structures**:
- **`freq_matrix` & `distance_matrix`**: Problem definition (shared across modules)
- **`sailfish_random_values` & `sardine_random_values`**: Continuous positions [0,1]
- **`sailfish_solutions` & `sardine_solutions`**: Integer permutations
- **`sailfish_fitness` & `sardine_fitness`**: Cost values
- **`best_solution` & `best_fitness`**: Global optimization state
- **`sailfish_using_sardine_positions`**: NEW: Tracks which sailfish should use sardine sorted positions for updates after replacement

### **Module Dependencies**:
- **`QAPFItnessfix.py`** → `io_utils.py`, `optimizer.py`
- **`optimizer.py`** → All `sfo/*.py` modules, `io_utils.py`
- **`sfo/*.py`** → `qap_core.py` (for fitness calculation)
- **`qap_core.py`** → No external dependencies (pure QAP logic)
- **`io_utils.py`** → No external dependencies (pure I/O operations)
