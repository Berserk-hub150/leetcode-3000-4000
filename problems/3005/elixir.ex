defmodule Solution do
  @spec max_frequency_elements([integer]) :: integer
  def max_frequency_elements(nums) do
    freq = Enum.frequencies(nums)
    best = freq |> Map.values() |> Enum.max()
    freq |> Map.values() |> Enum.filter(&(&1 == best)) |> Enum.sum()
  end
end
