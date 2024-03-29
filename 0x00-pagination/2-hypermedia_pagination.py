#!/usr/bin/env python3
""" Hypermedia pagination """

import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ a function that return a tuple of size two containing a
    start index and an end index corresponding to the range
    of indexes to return in a list for those particular
    pagination parameters.
    """
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Finds the correct indexes to paginate dataset correctly"""
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        dataList = self.dataset()
        try:
            start, end = index_range(page, page_size)
            return dataList[start:end]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Implement a get_hyper method that takes the same arguments
        (and defaults) as get_page and returns a dictionary
        containing the following key-value pairs:

        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        data = self.get_page(page, page_size)
        totalPages = math.ceil(len(self.dataset()) / page_size)

        next_page = page + 1 if page < totalPages else None
        prev_page = page - 1 if page > 1 else None

        return {
            'page_size': totalPages,
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': totalPages
        }
