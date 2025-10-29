# src/copymove_dense.py
import cv2, os, numpy as np

def _zncc(a, b):
    a = a.astype(np.float32); b = b.astype(np.float32)
    a -= a.mean(); b -= b.mean()
    denom = (a.std() * b.std()) + 1e-6
    return float((a*b).sum() / (a.size * denom))

def copymove_dense(in_path, out_path="out/copymove_mask.png",
                   win=32, stride=12, search_radius=140, zncc_thr=0.92):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = cv2.imread(in_path)
    if img is None:
        cv2.imwrite(out_path, np.zeros((200,200,3), np.uint8)); return out_path

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    best_pairs = []  # (x,y,x2,y2,score)
    for y in range(0, h - win, stride):
        for x in range(0, w - win, stride):
            patch = gray[y:y+win, x:x+win]
            # search in a neighborhood (avoid overlapping trivial self-match)
            xs = max(0, x - search_radius); xe = min(w - win, x + search_radius)
            ys = max(0, y - search_radius); ye = min(h - win, y + search_radius)
            best = (None, -1.0)
            for yy in range(ys, ye, stride):
                for xx in range(xs, xe, stride):
                    if abs(xx - x) < win//2 and abs(yy - y) < win//2:
                        continue
                    score = _zncc(patch, gray[yy:yy+win, xx:xx+win])
                    if score > best[1]:
                        best = ((xx, yy), score)
            if best[1] >= zncc_thr:
                (xx, yy), sc = best
                best_pairs.append((x, y, xx, yy, sc))

    vis = img.copy()
    drawn = 0
    for x, y, xx, yy, sc in best_pairs:
        color = (0, 0, 255)  # red
        cv2.rectangle(vis, (x, y), (x+win, y+win), color, 2)
        cv2.rectangle(vis, (xx, yy), (xx+win, yy+win), color, 2)
        drawn += 1
        if drawn > 60: break  # keep it clean

    if drawn == 0:
        cv2.putText(vis, "No copy-move evidence (dense)", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (40,220,40), 2)

    cv2.imwrite(out_path, vis)
    return out_path
