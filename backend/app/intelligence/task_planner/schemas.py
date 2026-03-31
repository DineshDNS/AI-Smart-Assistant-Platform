
from typing import List, Optional, Dict


class Task:
    task_id: str
    action: str
    target: str
    data_ref: Optional[int]
    status: str
    depends_on: Optional[str]
