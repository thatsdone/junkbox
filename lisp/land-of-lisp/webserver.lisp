; This program is free software; you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation; version 2 of the License.
;
; This program is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; Partial Author: Conrad Barski, M.D.
; Parts Adapted with permission from http.lisp by Ron Garret

(defun decode-param (s)
   (labels ((f (lst)
               (when lst
                 (case (car lst)
                     (#\% (cons (code-char (parse-integer (coerce (list (cadr lst) (caddr lst)) 'string) :radix 16 :junk-allowed t))
                                (f (cdddr lst))))
                     (#\+ (cons #\space (f (cdr lst))))
                     (otherwise (cons (car lst) (f (cdr lst))))))))
       (coerce (f (coerce s 'list)) 'string)))

(defun parse-params (s) 
   (let* ((i1 (position #\= s))
          (i2 (position #\& s))) 
      (cond (i1 (cons (cons (intern (string-upcase (subseq s 0 i1)))
                            (decode-param (subseq s (1+ i1) i2)))
                      (and i2 (parse-params (subseq s (1+ i2))))))
            ((equal s "") nil)
            (t s))))

(defun parse-url (s) 
  (let* ((url (subseq s
                      (+ 2 (position #\space s)) 
                      (position #\space s :from-end t)))
         (x (position #\? url)))
     (if x
         (cons (subseq url 0 x) (parse-params (subseq url (1+ x))))
         (cons url '()))))

(defun get-header (stream)
  (let* ((s (read-line stream))
         (h (let ((i (position #\: s)))
               (when i 
                     (cons (intern (string-upcase (subseq s 0 i)))
                           (subseq s (+ i 2)))))))
     (when h
        (cons h (get-header stream)))))

(defun get-content-params (stream header)
  (let ((content (assoc 'content-length header)))
    (when content
      (parse-params (read-sequence (make-string (read content)) stream)))))

(defun serve (request-handler)
  (let ((socket (socket-server 8080)))
    (unwind-protect
       (loop (with-open-stream (stream (socket-accept socket))
                 (let* ((url    (parse-url (read-line stream)))
                        (path   (car url))
                        (header (get-header stream))
                        (params (append (cdr url) 
                                        (get-content-params stream header)))
                        (*standard-output* stream))
                   (funcall request-handler path header params))))
       (socket-server-close socket))))

(defun hello-request-handler (path header params)
  (if (equal path "greeting")
      (let ((name (assoc 'name params)))
        (if (not name)
            (princ "<form>What is your name?<input name='name' /></form>")
            (format t "Nice to meet you, ~a!" (cdr name))))
      (princ "Sorry... I don't know that page.")))

