import logging
from logging import FileHandler

info_log = logging.getLogger('info_log')
info_log.setLevel(logging.INFO)
error_log = logging.getLogger('error_log')
error_log.setLevel(logging.ERROR)

info_handling = FileHandler('./info.log', mode='a', encoding=None, delay=False)
error_handling = FileHandler('./error.log', mode='a', encoding=None, delay=False)

formatting = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
info_handling.setFormatter(formatting)
error_handling.setFormatter(formatting)

info_log.addHandler(info_handling)
error_log.addHandler(error_handling)