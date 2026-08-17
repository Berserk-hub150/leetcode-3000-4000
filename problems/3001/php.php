<?php
class Solution {
    private function between($x, $y, $z) { return min($x, $z) < $y && $y < max($x, $z); }

    function minMovesToCaptureTheQueen($a, $b, $c, $d, $e, $f) {
        $rookBlocked = ($a === $e && $c === $a && $this->between($b, $d, $f)) ||
                       ($b === $f && $d === $b && $this->between($a, $c, $e));
        if (($a === $e || $b === $f) && !$rookBlocked) return 1;

        $bishopAttacks = abs($c - $e) === abs($d - $f);
        $bishopBlocked = $bishopAttacks && abs($a - $e) === abs($b - $f) &&
                         $this->between($c, $a, $e) && $this->between($d, $b, $f);
        return $bishopAttacks && !$bishopBlocked ? 1 : 2;
    }
}
?>
