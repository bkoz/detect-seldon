from Detection import *
import numpy as np
import requests

DETECTION_URL = 'http://detection-redhat-ml-mon.apps.ocp.2ff8.sandbox379.opentlc.com/api/v1.0/predictions'
IMAGE = os.path.abspath('./boats.png')

#
# Local test
#
d = Detection()
d.load()
# print(d.predict(np.array([1]), np.array([1])))
print()
print()

#
# Rest test
#
#response = requests.post(DETECTION_URL, files={"image": open(IMAGE, "rb").read()}).json()

img_bytes = open(IMAGE, "rb").read()
print(f'image size: {img_bytes.__len__()}')
payload = {'data': {'ndarray': [[5.1, 3.5, 1.4, 0.2]]}}

l2 = []
l2.append(list(img_bytes))

img_payload = {'data': {'ndarray': l2}}

print()
response = requests.post(DETECTION_URL, json=img_payload)
print(response)

# response = requests.post(DETECTION_URL, files={"image": open(IMAGE, "rb").read()})
# print(response)

