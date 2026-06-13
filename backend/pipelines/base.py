from abc import abstractmethod
from tinygrad.device import Device
from tinygrad.tensor import Tensor

class Pipeline:
  def __init__(self) -> None:
    self.device = Device.DEFAULT

  @abstractmethod
  def load(self, path: str):
    pass

  @abstractmethod
  def unload(self):
    pass

  @abstractmethod
  def generate(self, prompt: str) -> Tensor:
    pass
