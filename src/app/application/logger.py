import functools
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def log(func):  # noqa: ANN001
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"function {func.__name__} called with args {signature}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {e!s}")
            raise

    return wrapper
