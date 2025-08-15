from dataclasses import dataclass


@dataclass
class DataIngestionAtrifact:
    trained_file_path: str
    test_file_path: str
    