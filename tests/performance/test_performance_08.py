"""
Performance Test 8 - High I/O Operations
This test performs intensive input/output operations to test parallel execution performance.
"""

from .test_io_performance_base import TestIOPerformanceBase


class TestPerformance08(TestIOPerformanceBase):
    """Performance test instance 8"""
    
    def test_performance_08_large_file_read_write(self):
        """Test 8: Large file operations"""
        super().test_large_file_read_write()
    
    def test_performance_08_json_processing(self):
        """Test 8: JSON data processing"""
        super().test_json_processing()
    
    def test_performance_08_csv_operations(self):
        """Test 8: CSV file operations"""
        super().test_csv_operations()
    
    def test_performance_08_numpy_array_operations(self):
        """Test 8: NumPy array operations"""
        super().test_numpy_array_operations()
    
    def test_performance_08_multiple_file_operations(self):
        """Test 8: Multiple file operations"""
        super().test_multiple_file_operations()
    
    def test_performance_08_simulated_processing_delay(self):
        """Test 8: Processing with delays"""
        super().test_simulated_processing_delay()