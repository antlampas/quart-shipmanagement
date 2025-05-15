#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from abc import ABC, abstractmethod

class Editable(ABC):
    @abstractmethod
    def edit(self,attributes:dict):
        pass

class Addable(ABC):
    @abstractmethod
    def add(self,obj:Editable):
        pass
