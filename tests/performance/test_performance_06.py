"""
Performance Test 6 - High I/O Operations
This test performs intensive input/output operations to test parallel execution performance.
"""

from .test_io_performance_base import TestIOPerformanceBase


class TestPerformance06(TestIOPerformanceBase):
    """Performance test instance 6"""
    
    def test_performance_06_large_file_read_write(self):
        """Test 6: Large file operations"""
        super().test_large_file_read_write()
    
    def test_performance_06_json_processing(self):
        """Test 6: JSON data processing"""
        super().test_json_processing()
    
    def test_performance_06_csv_operations(self):
        """Test 6: CSV file operations"""
        super().test_csv_operations()
    
    def test_performance_06_numpy_array_operations(self):
        """Test 6: NumPy array operations"""
        super().test_numpy_array_operations()
    
    def test_performance_06_multiple_file_operations(self):
        """Test 6: Multiple file operations"""
        super().test_multiple_file_operations()
    
    def test_performance_06_simulated_processing_delay(self):
        """Test 6: Processing with delays"""
        super().test_simulated_processing_delay()