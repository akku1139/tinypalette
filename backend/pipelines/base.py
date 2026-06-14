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

  # @abstractmethod
  # def generate(self) -> Tensor:
  #   pass

class Text2ImagePipeline[T: Model](Pipeline):
  @abstractmethod
  def generate(self, prompt: str, nevative_prompt: str, steps: int, seed: int|None, guidance: float) -> Tensor:
    pass

# TODO
class Image2ImagePipeline[T: Model](Pipeline):
  pass
