import pandas as pd
from utils.logger import get_logger
from utils.exporter import export_to_csv

logger = get_logger(__name__, "reviewer.log")

MANDATORY = ["DDL", "Sanity", "Smoke", "Record Count", "Data Validation", "Referential Integrity"]

def detect_category(tc):
    tc = tc.lower()
    if "ddl" in tc: return "DDL"
    if "sanity" in tc: return "Sanity"
    if "smoke" in tc: return "Smoke"
    if "count" in tc: return "Record Count"
    if "referential" in tc: return "Referential Integrity"
    return "Data Validation"

def review_test_cases(dev_csv, qa_csv):
    try:
        dev_df = pd.read_csv(dev_csv)
        qa_df = pd.read_csv(qa_csv)

        dev = set(dev_df["test_case"])
        qa = set(qa_df["test_case"])

        missing_in_qa = list(dev - qa)
        missing_in_dev = list(qa - dev)

        dev_cat = set(detect_category(tc) for tc in dev)
        qa_cat = set(detect_category(tc) for tc in qa)

        missing_cat_dev = [c for c in MANDATORY if c not in dev_cat]
        missing_cat_qa = [c for c in MANDATORY if c not in qa_cat]

        consolidated = list(dev.union(qa))
        export_to_csv([{"test_case": t} for t in consolidated], "consolidated_test_cases.csv")

        logger.info("Review completed")
        return {
            "missing_in_qa": missing_in_qa,
            "missing_in_dev": missing_in_dev,
            "missing_cat_dev": missing_cat_dev,
            "missing_cat_qa": missing_cat_qa,
            "consolidated": consolidated
        }
    except Exception as e:
        logger.error(str(e))
        return {"error": str(e)}