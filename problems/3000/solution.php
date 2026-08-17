<?php
class Solution {
    function areaOfMaxDiagonal($dimensions) {
        $bestDiag = 0;
        $bestArea = 0;
        foreach ($dimensions as $d) {
            [$length, $width] = $d;
            $diag = $length * $length + $width * $width;
            $area = $length * $width;
            if ($diag > $bestDiag || ($diag === $bestDiag && $area > $bestArea)) {
                $bestDiag = $diag;
                $bestArea = $area;
            }
        }
        return $bestArea;
    }
}
?>
