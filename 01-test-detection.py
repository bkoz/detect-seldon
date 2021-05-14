from Detection import *
import numpy as np
import requests
import logging
import time

logging.basicConfig(level=logging.INFO)

DETECTION_URL = 'http://detection-redhat-opendatahub.apps.ocp.a122.sandbox1172.opentlc.com/api/v1.0/predictions'
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
# d = Detection()
# d.load()

# local_response = d.predict(img, np.array([1]))

# print()
# print(f'local_response:')
# print()
# print(f'{local_response}')
# print()

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
t0 = time.time()
img_payload = {"data": {"ndarray": img.tolist()} }
logging.info(f'Create payload: Elapsed time = {time.time() - t0}')

response = requests.post(DETECTION_URL, json=img_payload)
logging.info(f'Request: Elapsed time = {time.time() - t0}')
print(f'rest_response: {response}')
print(f'rest content:')
print()
print(response.json())

