from abc import abstractmethod
import os
import sys


class BaseSolution:

    def open_input_file(self, file_name):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, file_name), "r")
        return f.read()

    @abstractmethod
    def solve(*args, **kwargs):
        raise NotImplementedError
