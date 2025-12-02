# Test Suite Documentation

This directory contains the test suite for the Migraine Network Analysis project.

## 📋 Overview

The test suite uses **pytest** to ensure code quality, reliability, and correct functionality across all modules.

## 🚀 Quick Start

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# From project root
pytest

# With verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run specific test
pytest tests/test_main.py::test_initialization
```

## 📊 Test Coverage

### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=english_version/scripts --cov-report=html

# View coverage in terminal
pytest --cov=english_version/scripts --cov-report=term

# Generate detailed report
pytest --cov=english_version/scripts --cov-report=term-missing
```

Coverage reports are saved to `htmlcov/index.html`.

## 🏷️ Test Categories

Tests are organized with markers for selective execution:

### Unit Tests
```bash
pytest -m unit
```

### Integration Tests
```bash
pytest -m integration
```

### Network Building Tests
```bash
pytest -m network
```

### Slow Tests (Performance)
```bash
# Skip slow tests
pytest -m "not slow"

# Run only slow tests
pytest -m slow
```

## 📁 Test Structure

```
tests/
├── README.md          # This file
├── test_main.py       # Tests for main.py (PubMedRefinedNetworkV2)
├── conftest.py        # Shared fixtures (to be added)
└── fixtures/          # Sample data files (to be added)
    └── sample_pubmed.csv
```

## ✅ Test Coverage Areas

### Current Tests (test_main.py)

1. **Initialization Tests**
   - Network builder initialization
   - Stopwords configuration
   - Category structure validation

2. **Term Cleaning Tests**
   - Basic term cleaning
   - Stopword filtering
   - Edge cases handling
   - Number filtering

3. **Categorization Tests**
   - Trigger mechanism categorization
   - Comorbidity categorization
   - Social impact categorization
   - Intervention categorization
   - Unclassified term handling

4. **Term Extraction Tests**
   - Basic extraction from tags
   - Abstract text processing
   - Research methodology filtering
   - Empty input handling

5. **Network Building Tests**
   - Output structure validation
   - Non-empty results
   - Frequency filtering
   - Category validity

6. **Integration Tests**
   - Full pipeline execution
   - Analysis without crashes

7. **Data Validation Tests**
   - Unique node IDs
   - Valid edge references

8. **Performance Tests**
   - Large dataset processing
   - Time benchmarks

9. **File I/O Tests**
   - CSV loading
   - Missing file handling

## 🎯 Writing New Tests

### Test Naming Convention

- Test files: `test_<module>.py`
- Test classes: `Test<ClassName>`
- Test functions: `test_<functionality>`

### Example Test

```python
def test_example_functionality():
    """Test description"""
    # Arrange
    builder = PubMedRefinedNetworkV2()
    
    # Act
    result = builder.some_method('input')
    
    # Assert
    assert result is not None
    assert result == expected_value
```

### Using Fixtures

```python
@pytest.fixture
def sample_data():
    """Create sample test data"""
    return pd.DataFrame({'col': [1, 2, 3]})

def test_with_fixture(sample_data):
    """Test using fixture"""
    assert len(sample_data) == 3
```

## 🐛 Debugging Failed Tests

### Run with Detailed Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Drop into debugger on failure
pytest --pdb
```

### Run Specific Failed Test

```bash
pytest tests/test_main.py::test_specific_function -v
```

## 📈 Continuous Integration

Tests are automatically run on:
- Every commit (local pre-commit hook - to be added)
- Every pull request (GitHub Actions - to be added)
- Before releases

## 🔧 Troubleshooting

### Import Errors

If you get import errors, ensure you're running from the project root:

```bash
cd c:\Users\Deano\Downloads\detailed_refined_nodes
pytest
```

### Python Path Issues

The test suite adds necessary paths automatically. If issues persist:

```bash
export PYTHONPATH="${PYTHONPATH}:./english_version/scripts"
pytest
```

### Virtual Environment

Always run tests in the virtual environment:

```bash
# Activate venv
english_version\venv\Scripts\activate

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest
```

## 📝 Test Checklist for New Features

When adding new features, ensure:

- [ ] Unit tests for all new functions
- [ ] Integration tests for workflows
- [ ] Edge case handling tests
- [ ] Error condition tests
- [ ] Documentation updated
- [ ] All tests pass (`pytest`)
- [ ] Coverage maintained above 80% (`pytest --cov`)

## 🎓 Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## 📞 Getting Help

If tests fail or you need assistance:
1. Check test output for specific error messages
2. Run with `-v` for verbose output
3. Review the test code in `tests/test_main.py`
4. Check the main code being tested
5. Open an issue with test output

---

**Last Updated**: 2025-12-02
**Test Framework**: pytest 7.0+
**Coverage Tool**: pytest-cov
