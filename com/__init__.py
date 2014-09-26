from com.demimojo.netflix.loader import Constants

__author__ = 'mojosaurus'

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler(Constants.LOG_DIR+'hello.log')
handler.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
