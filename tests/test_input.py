from als.streams.input import FOLDER_SCANNER_THREAD_NAME, FolderScanner


def test_folder_scanner_names_observer_thread(monkeypatch):
    """
    Checks that watchdog callbacks log under the scanner name.
    """
    observer = _Observer()
    monkeypatch.setattr(
        "als.streams.input.config.get_scan_folder_path",
        lambda: "/tmp")
    monkeypatch.setattr(
        "als.streams.input.PollingObserver",
        lambda: observer)

    scanner = FolderScanner()
    scanner.start()

    assert observer.name == FOLDER_SCANNER_THREAD_NAME
    assert observer.scheduled_handler is scanner
    assert observer.scheduled_path == "/tmp"
    assert observer.scheduled_recursive is True
    assert observer.started is True


class _Observer:
    def __init__(self):
        self.name = None
        self.scheduled_handler = None
        self.scheduled_path = None
        self.scheduled_recursive = None
        self.started = False

    def schedule(self, handler, path, recursive):
        self.scheduled_handler = handler
        self.scheduled_path = path
        self.scheduled_recursive = recursive

    def start(self):
        self.started = True
