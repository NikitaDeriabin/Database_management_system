from abc import ABC, abstractmethod

class BaseWindow(ABC):
    @abstractmethod
    def _render_window(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

