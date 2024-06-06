from typing import Any

from loguru._logger import Core, Logger


class JaloLogger(Logger):
    def contextualize(__self, **kwargs: Any):
        __self.trace_id = kwargs.get("trace_id")
        __self.caller_id = kwargs.get("caller_id")

        return super().contextualize(**kwargs)


logger = JaloLogger(
    core=Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=[],
    extra={},
)
