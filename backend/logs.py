import logging

logging.basicConfig(
    filename= "logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode= "w",
    encoding= 'utf-8'
)

log = logging.getLogger(__name__)