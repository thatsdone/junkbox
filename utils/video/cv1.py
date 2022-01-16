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
print('FRAME_COUNT  %d' % (cap.get(cv2.CAP_PROP_FRAME_COUNT)))
fcc = int(cap.get(cv2.CAP_PROP_FOURCC))
print('FOURCC %c%c%c%c (0x%08x)' % (
    (fcc & 0xff),
    ((fcc >> 8) & 0xff),
    ((fcc >> 16) & 0xff),
    ((fcc >> 24) & 0xff),
    fcc)
)
# On CAP_PROP_FORMAT
# https://stackoverflow.com/questions/46094985/what-do-the-numbers-returned-by-opencvs-videocapturegetcv-cap-prop-format-m
# https://stackoverflow.com/questions/14364563/minmaxloc-datatype/14365886#14365886
print('FORMAT %d' % (cap.get(cv2.CAP_PROP_FORMAT)))
# backend specific value indicating the current capture mode
print('MODE  %d' % (cap.get(cv2.CAP_PROP_MODE)))
print('GAMMA %s' % (cap.get(cv2.CAP_PROP_GAMMA)))
print('TEMPERATUR %s' % (cap.get(cv2.CAP_PROP_TEMPERATURE)))
print('SETTINGS %s' % (cap.get(cv2.CAP_PROP_SETTINGS)))
print('CONVERT_RGB %s' % (cap.get(cv2.CAP_PROP_CONVERT_RGB)))
print('POS_MSEC %s' % (cap.get(cv2.CAP_PROP_POS_MSEC)))

cap.release()
#
# other references
#
# https://ichi.pro/opencv-python-gazo-to-bideo-no-yomitori-to-kakikomi-260590272275980
