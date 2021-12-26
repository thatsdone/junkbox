#
# cv1.py : A sample to get properties of the given vide file.
#
import cv2
import sys

if len(sys.argv) >= 2:
    video_file = sys.argv[1]
else:
    print('Specify a video file')
    sys.exit()

print('opening: %s' % (video_file))

cap = cv2.VideoCapture(video_file)

print('WIDTH  %d' % (cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print('HEIGHT %d' % (cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('FPS    %d' % (cap.get(cv2.CAP_PROP_FPS)))
print('COUNT  %d' % (cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fcc = int(cap.get(cv2.CAP_PROP_FOURCC))
print('FOURCC %c%c%c%c (0x%08x)' % (
    (fcc & 0xff),
    ((fcc >> 8) & 0xff),
    ((fcc >> 16) & 0xff),
    ((fcc >> 24) & 0xff),
    fcc)
)

cap.release()
