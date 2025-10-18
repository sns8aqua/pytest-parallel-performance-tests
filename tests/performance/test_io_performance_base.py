"""
High I/O Performance Test Base
This test performs intensive input/output operations to test parallel execution performance.
"""

import os
import json
import csv
import time
import tempfile
import random
import string
from pathlib import Path
import pytest
import numpy as np
from typing import List, Dict, Any


class TestIOPerformanceBase:
    """Base performance test class with high I/O operations"""
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, tmp_path):
        """Setup test data directory"""
        self.test_dir = tmp_path / "performance_test_data"
        self.test_dir.mkdir(exist_ok=True)
        
    def generate_large_text_file(self, file_path: Path, size_mb: int = 10) -> None:
        """Generate a large text file for I/O testing"""
        with open(file_path, 'w') as f:
            # Generate approximately size_mb megabytes of text
            chunk_size = 1024  # 1KB chunks
            chunks_needed = size_mb * 1024
            
            for _ in range(chunks_needed):
                # Generate random text chunk
                chunk = ''.join(random.choices(string.ascii_letters + string.digits + ' \n', k=chunk_size))
                f.write(chunk)
    
    def generate_json_data(self, num_records: int = 10000) -> List[Dict[str, Any]]:
        """Generate large JSON dataset"""
        data = []
        for i in range(num_records):
            record = {
                'id': i,
                'name': f'user_{i}',
                'email': f'user_{i}@example.com',
                'age': random.randint(18, 80),
                'salary': random.uniform(30000, 150000),
                'department': random.choice(['Engineering', 'Marketing', 'Sales', 'HR', 'Finance']),
                'skills': [random.choice(['Python', 'Java', 'JavaScript', 'Go', 'Rust']) for _ in range(random.randint(1, 5))],
                'metadata': {
                    'created_at': f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                    'last_login': f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                    'preferences': {
                        'theme': random.choice(['light', 'dark']),
                        'language': random.choice(['en', 'es', 'fr', 'de']),
                        'notifications': random.choice([True, False])
                    }
                }
            }
            data.append(record)
        return data
    
    def test_large_file_read_write(self):
        """Test reading and writing large files"""
        start_time = time.time()
        
        # Create large text file (10MB)
        large_file = self.test_dir / "large_test_file.txt"
        self.generate_large_text_file(large_file, size_mb=10)
        
        # Read the entire file
        with open(large_file, 'r') as f:
            content = f.read()
        
        # Process the content (count lines and words)
        lines = content.split('\n')
        word_count = len(content.split())
        
        # Write processed results to new file
        results_file = self.test_dir / "processed_results.txt"
        with open(results_file, 'w') as f:
            f.write(f"Total lines: {len(lines)}\n")
            f.write(f"Total words: {word_count}\n")
            f.write(f"File size: {os.path.getsize(large_file)} bytes\n")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert file operations completed successfully
        assert results_file.exists()
        assert os.path.getsize(results_file) > 0
        assert execution_time > 0
        
        print(f"Large file I/O test completed in {execution_time:.2f} seconds")
    
    def test_json_processing(self):
        """Test JSON data processing with heavy I/O"""
        start_time = time.time()
        
        # Generate large JSON dataset
        json_data = self.generate_json_data(num_records=15000)
        
        # Write JSON to file
        json_file = self.test_dir / "large_dataset.json"
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        # Read and process JSON
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        
        # Perform data analysis
        departments = {}
        total_salary = 0
        skill_counts = {}
        
        for record in loaded_data:
            # Department analysis
            dept = record['department']
            departments[dept] = departments.get(dept, 0) + 1
            
            # Salary analysis
            total_salary += record['salary']
            
            # Skill analysis
            for skill in record['skills']:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Write analysis results
        analysis_file = self.test_dir / "json_analysis.json"
        analysis_results = {
            'total_records': len(loaded_data),
            'average_salary': total_salary / len(loaded_data),
            'department_distribution': departments,
            'skill_distribution': skill_counts,
            'processing_time': time.time() - start_time
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assertions
        assert analysis_file.exists()
        assert len(loaded_data) == 15000
        assert analysis_results['total_records'] == 15000
        
        print(f"JSON processing test completed in {execution_time:.2f} seconds")
    
    def test_csv_operations(self):
        """Test CSV file operations with large datasets"""
        start_time = time.time()
        
        # Generate CSV data
        csv_file = self.test_dir / "large_dataset.csv"
        
        # Write CSV file
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'value', 'category', 'timestamp'])
            
            for i in range(20000):
                writer.writerow([
                    i,
                    f'item_{i}',
                    random.uniform(0, 1000),
                    random.choice(['A', 'B', 'C', 'D', 'E']),
                    f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
                ])
        
        # Read and process CSV
        data_rows = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            data_rows = list(reader)
        
        # Process data - calculate statistics
        values = [float(row['value']) for row in data_rows]
        categories = [row['category'] for row in data_rows]
        
        stats = {
            'count': len(values),
            'sum': sum(values),
            'mean': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'category_counts': {cat: categories.count(cat) for cat in set(categories)}
        }
        
        # Write statistics to new CSV
        stats_file = self.test_dir / "csv_statistics.csv"
        with open(stats_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['metric', 'value'])
            for key, value in stats.items():
                if key != 'category_counts':
                    writer.writerow([key, value])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assertions
        assert stats_file.exists()
        assert len(data_rows) == 20000
        assert stats['count'] == 20000
        
        print(f"CSV operations test completed in {execution_time:.2f} seconds")
    
    def test_numpy_array_operations(self):
        """Test NumPy array operations with file I/O"""
        start_time = time.time()
        
        # Generate large arrays
        array_size = (1000, 1000)
        array1 = np.random.rand(*array_size)
        array2 = np.random.rand(*array_size)
        
        # Save arrays to files
        array1_file = self.test_dir / "array1.npy"
        array2_file = self.test_dir / "array2.npy"
        
        np.save(array1_file, array1)
        np.save(array2_file, array2)
        
        # Load arrays from files
        loaded_array1 = np.load(array1_file)
        loaded_array2 = np.load(array2_file)
        
        # Perform computations
        result_add = loaded_array1 + loaded_array2
        result_multiply = loaded_array1 * loaded_array2
        result_dot = np.dot(loaded_array1, loaded_array2)
        
        # Save results
        results_file = self.test_dir / "numpy_results.npz"
        np.savez(results_file, 
                 addition=result_add,
                 multiplication=result_multiply,
                 dot_product=result_dot)
        
        # Load and verify results
        loaded_results = np.load(results_file)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assertions
        assert results_file.exists()
        assert 'addition' in loaded_results
        assert 'multiplication' in loaded_results
        assert 'dot_product' in loaded_results
        assert loaded_results['addition'].shape == array_size
        
        print(f"NumPy operations test completed in {execution_time:.2f} seconds")
    
    def test_multiple_file_operations(self):
        """Test multiple concurrent file operations"""
        start_time = time.time()
        
        # Create multiple files with different operations
        files_created = []
        
        for i in range(50):
            file_path = self.test_dir / f"multi_file_{i}.txt"
            
            # Write different content to each file
            with open(file_path, 'w') as f:
                content = f"File {i} content:\n"
                content += "=" * 50 + "\n"
                
                # Add random data
                for j in range(100):
                    line = f"Line {j}: " + ''.join(random.choices(string.ascii_letters, k=50)) + "\n"
                    content += line
                
                f.write(content)
            
            files_created.append(file_path)
        
        # Read all files and process
        total_lines = 0
        total_size = 0
        
        for file_path in files_created:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                total_lines += len(lines)
                total_size += os.path.getsize(file_path)
        
        # Create summary file
        summary_file = self.test_dir / "file_operations_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Files created: {len(files_created)}\n")
            f.write(f"Total lines: {total_lines}\n")
            f.write(f"Total size: {total_size} bytes\n")
            f.write(f"Average file size: {total_size / len(files_created):.2f} bytes\n")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assertions
        assert len(files_created) == 50
        assert summary_file.exists()
        assert total_lines > 0
        assert total_size > 0
        
        print(f"Multiple file operations test completed in {execution_time:.2f} seconds")
    
    def test_simulated_processing_delay(self):
        """Test with simulated processing delays"""
        start_time = time.time()
        
        # Simulate various processing operations with delays
        processing_results = []
        
        for i in range(10):
            # Simulate different types of processing
            if i % 3 == 0:
                # Simulate CPU-intensive task
                result = sum([x**2 for x in range(10000)])
                time.sleep(0.1)  # Simulate I/O wait
            elif i % 3 == 1:
                # Simulate file processing
                temp_file = self.test_dir / f"temp_processing_{i}.txt"
                with open(temp_file, 'w') as f:
                    f.write(f"Processing result {i}: {random.randint(1000, 9999)}")
                
                with open(temp_file, 'r') as f:
                    result = f.read()
                time.sleep(0.15)  # Simulate processing delay
            else:
                # Simulate data transformation
                data = [random.randint(1, 1000) for _ in range(1000)]
                result = {
                    'sum': sum(data),
                    'avg': sum(data) / len(data),
                    'max': max(data),
                    'min': min(data)
                }
                time.sleep(0.2)  # Simulate computation delay
            
            processing_results.append(result)
        
        # Save final results
        results_file = self.test_dir / "processing_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'results_count': len(processing_results),
                'total_processing_time': time.time() - start_time,
                'results': str(processing_results)  # Convert to string for JSON serialization
            }, f, indent=2)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assertions
        assert len(processing_results) == 10
        assert results_file.exists()
        assert execution_time >= 1.0  # Should take at least 1 second due to sleep operations
        
        print(f"Simulated processing test completed in {execution_time:.2f} seconds")