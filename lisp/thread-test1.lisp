;;
;; thread-test1.lisp : An exercise of using bordeaux-threads.
;;
;; Usage:
;;   $ sbcl --load thread-test1.lisp --eval '(main)'
;;
;; License:
;;  Apache License, Version 2.0
;; History:
;;   * 2021/12/31 v0.1 Initial version based on:
;; Author:
;;  Masanori Itoh <masanori.itoh@gmail.com>
;; References:
;;   * [1] https://quickdocs.org/bordeaux-threads
;;   * [2] https://blog.8arrow.org/entry/2014/02/04/041417
;; Credits:
;;   * This is based on an example shown in [1].
;;     Faults are mine, honors belong to the blog author of [1].
;; TOTO:
;;  * Write mpmt1.lisp

(ql:quickload :bordeaux-threads)
(defun print-thread-info ()
  (let* ((curr-thread (bt:current-thread))
         (curr-thread-name (bt:thread-name curr-thread))
         (all-threads (bt:all-threads)))
    (format t "Current thread: ~a~%" curr-thread)
    (format t "Current thread name: ~a~%" curr-thread-name)
    (format t "All threads:~% ~{~a~%~}~%" all-threads))
  nil)
;;
;;
;;
(defun iota (n &optional (start 0))
  (if (zerop n)
      nil
      (cons start (iota (- n 1) (1+ start)))))

(defun fib (n)
  "Return the nth Fibonacchi number."
  (if (< n 2)
      n
    (+ (fib (- n 1))
       (fib (- n 2)))))
;;
(defun main ()
  (let*
      ((iota_n 8)
       (fib_n 40)
       (ths
	(mapcar
	 (lambda (i)
	   (declare (ignore i))
	   (bt:make-thread
	    (lambda ()
	      (time (fib fib_n)))
	      :initial-bindings `((*trace-output* . ,*trace-output*))))
	 (iota iota_n))))
    (print-thread-info)
    (mapcar #'bt:join-thread ths))
  (quit))
