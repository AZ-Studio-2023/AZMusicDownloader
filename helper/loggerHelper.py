import logging, colorlog
from helper.config import cfg


# logger日志
def get_logger(level=logging.INFO):
    # 创建logger对象
    logger = logging.getLogger()
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # 定义颜色输出格式
    color_formatter = colorlog.ColoredFormatter(
        '%(asctime)s - %(log_color)s[%(levelname)s]: %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(color_formatter)

    # 修改Handler
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(console_handler)
    return logger


if cfg.debug_card.value:
    logger = get_logger(logging.DEBUG)
else:
    logger = get_logger()
