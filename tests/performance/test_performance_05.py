"""
Performance Test 5 - High I/O Operations
This test performs intensive input/output operations to test parallel execution performance.
"""

from .test_io_performance_base import TestIOPerformanceBase


class TestPerformance05(TestIOPerformanceBase):
    """Performance test instance 5"""
    
    def test_performance_05_large_file_read_write(self):
        """Test 5: Large file operations"""
        super().test_large_file_read_write()
    
    def test_performance_05_json_processing(self):
        """Test 5: JSON data processing"""
        super().test_json_processing()
    
    def test_performance_05_csv_operations(self):
        """Test 5: CSV file operations"""
        super().test_csv_operations()
    
    def test_performance_05_numpy_array_operations(self):
        """Test 5: NumPy array operations"""
        super().test_numpy_array_operations()
    
    def test_performance_05_multiple_file_operations(self):
        """Test 5: Multiple file operations"""
        super().test_multiple_file_operations()
    
    def test_performance_05_simulated_processing_delay(self):
        """Test 5: Processing with delays"""
        super().test_simulated_processing_delay()