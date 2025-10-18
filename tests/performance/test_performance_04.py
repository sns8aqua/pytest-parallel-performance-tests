"""
Performance Test 4 - High I/O Operations
This test performs intensive input/output operations to test parallel execution performance.
"""

from .test_io_performance_base import TestIOPerformanceBase


class TestPerformance04(TestIOPerformanceBase):
    """Performance test instance 4"""
    
    def test_performance_04_large_file_read_write(self):
        """Test 4: Large file operations"""
        super().test_large_file_read_write()
    
    def test_performance_04_json_processing(self):
        """Test 4: JSON data processing"""
        super().test_json_processing()
    
    def test_performance_04_csv_operations(self):
        """Test 4: CSV file operations"""
        super().test_csv_operations()
    
    def test_performance_04_numpy_array_operations(self):
        """Test 4: NumPy array operations"""
        super().test_numpy_array_operations()
    
    def test_performance_04_multiple_file_operations(self):
        """Test 4: Multiple file operations"""
        super().test_multiple_file_operations()
    
    def test_performance_04_simulated_processing_delay(self):
        """Test 4: Processing with delays"""
        super().test_simulated_processing_delay()