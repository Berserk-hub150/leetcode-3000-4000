defmodule Solution do
  @spec area_of_max_diagonal([[integer]]) :: integer
  def area_of_max_diagonal(dimensions) do
    {_diag, area} =
      Enum.reduce(dimensions, {0, 0}, fn [length, width], {best_diag, best_area} ->
        diag = length * length + width * width
        area = length * width
        if diag > best_diag or (diag == best_diag and area > best_area),
          do: {diag, area},
          else: {best_diag, best_area}
      end)

    area
  end
end
