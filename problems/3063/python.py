from collections import Counter
from typing import Optional


class Solution:
    def frequenciesOfElements(self, head: Optional['ListNode']) -> Optional['ListNode']:
        counts = Counter()
        node = head
        while node:
            counts[node.val] += 1
            node = node.next
        dummy = ListNode(0)
        tail = dummy
        for frequency in counts.values():
            tail.next = ListNode(frequency)
            tail = tail.next
        return dummy.next
