from abc import ABC, abstractmethod


class ITracker(ABC):

    @abstractmethod
    async def get_hash(self):
        pass

    @abstractmethod
    async def start_track(self):
        pass

    @abstractmethod
    async def stop_track(self):
        pass

    @abstractmethod
    async def check_all_sites(self):
        pass
