import unittest
from unittest.mock import Mock
from task_pool import TaskPool, TaskResult

'''TaskPool test'''
class TestTaskPool(unittest.TestCase):
    def setUp(self):
        self.max_workers = 3
        self.task_pool = TaskPool(max_workers=self.max_workers)

    def tearDown(self):
        self.task_pool.close()

    def test_submit_and_get_results(self):
        # Define a mock method and expected result
        mock_method = Mock(return_value=TaskResult(msg="Mock result"))
        expected_result = TaskResult(msg="Mock result")

        # Submit the mock method to the task pool
        self.task_pool.submit(mock_method, "arg")
        self.task_pool.join()

        # Get and check the results
        results = self.task_pool.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], expected_result)
        mock_method.assert_called_once_with("arg")

    def test_submit_exception(self):
        # Define a method that raises an exception
        def exception_method(arg):
            raise ValueError("Test exception")

        # Submit the exception-raising method to the task pool
        self.task_pool.submit(exception_method, "arg")
        self.task_pool.join()

        # Get and check the results
        results = self.task_pool.get_results()
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].flag)
        self.assertIsInstance(results[0].msg, ValueError)


if __name__ == '__main__':
    unittest.main()
