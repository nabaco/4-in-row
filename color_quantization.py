import sys
import re
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans as SKKMeans


"""
Color-Quantization of image by K-Means algorithm
Command line argument:
    origin image path.
    Num of colors or 'bw' for black and white image.
The result image will be save in the origin folder.
"""


# Upload the cmd argument to variabels
assert len(sys.argv) == 3
img_path = sys.argv[1]
n_colors = sys.argv[2]
bw = False

if n_colors == 'bw':    # Black and white option
    n_colors = 2
    bw = True

assert 0 < int(n_colors) < 256


# Upload the image and convert it to numpy array
img = Image.open(img_path)
img = np.array(img)
w, h, d = img.shape
X = img.reshape((w*h, d))
print(f"Succefly uploaded image from: \"{img_path}\"")


# Initialize K-Means model and cauterize the data
model = SKKMeans(int(n_colors), "random", 1, 100)
model.fit(X)
labels = model.labels_
print("Succefly created and fit K-Means model")


# Cluster centers
if bw:
    centers = np.array([[0, 0, 0], [255, 255, 255]])
else:
    centers = model.cluster_centers_


# Build new image
new_img = []
for label in labels:
    new_img.append(centers[int(label)])

new_img = np.array(new_img)
new_img = new_img.reshape((w, h, d))
new_img = Image.fromarray(new_img.astype(np.uint8))


# Save the new image
pattern = r"\.[\w]+$"
form = re.search(pattern, img_path).group()
new_img_path = re.sub(pattern, "-new"+form, img_path)
new_img.save(new_img_path)
print(f"Succefly created new image at: \"{new_img_path}\"")
