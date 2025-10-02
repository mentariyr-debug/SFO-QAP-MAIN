import sys
from datetime import datetime
from typing import List, Tuple, Any

from qap_core import get_default_matrices


DEFAULT_CSV_PATH: str = r"C:\Users\bengkel\Desktop\Project_SFO\QAP\qap_matrices2.csv"


class OutputLogger:
    """Class to handle dual output to both console and file"""
    def __init__(self, filename: str = "output.txt") -> None:
        self.terminal: Any = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')
        # Add header with student information
        self.log.write("="*80 + "\n")
        self.log.write("PENERAPAN SAILFISH OPTIMIZER ALGORITHM\n")
        self.log.write("(SFO) UNTUK MENYELESAIKAN QUADRATIC\n")
        self.log.write("ASSIGNMENT PROBLEM (QAP)\n")
        self.log.write("\n")
        self.log.write("MENTARI YANI ROFANDI\n")
        self.log.write("082111233064\n")
        self.log.write("="*80 + "\n\n")
        self.log.write(f"Sailfish Optimizer Output Log\n")
        self.log.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log.write(f"{'='*80}\n\n")
        self.log.flush()
    def write(self, message: str) -> None:
        # Only write to file (suppress terminal)
        self.log.write(message)
        self.log.flush()
    def flush(self) -> None:
        # No terminal echo; just flush file
        self.log.flush()
    def close(self) -> None:
        if self.log:
            self.log.close()
    def __enter__(self) -> "OutputLogger":
        return self
    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


class DualOutputLogger:
    """Class to handle separate output to terminal and file"""
    def __init__(self, filename: str = "output.txt") -> None:
        self.terminal: Any = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')
        # Add header with student information
        self.log.write("="*80 + "\n")
        self.log.write("PENERAPAN SAILFISH OPTIMIZER ALGORITHM\n")
        self.log.write("(SFO) UNTUK MENYELESAIKAN QUADRATIC\n")
        self.log.write("ASSIGNMENT PROBLEM (QAP)\n")
        self.log.write("\n")
        self.log.write("MENTARI YANI ROFANDI\n")
        self.log.write("082111233064\n")
        self.log.write("="*80 + "\n\n")
        self.log.write(f"Sailfish Optimizer Detailed Output Log\n")
        self.log.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log.write(f"{'='*80}\n\n")
        self.log.flush()
        
    def write(self, message: str) -> None:
        """Write to file only (used when redirected as stdout)"""
        self.log.write(message)
        self.log.flush()
        
    def write_to_file(self, message: str) -> None:
        """Write only to file"""
        self.log.write(message)
        self.log.flush()
        
    def write_to_terminal(self, message: str) -> None:
        """Write only to terminal"""
        self.terminal.write(message)
        self.terminal.flush()
        
    def write_to_both(self, message: str) -> None:
        """Write to both terminal and file"""
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()
        
    def flush(self) -> None:
        self.terminal.flush()
        self.log.flush()
        
    def close(self) -> None:
        if self.log:
            self.log.close()
            
    def __enter__(self) -> "DualOutputLogger":
        return self
        
    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def read_matrices_from_csv(filename: str) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Read frequency and distance matrices from a CSV file.
    Expected format:
    - First n rows: frequency matrix
    - Empty row
    - Next n rows: distance matrix
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        empty_row_index = -1
        for i, line in enumerate(lines):
            if line.strip() == '':
                empty_row_index = i
                break
        if empty_row_index == -1:
            raise ValueError("No empty row found to separate matrices")
        freq_data: List[List[float]] = []
        for i in range(empty_row_index):
            row = [float(x) for x in lines[i].strip().split(',')]
            freq_data.append(row)
        dist_data: List[List[float]] = []
        for i in range(empty_row_index + 1, len(lines)):
            if lines[i].strip():
                row = [float(x) for x in lines[i].strip().split(',')]
                dist_data.append(row)
        return freq_data, dist_data
    except FileNotFoundError:
        print(f"File {filename} not found. Using default matrices.")
        return get_default_matrices()


__all__ = [
    "OutputLogger",
    "DualOutputLogger",
    "NullWriter",
    "DEFAULT_CSV_PATH",
    "read_matrices_from_csv",
]


class NullWriter:
    def write(self, message: str) -> None:
        pass
    def flush(self) -> None:
        pass



