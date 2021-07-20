import cv2
import numpy as np
import os
import random
import webcolors
from math import sqrt
from scipy.spatial import KDTree

try:
    import Image
except ImportError:
    from PIL import Image
from IPython.display import Image as CImage


class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates


class Cluster:
    def __init__(self, center, points):
        self.center = center
        self.points = points


class KMeans:

    def __init__(self, n_clusters, min_diff=1):
        self.n_clusters = n_clusters
        self.min_diff = min_diff

    def calculate_center(self, points):
        n_dim = len(points[0].coordinates)
        vals = [0.0 for i in range(n_dim)]
        for p in points:
            for i in range(n_dim):
                vals[i] += p.coordinates[i]
        coords = [(v / len(points)) for v in vals]
        return Point(coords)

    def assign_points(self, clusters, points):
        plists = [[] for i in range(self.n_clusters)]

        for p in points:
            smallest_distance = float('inf')

            for i in range(self.n_clusters):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i

            plists[idx].append(p)

        return plists

    def fit(self, points):
        clusters = [Cluster(center=p, points=[p]) for p in random.sample(points, self.n_clusters)]

        while True:

            plists = self.assign_points(clusters, points)

            diff = 0

            for i in range(self.n_clusters):
                if not plists[i]:
                    continue
                old = clusters[i]
                center = self.calculate_center(plists[i])
                new = Cluster(center, plists[i])
                clusters[i] = new
                diff = max(diff, euclidean(old.center, new.center))

            if diff < self.min_diff:
                break

        return clusters


def get_points(imagepath):
    img = Image.open(imagepath)

    img.thumbnail((200, 400))
    img = img.convert("RGB")
    w, h = img.size

    points = []
    for count, color in img.getcolors(w * h):
        for _ in range(count):
            points.append(Point(color))
    return points


def euclidean(p, q):
    n_dim = len(p.coordinates)
    return sqrt(sum([(p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)]))


def rgb_to_hex(rgb):
    return (list(rgb))


def get_colors(filename, n_colors):
    points = get_points(filename)
    clusters = KMeans(n_colors).fit(points)
    clusters.sort(key=lambda c: len(c.points), reverse=True)
    rgbs = [map(int, c.center.coordinates) for c in clusters]
    return list(map(rgb_to_hex, rgbs))


def ColorReco(frame):
    cv2.imwrite("Temp.jpg", frame)
    path = "Temp.jpg"
    CImage(path, width=350, height=700)
    colors = get_colors(path, 1)


    hexnames = webcolors.HTML4_HEX_TO_NAMES
    names = []
    positions = []

    for hex, name in hexnames.items():
        names.append(name)
        positions.append(webcolors.hex_to_rgb(hex))

    spacedb = KDTree(positions)

    # query nearest point
    col = (colors[0])
    dist, index = spacedb.query(col)

    os.remove("Temp.jpg")
    return 'The color is %s.' % (names[index])
