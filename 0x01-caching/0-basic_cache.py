#!/usr/bin/env python3
"""Basic dictionary implementation"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    a class BasicCache that inherits from BaseCaching and
    is a caching system
    """

    def __init__(self):
        """
        Class Constructor
        """
        super().__init__()

    def put(self, key, item):
        """
        Must assign to the dictionary self.cache_data the
        item value for the key key.
        if key is None or item is None, this method
        should not do anything.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in
        self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
