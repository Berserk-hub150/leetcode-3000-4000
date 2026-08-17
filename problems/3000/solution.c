int areaOfMaxDiagonal(int** dimensions, int dimensionsSize, int* dimensionsColSize) {
    int bestDiag = 0, bestArea = 0;
    for (int i = 0; i < dimensionsSize; ++i) {
        int length = dimensions[i][0], width = dimensions[i][1];
        int diag = length * length + width * width;
        int area = length * width;
        if (diag > bestDiag || (diag == bestDiag && area > bestArea)) {
            bestDiag = diag;
            bestArea = area;
        }
    }
    return bestArea;
}
