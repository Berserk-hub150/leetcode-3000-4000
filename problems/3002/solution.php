<?php
class Solution {
    function maximumSetSize($nums1, $nums2) {
        $s1 = array_fill_keys($nums1, true);
        $s2 = array_fill_keys($nums2, true);
        $all = $s1 + $s2;
        $half = intdiv(count($nums1), 2);
        return min(count($all), min(count($s1), $half) + min(count($s2), $half));
    }
}
?>
