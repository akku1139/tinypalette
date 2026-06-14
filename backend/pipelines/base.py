from abc import ABC, abstractmethod
from tinygrad.device import Device
from tinygrad.tensor import Tensor

class Model(ABC):
  def __init__(self, path: str) -> None:
    pass

class Pipeline[T: Model](ABC):
  def __init__(self, model: T) -> None:
    self.device = Device[Device.DEFAULT]
    self.model = model

  @abstractmethod
  def generate(self, prompt: str) -> Tensor:
    pass
