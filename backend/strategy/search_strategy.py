# backend/strategy/search_strategy.py

from abc import ABC, abstractmethod
from backend.singleton.account_manager import AccountManager

# --- Strategy Interface ---
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query):
        pass

# --- Concrete Strategy 1 ---
class SearchByMeterID(SearchStrategy):
    def search(self, query):
        return AccountManager().get_user_by_meter_id(query)

# --- Concrete Strategy 2 ---
class SearchByUserID(SearchStrategy):
    def search(self, query):
        return AccountManager().get_user_by_user_id(query)

# --- Context Class ---
class UserSearchContext:
    def __init__(self, strategy: SearchStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self._strategy = strategy

    def execute_search(self, query):
        return self._strategy.search(query)
