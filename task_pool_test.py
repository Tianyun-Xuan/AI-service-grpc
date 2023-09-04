"""
Unit tests for task_pool.py

Author: Tianyun Xuan (tianyun.xuan@cn.innovusion.com)

"""
import unittest
from unittest.mock import Mock
from task_pool import TaskPool, TaskResult, ai_grpc_heartbeat_pb2


class TestTaskPool(unittest.TestCase):
    def setUp(self):
        self.max_workers = 3
        self.task_pool = TaskPool(max_workers=self.max_workers)

    def tearDown(self):
        self.task_pool.close()

    def test_submit_and_get_results(self):
        # Define a mock method and expected result
        expected_result = TaskResult(msg="Regular result")
        mock_method = Mock(return_value=expected_result)

        # Submit the mock method to the task pool
        self.task_pool.submit(mock_method, "arg")
        self.task_pool.join()

        # Get and check the results
        results = self.task_pool.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], expected_result)
        mock_method.assert_called_once_with("arg")

    def test_submit_task_exception(self):
        expected_result = TaskResult(
            msg="Mock result", status=ai_grpc_heartbeat_pb2.StatusCode.TASK_EXCEPTION)
        # Define a method that raises an exception
        mock_method = Mock(return_value=expected_result)
        # Submit the exception-raising method to the task pool
        self.task_pool.submit(mock_method, "arg")
        self.task_pool.join()

        # Get and check the results
        results = self.task_pool.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], expected_result)
        mock_method.assert_called_once_with("arg")

    def test_submit_none_exception(self):
        # Submit the exception-raising method to the task pool
        self.task_pool.submit(None, None)
        self.task_pool.join()

        # Get and check the results
        results = self.task_pool.get_results()
        self.assertEqual(len(results), 1)
        expected_result = TaskResult(
            msg="Method is None", status=ai_grpc_heartbeat_pb2.StatusCode.TASK_EXCEPTION)
        self.assertEqual(results[0], expected_result)

    def test_multiple_submissions(self):
        # Define multiple mock methods and expected results
        mock_methods = [
            Mock(return_value=TaskResult(msg="Result 1")),
            Mock(return_value=TaskResult(msg="Result 2")),
            Mock(return_value=TaskResult(msg="Result 3")),
        ]

        expected_results = [
            TaskResult(msg="Result 1"),
            TaskResult(msg="Result 2"),
            TaskResult(msg="Result 3"),
        ]

        # Submit the mock methods to the task pool
        for i, mock_method in enumerate(mock_methods):
            self.task_pool.submit(mock_method, f"arg {i}")

        self.task_pool.join()

        # Get and check the results
        results = self.task_pool.get_results()
        self.assertEqual(len(results), len(expected_results))
        for i in range(len(results)):
            self.assertEqual(results[i], expected_results[i])
            mock_methods[i].assert_called_once_with(f"arg {i}")


if __name__ == '__main__':
    unittest.main()
