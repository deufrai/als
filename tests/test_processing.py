import threading

from als.code_utilities import SignalingQueue
from als.processing import QueueConsumer


class _Consumer(QueueConsumer):
    def _handle_item(self, image):
        pass


def test_queue_consumer_names_python_thread_for_logging(monkeypatch):
    """
    Checks that QThread workers replace Python's Dummy-* logging name.
    """
    consumer = _Consumer("pre-process", SignalingQueue())
    original_name = threading.current_thread().name
    monkeypatch.setattr(
        "als.processing.QThread.currentThread",
        lambda: consumer)

    try:
        consumer._prepare_thread_logging()

        assert threading.current_thread().name == "pre-process"
    finally:
        threading.current_thread().name = original_name


def test_queue_consumer_does_not_rename_other_threads(monkeypatch):
    """
    Checks that setup-time calls in the main Qt thread keep their Python name.
    """
    consumer = _Consumer("pre-process", SignalingQueue())
    original_name = threading.current_thread().name
    monkeypatch.setattr(
        "als.processing.QThread.currentThread",
        lambda: object())

    consumer._prepare_thread_logging()

    assert threading.current_thread().name == original_name
