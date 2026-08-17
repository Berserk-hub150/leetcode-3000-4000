/**
 * @param {number[][]} dimensions
 * @return {number}
 */
var areaOfMaxDiagonal = function(dimensions) {
    let bestDiag = 0;
    let bestArea = 0;
    for (const [length, width] of dimensions) {
        const diag = length * length + width * width;
        const area = length * width;
        if (diag > bestDiag || (diag === bestDiag && area > bestArea)) {
            bestDiag = diag;
            bestArea = area;
        }
    }
    return bestArea;
};
