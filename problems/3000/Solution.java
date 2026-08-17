class Solution {
    public int areaOfMaxDiagonal(int[][] dimensions) {
        int bestDiag = 0;
        int bestArea = 0;
        for (int[] d : dimensions) {
            int length = d[0], width = d[1];
            int diag = length * length + width * width;
            int area = length * width;
            if (diag > bestDiag || (diag == bestDiag && area > bestArea)) {
                bestDiag = diag;
                bestArea = area;
            }
        }
        return bestArea;
    }
}
