class Solution {
    fun areaOfMaxDiagonal(dimensions: Array<IntArray>): Int {
        var bestDiag = 0
        var bestArea = 0
        for (d in dimensions) {
            val length = d[0]
            val width = d[1]
            val diag = length * length + width * width
            val area = length * width
            if (diag > bestDiag || (diag == bestDiag && area > bestArea)) {
                bestDiag = diag
                bestArea = area
            }
        }
        return bestArea
    }
}
