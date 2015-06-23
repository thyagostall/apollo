# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Command(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

class Create(Command):
    def execute(self):
        
