<?php
class Solution {
    function maxFrequencyElements($nums) {
        $freq = [];
        $best = 0;
        foreach ($nums as $x) {
            $freq[$x] = ($freq[$x] ?? 0) + 1;
            $best = max($best, $freq[$x]);
        }
        $ans = 0;
        foreach ($freq as $count) if ($count === $best) $ans += $count;
        return $ans;
    }
}
?>
