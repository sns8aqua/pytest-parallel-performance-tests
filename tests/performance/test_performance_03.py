"""
Performance Test 3 - High I/O Operations
This test performs intensive input/output operations to test parallel execution performance.
"""

from .test_io_performance_base import TestIOPerformanceBase


class TestPerformance03(TestIOPerformanceBase):
    """Performance test instance 3"""
    
    def test_performance_03_large_file_read_write(self):
        """Test 3: Large file operations"""
        super().test_large_file_read_write()
    
    def test_performance_03_json_processing(self):
        """Test 3: JSON data processing"""
        super().test_json_processing()
    
    def test_performance_03_csv_operations(self):
        """Test 3: CSV file operations"""
        super().test_csv_operations()
    
    def test_performance_03_numpy_array_operations(self):
        """Test 3: NumPy array operations"""
        super().test_numpy_array_operations()
    
    def test_performance_03_multiple_file_operations(self):
        """Test 3: Multiple file operations"""
        super().test_multiple_file_operations()
    
    def test_performance_03_simulated_processing_delay(self):
        """Test 3: Processing with delays"""
        super().test_simulated_processing_delay()