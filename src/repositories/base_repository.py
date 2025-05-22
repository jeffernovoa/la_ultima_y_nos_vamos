from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def save(self, obj):
        pass

    @abstractmethod
    def get_by_id(self, obj_id):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def list_all(self):
        pass
