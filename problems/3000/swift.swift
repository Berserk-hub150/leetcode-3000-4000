class Solution {
    func areaOfMaxDiagonal(_ dimensions: [[Int]]) -> Int {
        var bestDiag = 0
        var bestArea = 0
        for d in dimensions {
            let length = d[0]
            let width = d[1]
            let diag = length * length + width * width
            let area = length * width
            if diag > bestDiag || (diag == bestDiag && area > bestArea) {
                bestDiag = diag
                bestArea = area
            }
        }
        return bestArea
    }
}
