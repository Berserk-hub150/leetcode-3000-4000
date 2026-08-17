(define/contract (minimum-cost nums)
  (-> (listof exact-integer?) exact-integer?)
  (+ (first nums) (first (sort (rest nums) <)) (second (sort (rest nums) <))))
