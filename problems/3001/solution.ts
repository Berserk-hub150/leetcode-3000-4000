function minMovesToCaptureTheQueen(a: number, b: number, c: number, d: number, e: number, f: number): number {
    const between = (x: number, y: number, z: number): boolean => Math.min(x, z) < y && y < Math.max(x, z);
    const rookBlocked = (a === e && c === a && between(b, d, f)) ||
                        (b === f && d === b && between(a, c, e));
    if ((a === e || b === f) && !rookBlocked) return 1;

    const bishopAttacks = Math.abs(c - e) === Math.abs(d - f);
    const bishopBlocked = bishopAttacks && Math.abs(a - e) === Math.abs(b - f) &&
                          between(c, a, e) && between(d, b, f);
    return bishopAttacks && !bishopBlocked ? 1 : 2;
}
