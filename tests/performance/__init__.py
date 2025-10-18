"""
Performance Test Module

This module contains high I/O performance tests designed to test parallel execution
with pytest-xdist. Each test performs intensive input/output operations including:

- Large file read/write operations
- JSON data processing
- CSV file operations  
- NumPy array operations
- Multiple file operations
- Simulated processing delays

The tests are replicated 10 times to provide sufficient load for parallel execution testing.
"""