from typing import Optional


class Solution:
    def gameResult(self, head: Optional['ListNode']) -> str:
        odd = even = 0
        node = head
        while node and node.next:
            if node.val > node.next.val:
                even += 1
            elif node.val < node.next.val:
                odd += 1
            node = node.next.next
        if odd > even:
            return "Odd"
        if even > odd:
            return "Even"
        return "Tie"
