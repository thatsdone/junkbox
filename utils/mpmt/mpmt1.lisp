;;
;; mpmt1.lisp : A Common Lisp version of mpmt1.py
;;
;; Usage:
;;   $ sbcl --load mpmt1.lisp --eval '(main)' [-n #CTX] [-d DURATION] [-m MODE]
;;
;; License:
;;  Apache License, Version 2.0
;; History:
;;   * 2022/01/08 v0.1 Initial version.
;; Author:
;;  Masanori Itoh <masanori.itoh@gmail.com>
;;
;; TODO:
;;  * Need to investigate thread argument handling behavior.
(ql:quickload :bordeaux-threads)
(ql:quickload :getopt)
(use-package :getopt)


(defun time-us ()
  (multiple-value-bind (tv_sec tv_usec)
      (get-time-of-day)
    (+ (* tv_sec 1000000) tv_usec)))

(defun busy_worker (id duration)
  (format t "busy_worker: id: ~a ~a~%" id duration)
  (let* ((ts_save (time-us))
	(max (* duration 1000000))
	(ts ts_save))
    (loop
       (setq ts (time-us))
       (if (>= (- ts ts_save) max)
	   (progn
	    (format t "Expired! id: ~a ~a ~%" id (- ts ts_save))
	    (return))))))

(defun parse-arg()
  (multiple-value-bind (out-args out-opts errors num_context duration mode)
      (getopt (cdr sb-ext:*posix-argv*)
	      '(("n" :OPTIONAL 4) ("d" :OPTIONAL 10) ("m" :OPTIONAL "t")))

    ;; Handle illegal options
    (when errors
      (format t "Illegal options: ~a ~a ~a ~%" out-args out-opts errors)
      (quit))
    (dolist (opt out-opts)
      (cond
	((equal (car opt) "n")
	 (setf num_context (parse-integer(cdr opt))))
	((equal (car opt) "d")
	 (setf duration (parse-integer(cdr opt))))
	((equal (car opt) "m")
	 (setf mode (cdr opt)))))
    (pairlis '(num_context duration mode) (list num_context duration mode))
    )
  )

(defun main ()
  ;;
  ;; parse command line arguments
  ;;
  (let ((options (parse-arg))
	(threads '()))
    (format t "num_context: ~a duration: ~a mode: ~a ~%"
	    (cdr (assoc 'num_context options))
	    (cdr (assoc 'duration options))
	    (cdr (assoc 'mode options)))
    ;;
    ;; create given number of threads
    ;;
    (loop for i from 1
       while (<= i (cdr (assoc 'num_context options)))
       do
	 (format t "creating thread id: ~a~%" i)
	 (push
	  (bt:make-thread
	   (lambda()
	     ;; 'i' is pass-by-reference?
	     (busy_worker i (cdr (assoc 'duration options))))
	   :initial-bindings `((*trace-output* . ,*trace-output*)))
	  threads)
	 ;; if you uncomment the below, you would see consistent worker id.
	 ;; (sleep 1)
	 )

    (format t "threads: ~a ~%" threads)

    ;;
    ;; wait for thread completions
    ;;
    (mapcar (lambda (th)
	      (format t "calling join-thread for ~a ~%" th)
	      (bt:join-thread th)
	      (format t "join-thread returned for ~a ~%" th)
	      )
	      threads)
    )
    (quit)
)
