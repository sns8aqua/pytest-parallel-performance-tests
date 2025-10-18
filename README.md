# PyTest Parallel Performance Tests

A comprehensive performance testing suite designed to benchmark pytest execution with various parallelization strategies. This repository contains performance tests that simulate I/O operations, data processing, and computational tasks to evaluate the effectiveness of parallel test execution.

## 🚀 Quick Start

### Clone the Repository

```bash
git clone git@github.com:sns8aqua/pytest-parallel-performance-tests.git
cd pytest-parallel-performance-tests
```

### Setup Python Environment

1. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

2. **Activate Virtual Environment**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencies

The project uses the following core dependencies:

- `numpy==2.2.4` - For numerical computations and array operations
- `pytest==8.3.5` - Testing framework
- `pytest-xdist==3.8.0` - Distributed testing plugin for parallel execution
- `PyYAML==6.0.2` - YAML processing for configuration files
- `jsonschema==4.24.0` - JSON schema validation

## 🧪 Test Structure

The performance test suite includes:

- **11 Test Files**: `test_io_performance_base.py` + `test_performance_01.py` through `test_performance_10.py`
- **186 Total Tests**: Each file contains multiple test classes and methods
- **Test Categories**:
  - Large file read/write operations
  - JSON data processing
  - CSV file operations
  - NumPy array computations
  - Multiple file operations
  - Simulated processing delays

## 🏃‍♂️ Running Tests

### Sequential Execution (Default)

Run all tests sequentially (single-threaded):

```bash
python -m pytest tests/performance/ -v
```

**Expected Output:**
- **Tests**: 186 tests
- **Duration**: ~75-90 seconds
- **Execution**: Single process

### Parallel Execution with Different Core Counts

#### 2 Cores (Processes)
```bash
python -m pytest tests/performance/ -n 2 -v
```

#### 4 Cores (Processes)
```bash
python -m pytest tests/performance/ -n 4 -v
```

#### 8 Cores (Processes)
```bash
python -m pytest tests/performance/ -n 8 -v
```

#### Auto-detect CPU Cores
```bash
python -m pytest tests/performance/ -n auto -v
```

### Advanced Parallel Options


#### Distributed by Individual Tests
```bash
python -m pytest tests/performance/ -n 4 --dist each -v
```

#### Load Balancing (Work Stealing)
```bash
python -m pytest tests/performance/ -n 4 --dist loadscope -v
```

## 📊 Performance Comparison

### Typical Results

| Execution Mode | Cores | Duration | Speedup |
|----------------|-------|----------|---------|
| Sequential     | 1     | ~75s     | 1.0x    |
| Parallel       | 2     | ~45s     | 1.7x    |
| Parallel       | 4     | ~25s     | 3.0x    |
| Parallel       | 8     | ~18s     | 4.2x    |

*Results may vary based on system specifications and available resources*

## 🔧 Additional Options

### Run Specific Test Files
```bash
# Run only one test file
python -m pytest tests/performance/test_performance_01.py -v

# Run specific test files in parallel
python -m pytest tests/performance/test_performance_01.py tests/performance/test_performance_02.py -n 2 -v
```

### Generate Test Reports
```bash
# With detailed output
python -m pytest tests/performance/ -n 4 -v --tb=short

# With test duration timing
python -m pytest tests/performance/ -n 4 -v --durations=10

# Quiet mode (minimal output)
python -m pytest tests/performance/ -n 4 -q
```

### Run with Coverage (if needed)
```bash
# Install coverage first
pip install pytest-cov

# Run with coverage
python -m pytest tests/performance/ -n 4 --cov=tests/performance/ --cov-report=html
```

## 🎯 Benchmarking Different Strategies

### Compare Sequential vs Parallel Performance

1. **Baseline (Sequential)**
   ```bash
   time python -m pytest tests/performance/ -v
   ```

2. **2 Cores**
   ```bash
   time python -m pytest tests/performance/ -n 2 -v
   ```

3. **4 Cores**
   ```bash
   time python -m pytest tests/performance/ -n 4 -v
   ```

4. **8 Cores**
   ```bash
   time python -m pytest tests/performance/ -n 8 -v
   ```

5. **Auto-detect**
   ```bash
   time python -m pytest tests/performance/ -n auto -v
   ```

## 📝 Understanding the Test Output

When running tests, you'll see:

- **Test Discovery**: pytest collects all test files and methods
- **Execution Progress**: Real-time progress with percentage completion
- **Test Results**: Each test shows PASSED/FAILED status
- **Summary**: Final count of passed/failed tests and total duration

Example output:
```
============================== test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.3.5, pluggy-1.6.0
plugins: xdist-3.8.0
collected 186 items

tests/performance/test_io_performance_base.py::TestIOPerformanceBase::test_large_file_read_write PASSED [  0%]
...
============================== 186 passed in 25.34s ==============================
```

### Performance Tips

- **Optimal Core Count**: Usually 2-4x the number of physical CPU cores
- **I/O Bound Tests**: Benefit more from parallelization
- **CPU Bound Tests**: Limited by actual CPU cores
- **Memory Usage**: Monitor memory consumption with high core counts

