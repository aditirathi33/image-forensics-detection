import cv2
import numpy as np
import os
from sklearn.cluster import DBSCAN
from scipy.spatial import Delaunay

# ---------- Tunables ----------
MAX_WIDTH          = 1024
FEATURES_TARGET    = 4000
LOWE_RATIO         = 0.78
MIN_PAIR_DIST_PX   = 12
MAX_PAIR_DIST_PX   = 240
DBSCAN_EPS         = 42
DBSCAN_MIN_SAMPLES = 6
DRAW_MATCH_LINES   = False  # set True if you still want yellow lines too

def _resize(img):
    h, w = img.shape[:2]
    if max(h, w) <= MAX_WIDTH:
        return img, 1.0
    s = MAX_WIDTH / float(max(h, w))
    return cv2.resize(img, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA), s

def _prep(gray):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return gray

def _get_detector():
    if hasattr(cv2, "SIFT_create"):
        det = cv2.SIFT_create(nfeatures=FEATURES_TARGET, contrastThreshold=0.02, edgeThreshold=10)
        matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=100))
        knn = True
    else:
        det = cv2.ORB_create(nfeatures=FEATURES_TARGET, scaleFactor=1.2, edgeThreshold=15)
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        knn = True
    return det, matcher, knn

def _good_pairs(kp, des, matcher, knn=True):
    if knn:
        m2 = matcher.knnMatch(des, des, k=2)
    else:
        m2 = [[m] for m in matcher.match(des, des)]
    pairs = []
    for ms in m2:
        if len(ms) < 2: continue
        a, b = ms[0], ms[1]
        if a.queryIdx == a.trainIdx:  # same keypoint
            continue
        # Lowe ratio test
        if a.distance >= LOWE_RATIO * b.distance:
            continue
        p1 = np.array(kp[a.queryIdx].pt, np.float32)
        p2 = np.array(kp[a.trainIdx].pt, np.float32)
        d = np.linalg.norm(p1 - p2)
        if d < MIN_PAIR_DIST_PX or d > MAX_PAIR_DIST_PX:
            continue
        # order to deduplicate
        if p1[0] > p2[0] or (p1[0] == p2[0] and p1[1] > p2[1]):
            p1, p2 = p2, p1
        pairs.append((p1, p2))
    # dedupe almost-identical pairs
    if not pairs:
        return []
    arr = np.array([np.hstack((p1, p2)) for p1, p2 in pairs])
    _, idx = np.unique(arr.round(0), axis=0, return_index=True)
    return [pairs[i] for i in sorted(idx)]

def _draw_delaunay(vis, pts, color=(0,0,255), thickness=2):
    """Draw triangles over points using Delaunay triangulation."""
    if len(pts) < 3:
        return 0
    tri = Delaunay(pts)
    count = 0
    for simp in tri.simplices:
        a = tuple(np.int32(pts[simp[0]]))
        b = tuple(np.int32(pts[simp[1]]))
        c = tuple(np.int32(pts[simp[2]]))
        # discard tiny skinny triangles
        area = abs(0.5*((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])))
        if area < 60:  # px^2
            continue
        cv2.polylines(vis, [np.array([a,b,c])], True, color, thickness, lineType=cv2.LINE_AA)
        count += 1
    return count

def copymove_mask(in_path, out_path="out/copymove_mask.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = cv2.imread(in_path)
    if img is None:
        blank = np.zeros((200,200,3), np.uint8)
        cv2.imwrite(out_path, blank)
        return out_path

    work, scale = _resize(img.copy())
    gray = _prep(cv2.cvtColor(work, cv2.COLOR_BGR2GRAY))

    det, matcher, use_knn = _get_detector()
    kp, des = det.detectAndCompute(gray, None)
    vis = work.copy()

    if des is None or len(kp) < 8:
        cv2.putText(vis, "No copy-move evidence (too few features)",
                    (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30,220,30), 2)
        out_img = cv2.resize(vis, (img.shape[1], img.shape[0]))
        cv2.imwrite(out_path, out_img)
        return out_path

    pairs = _good_pairs(kp, des, matcher, use_knn)

    if DRAW_MATCH_LINES:
        for p1, p2 in pairs[:1000]:
            cv2.line(vis, tuple(np.int32(p1)), tuple(np.int32(p2)), (0,255,255), 1, cv2.LINE_AA)

    if len(pairs) < 12:
        cv2.putText(vis, "No strong clone patterns found",
                    (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30,220,30), 2)
        out_img = cv2.resize(vis, (img.shape[1], img.shape[0]))
        cv2.imwrite(out_path, out_img)
        return out_path

    # Cluster midpoints → candidate clone regions
    mids = np.array([(p1+p2)/2.0 for p1, p2 in pairs], np.float32)
    clustering = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN_SAMPLES).fit(mids)
    labels = clustering.labels_
    uniq = [l for l in set(labels) if l != -1]

    triangles_drawn = 0
    for l in uniq:
        pts = mids[labels == l]
        # draw Delaunay triangles for this cluster
        triangles_drawn += _draw_delaunay(vis, pts)

    if triangles_drawn > 0:
        cv2.putText(vis, "Suspicious clone clusters (red triangles)",
                    (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (40,220,255), 2)
    else:
        cv2.putText(vis, "No strong clone clusters found",
                    (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30,220,30), 2)

    out_img = cv2.resize(vis, (img.shape[1], img.shape[0]))
    cv2.imwrite(out_path, out_img)
    return out_path
