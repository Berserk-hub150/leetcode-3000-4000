(define/contract (min-moves-to-capture-the-queen a b c d e f)
  (-> exact-integer? exact-integer? exact-integer? exact-integer? exact-integer? exact-integer? exact-integer?)
  (define (between? x y z) (< (min x z) y (max x z)))
  (define rook-blocked?
    (or (and (= a e) (= c a) (between? b d f))
        (and (= b f) (= d b) (between? a c e))))
  (cond
    [(and (or (= a e) (= b f)) (not rook-blocked?)) 1]
    [else
     (define bishop-attacks? (= (abs (- c e)) (abs (- d f))))
     (define bishop-blocked?
       (and bishop-attacks? (= (abs (- a e)) (abs (- b f)))
            (between? c a e) (between? d b f)))
     (if (and bishop-attacks? (not bishop-blocked?)) 1 2)]))
