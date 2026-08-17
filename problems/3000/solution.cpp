class Solution {
public:
    int areaOfMaxDiagonal(vector<vector<int>>& dimensions) {
        int bestDiag = 0, bestArea = 0;
        for (const auto& d : dimensions) {
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
};
