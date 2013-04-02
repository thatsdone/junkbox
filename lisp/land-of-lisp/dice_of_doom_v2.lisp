(load "dice_of_doom_v1.lisp")
(load "lazy.lisp")

(defparameter *board-size* 4)
(defparameter *board-hexnum* (* *board-size* *board-size*))

(defun add-passing-move (board player spare-dice first-move moves)
  (if first-move 
      moves
      (lazy-cons (list nil
                       (game-tree (add-new-dice board player 
                                                (1- spare-dice))
                                  (mod (1+ player) *num-players*)
                                  0
                                  t))
                 moves)))

(defun attacking-moves (board cur-player spare-dice)
  (labels ((player (pos)
		   (car (aref board pos)))
	   (dice (pos)
		 (cadr (aref board pos))))
    (lazy-mapcan 
     (lambda (src)
       (if (eq (player src) cur-player)
           (lazy-mapcan
            (lambda (dst)
              (if (and (not (eq (player dst)
                                cur-player)) 
                       (> (dice src) (dice dst)))
                  (make-lazy 
                   (list (list (list src dst)
                               (game-tree (board-attack board
                                                        cur-player
                                                        src
                                                        dst
                                                        (dice src))
                                          cur-player
                                          (+ spare-dice (dice dst))
                                          nil))))
                (lazy-nil)))
            (make-lazy (neighbors src)))
         (lazy-nil)))
     (make-lazy (loop for n below *board-hexnum*
                      collect n)))))

(defun handle-human (tree)
  (fresh-line)
  (princ "choose your move:")
  (let ((moves (caddr tree)))
    (labels ((print-moves (moves n)
			  (unless (lazy-null moves)
			    (let* ((move (lazy-car moves))
				   (action (car move)))
			      (fresh-line)
			      (format t "~a. " n)
			      (if action
				  (format t "~a -> ~a" (car action) (cadr action))
				(princ "end turn")))
			    (print-moves (lazy-cdr moves) (1+ n)))))
	    (print-moves moves 1))
    (fresh-line)
    (cadr (lazy-nth (1- (read)) moves))))

(defun play-vs-human (tree)
  (print-info tree)
  (if (not (lazy-null (caddr tree)))
      (play-vs-human (handle-human tree))
    (announce-winner (cadr tree))))

;At this point, you can play a game vs a human with:
; (play-vs-human (game-tree (gen-board) 0 0 t))
;
;Now we start writing improvements for the AI...

(defun limit-tree-depth (tree depth)
  (list (car tree) 
	(cadr tree) 
	(if (zerop depth)
	    (lazy-nil)
	  (lazy-mapcar (lambda (move)
			 (list (car move) 
                               (limit-tree-depth (cadr move) (1- depth))))
		       (caddr tree)))))

(defparameter *ai-level* 4)

(defun handle-computer (tree)
  (let ((ratings (get-ratings (limit-tree-depth tree *ai-level*)
                              (car tree))))
    (cadr (lazy-nth (position (apply #'max ratings) ratings)
                    (caddr tree)))))

(defun play-vs-computer (tree)
  (print-info tree)
  (cond ((lazy-null (caddr tree)) (announce-winner (cadr tree)))
      ((zerop (car tree)) (play-vs-computer (handle-human tree)))
      (t (play-vs-computer (handle-computer tree)))))

(defun score-board (board player)
  (loop for hex across board
        for pos from 0
        sum (if (eq (car hex) player)
                (if (threatened pos board)
                    1
                  2)
              -1)))

(defun threatened (pos board)
  (let* ((hex (aref board pos))
         (player (car hex))
         (dice (cadr hex)))
    (loop for n in (neighbors pos)
          do (let* ((nhex (aref board n))
                    (nplayer (car nhex))
                    (ndice (cadr nhex)))
               (when (and (not (eq player nplayer)) (> ndice dice))
                 (return t))))))

(defun get-ratings (tree player)
  (take-all (lazy-mapcar (lambda (move)
                           (rate-position (cadr move) player))
                         (caddr tree))))

(defun rate-position (tree player)
  (let ((moves (caddr tree)))
    (if (not (lazy-null moves))
	(apply (if (eq (car tree) player)
		   #'max
		 #'min)
	       (get-ratings tree player))
      (score-board (cadr tree) player))))

;You can now play a game against the computer AI:
;
;(play-vs-computer (game-tree (gen-board) 0 0 t))
;
;The rest of this file implements ab pruning.

(defun ab-get-ratings-max (tree player upper-limit lower-limit)
  (labels ((f (moves lower-limit)
           (unless (lazy-null moves)
             (let ((x (ab-rate-position (cadr (lazy-car moves))
                                        player
                                        upper-limit
                                        lower-limit)))
               (if (>= x upper-limit)
                   (list x)
                 (cons x (f (lazy-cdr moves) (max x lower-limit))))))))
    (f (caddr tree) lower-limit)))

(defun ab-get-ratings-min (tree player upper-limit lower-limit)
  (labels ((f (moves upper-limit)
           (unless (lazy-null moves)
             (let ((x (ab-rate-position (cadr (lazy-car moves))
                                        player
                                        upper-limit
                                        lower-limit)))
               (if (<= x lower-limit)
                   (list x)
                 (cons x (f (lazy-cdr moves) (min x upper-limit))))))))
    (f (caddr tree) upper-limit)))

(defun ab-rate-position (tree player upper-limit lower-limit)
  (let ((moves (caddr tree)))
    (if (not (lazy-null moves))
	(if (eq (car tree) player)
            (apply #'max (ab-get-ratings-max tree
                                             player
                                             upper-limit
                                             lower-limit))
          (apply #'min (ab-get-ratings-min tree
                                           player
                                           upper-limit
                                           lower-limit)))
      (score-board (cadr tree) player))))

(defun handle-computer (tree)
  (let ((ratings (ab-get-ratings-max (limit-tree-depth tree *ai-level*)
                                     (car tree) 
                                     most-positive-fixnum
                                     most-negative-fixnum)))
    (cadr (lazy-nth (position (apply #'max ratings) ratings) (caddr tree)))))

(defparameter *board-size* 5)
(defparameter *board-hexnum* (* *board-size* *board-size*))

;(play-vs-computer (game-tree (gen-board) 0 0 t))