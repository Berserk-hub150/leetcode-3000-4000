<?php
class Solution {
    function minimumCost($nums) {
        $first = PHP_INT_MAX; $second = PHP_INT_MAX;
        for ($i = 1; $i < count($nums); ++$i) {
            $x = $nums[$i];
            if ($x < $first) { $second = $first; $first = $x; }
            elseif ($x < $second) $second = $x;
        }
        return $nums[0] + $first + $second;
    }
}
?>
