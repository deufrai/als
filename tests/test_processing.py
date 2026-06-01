import threading

from als.code_utilities import SignalingQueue
from als.processing import QueueConsumer


class _Consumer(QueueConsumer):
    def _handle_item(self, image):
        pass


def test_queue_consumer_names_python_thread_for_logging():
    """
    Checks that worker startup can replace Python's Dummy-* logging name.
    """
    consumer = _Consumer("pre-process", SignalingQueue())
    original_name = threading.current_thread().name

    try:
        consumer._name_current_thread_for_logging()

        assert threading.current_thread().name == "pre-process"
    finally:
        threading.current_thread().name = original_name
