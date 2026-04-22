from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict


class PostgreSQLClientPort(ABC):

    @abstractmethod
    def get_db(self):
        pass