import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("general")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def setup_env():
    # Load environment
    python_path = os.getenv("PYTHONPATH")
    if python_path:
        full_path = os.path.abspath(python_path)
        if full_path not in sys.path:
            sys.path.insert(0, full_path)

    # Set up logging
    setup_logging()
    logger.info("Python Env setup complete.")
