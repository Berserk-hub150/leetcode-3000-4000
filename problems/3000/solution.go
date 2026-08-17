func areaOfMaxDiagonal(dimensions [][]int) int {
    bestDiag, bestArea := 0, 0
    for _, d := range dimensions {
        length, width := d[0], d[1]
        diag := length*length + width*width
        area := length * width
        if diag > bestDiag || (diag == bestDiag && area > bestArea) {
            bestDiag, bestArea = diag, area
        }
    }
    return bestArea
}
