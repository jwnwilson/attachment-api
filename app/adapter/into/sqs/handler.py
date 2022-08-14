import json
import logging
import os
import traceback
from typing import List


logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

ENVIRONMENT = os.environ["ENVIRONMENT"]


def lambda_handler(event, context) -> List[dict]:
    tasks_data = []
    records = event["Records"]

    logger.info(f"Processing {len(records)} record(s) from SQS")

    # Loops through every file uploaded
    for i, record in enumerate(event["Records"]):
        i = i + 1
        try:
            logger.info(f"Processing record {i} from SQS")
        except Exception as err:
            err_msg = traceback.format_exc()
            logger.error(f"Record processing failed: {err_msg}, skipping")

    logger.info(f"{len(tasks_data)} records processed from SQS")

    return tasks_data
