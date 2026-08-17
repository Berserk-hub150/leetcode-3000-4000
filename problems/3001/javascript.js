/** @return {number} */
var minMovesToCaptureTheQueen = function(a, b, c, d, e, f) {
    const between = (x, y, z) => Math.min(x, z) < y && y < Math.max(x, z);
    const rookBlocked = (a === e && c === a && between(b, d, f)) ||
                        (b === f && d === b && between(a, c, e));
    if ((a === e || b === f) && !rookBlocked) return 1;

    const bishopAttacks = Math.abs(c - e) === Math.abs(d - f);
    const bishopBlocked = bishopAttacks && Math.abs(a - e) === Math.abs(b - f) &&
                          between(c, a, e) && between(d, b, f);
    return bishopAttacks && !bishopBlocked ? 1 : 2;
};
