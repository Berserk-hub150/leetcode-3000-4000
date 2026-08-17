# @param {Integer[][]} dimensions
# @return {Integer}
def area_of_max_diagonal(dimensions)
  best_diag = 0
  best_area = 0
  dimensions.each do |length, width|
    diag = length * length + width * width
    area = length * width
    if diag > best_diag || (diag == best_diag && area > best_area)
      best_diag = diag
      best_area = area
    end
  end
  best_area
end
