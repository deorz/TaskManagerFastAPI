from enum import IntEnum


class StatusEnum(IntEnum):
    created = 1
    scheduled = 2
    running = 3
    interrupted = 4
    exited = 5
