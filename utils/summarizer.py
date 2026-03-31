# utils/summarizer.py

from utils.logger import get_logger

logger = get_logger(__name__, "summarizer.log")

def summarize_brd(text):
    try:
        sentences = text.split(".")
        summary = ". ".join(sentences[:5]).strip()
        logger.info("BRD summarized")
        return summary if summary else "No content found"
    except Exception as e:
        logger.error(str(e))
        return "Error in summarization"