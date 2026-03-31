# utils/test_generator.py

from utils.logger import get_logger
from utils.exporter import export_to_csv

logger = get_logger(__name__, "generator.log")

MANDATORY = [
    "DDL", "Sanity", "Smoke",
    "Record Count", "Data Validation",
    "Referential Integrity"
]

def generate_test_cases(text):
    try:
        test_cases = []

        for line in text.split("\n"):
            line = line.strip()
            if line:
                test_cases.append({"test_case": f"Validate {line}", "category": "Data Validation"})

        # Add mandatory coverage
        for cat in MANDATORY:
            test_cases.append({"test_case": f"{cat} validation check", "category": cat})

        file_path = export_to_csv(test_cases, "qa_test_cases.csv")
        logger.info("Test cases generated")
        return test_cases, file_path
    except Exception as e:
        logger.error(str(e))
        return [], None