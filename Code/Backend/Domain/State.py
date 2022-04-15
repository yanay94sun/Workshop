from abc import ABC

from Code.Backend.Domain.Visitor import Visitor


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def visitor(self) -> Visitor:
        return self._visitor

    @visitor.setter
    def visitor(self, visitor: Visitor) -> None:
        self._visitor = visitor

    @abstractmethod
    def
