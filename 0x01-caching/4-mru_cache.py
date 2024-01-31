#!/usr/bin/env python3
"""MRU caching"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    a class MRUCache that inherits from BaseCaching
    and is a caching system:
    """
    
    def __init__(self):
        """
        constructor
        """
        super().__init__()
        self.unused_keys = []
    
    def put(self, key, item):
        """
        Must assign to the dictionary self.cache_data the item
        value for the key key.
        """
        if key or item is None:
            return
        size = BaseCaching.MAX_ITEMS
        if key not in self.cache_data and len(self.cache_data) >= size:
            if key in self.unused_keys:
                self.unused_keys.append(
                    self.unused_keys.pop(self.unused_keys.index(key))
                    )
            else:
                self.unused_keys.append(key)
            discard_key = self.unused_keys.pop()
            self.cache_data.pop(discard_key)
            print("DISCARD: {}".format(discard_key))
        self.cache_data[key] = item
    

    def get(self, key):
        """
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in
        self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        if key in self.unused_keys:
            self.unused_keys.append(
                    self.unused_keys.pop(self.unused_keys.index(key))
                    )
        return self.cache_data[key]
