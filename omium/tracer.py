import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OmiumTracer")

class OmiumTracer:
    @staticmethod
    def start_trace(name: str, metadata: dict = None):
        logger.info(f"[OMIUM TRACE START] {name} | Metadata: {metadata}")
        return {"trace_id": f"trace_{int(time.time())}", "name": name}

    @staticmethod
    def add_event(trace_id: str, event_name: str, details: dict = None):
        logger.info(f"[OMIUM EVENT] {trace_id} -> {event_name} | Details: {details}")

    @staticmethod
    def end_trace(trace_id: str, status: str = "success", result: dict = None):
        logger.info(f"[OMIUM TRACE END] {trace_id} | Status: {status} | Result: {result}")
