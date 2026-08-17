class Solution {
  int areaOfMaxDiagonal(List<List<int>> dimensions) {
    int bestDiag = 0;
    int bestArea = 0;
    for (final d in dimensions) {
      final length = d[0], width = d[1];
      final diag = length * length + width * width;
      final area = length * width;
      if (diag > bestDiag || (diag == bestDiag && area > bestArea)) {
        bestDiag = diag;
        bestArea = area;
      }
    }
    return bestArea;
  }
}
