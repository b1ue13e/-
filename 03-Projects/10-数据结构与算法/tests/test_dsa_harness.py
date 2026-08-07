import sys, os, unittest

# Add scripts directory to module path
scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.insert(0, os.path.abspath(scripts_dir))

from harness import DataGenerator, SortAlgorithms, StressTester

class TestDSAAlgorithms(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(SortAlgorithms.merge_sort([]), [])
        self.assertEqual(SortAlgorithms.quick_sort_3way([]), [])
        self.assertEqual(SortAlgorithms.bubble_sort([]), [])

    def test_single_element(self):
        self.assertEqual(SortAlgorithms.merge_sort([42]), [42])
        self.assertEqual(SortAlgorithms.quick_sort_3way([42]), [42])

    def test_duplicates(self):
        data = [5, 5, 5, 5, 5]
        self.assertEqual(SortAlgorithms.quick_sort_3way(data), [5, 5, 5, 5, 5])
        self.assertEqual(SortAlgorithms.merge_sort(data), [5, 5, 5, 5, 5])

    def test_stress_pass(self):
        self.assertTrue(StressTester.run_stress_test(num_trials=20, max_n=100))

if __name__ == '__main__':
    unittest.main()
