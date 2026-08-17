defmodule Solution do
  def minimum_cost([head | tail]) do
    [a, b | _] = Enum.sort(tail)
    head + a + b
  end
end
