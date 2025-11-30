#!/usr/bin/env python
"""
Test runner for WhatsApp Bot
Runs all unit tests and displays results
"""
import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """Discover and run all tests"""
    # Discover tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("=" * 70)
    print("Running WhatsApp Bot Test Suite")
    print("=" * 70)
    print()

    exit_code = run_tests()

    print()
    print("=" * 70)
    if exit_code == 0:
        print("[PASS] All tests passed!")
    else:
        print("[FAIL] Some tests failed. Please review the output above.")
    print("=" * 70)

    sys.exit(exit_code)
