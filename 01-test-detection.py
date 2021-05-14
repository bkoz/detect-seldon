from Detection import *
import numpy as np
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

DETECTION_URL = 'http://detection-redhat-ml-mon.apps.ocp.2ff8.sandbox379.opentlc.com/api/v1.0/predictions'
# Load 720x1280x3 test image
IMAGE = os.path.abspath('./boats.png')

img_bytes = open(IMAGE, "rb").read()
# read image file and convert to a numpy array.
img = np.asarray(bytearray(img_bytes), dtype="uint8")
img = cv2.imdecode(img, 1)
logging.debug(f'img type: {type(img)}, shape = {img.shape}')
logging.debug(f'img: shape = {img.shape}, dtype: {img.dtype}')

#payload = {'data': {'ndarray': [[5.1, 3.5, 1.4, 0.2]]}}

#
# Local test
#
d = Detection()
d.load()
# X = np.array(img_bytes)
# response = d.predict(np.array([1]), np.array([1]))
# response = d.predict(np.array(open(IMAGE, "rb").read()), np.array([1]))
# local_response = d.predict(X, np.array([1]))
local_response = d.predict(img, np.array([1]))

print()
print(f'local_response:')
print()
print(f'{local_response}')
print()

#
#  REST test
#
# REST Payload options
# Option 1
# l2 = []
# l2.append(list(img))
# img_payload = {'data': {'ndarray': l2}}
# Option 2
# N = np.frombuffer(img, count=-1, dtype=np.ubyte)
# l2 = []
# l2.append(N.tolist())
# img_payload = {'data': {'ndarray': l2}}
#
# Option 3
#
img_payload = {"data": {"ndarray": img.tolist()} }

#response = requests.post(DETECTION_URL, files={"image": open(IMAGE, "rb").read()}).json()
print()
response = requests.post(DETECTION_URL, json=img_payload)
print(f'rest_response: {response}')
print(f'rest content:')
print()
print(response.content)

