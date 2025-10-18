"""
Performance Test 7 - High I/O Operations
This test performs intensive input/output operations to test parallel execution performance.
"""

from .test_io_performance_base import TestIOPerformanceBase


class TestPerformance07(TestIOPerformanceBase):
    """Performance test instance 7"""
    
    def test_performance_07_large_file_read_write(self):
        """Test 7: Large file operations"""
        super().test_large_file_read_write()
    
    def test_performance_07_json_processing(self):
        """Test 7: JSON data processing"""
        super().test_json_processing()
    
    def test_performance_07_csv_operations(self):
        """Test 7: CSV file operations"""
        super().test_csv_operations()
    
    def test_performance_07_numpy_array_operations(self):
        """Test 7: NumPy array operations"""
        super().test_numpy_array_operations()
    
    def test_performance_07_multiple_file_operations(self):
        """Test 7: Multiple file operations"""
        super().test_multiple_file_operations()
    
    def test_performance_07_simulated_processing_delay(self):
        """Test 7: Processing with delays"""
        super().test_simulated_processing_delay()