# fingerprint_verify.py

import cv2
import os

FINGERPRINT_DIR = os.path.join(os.path.dirname(__file__), "fingerprints")

def match_fingerprint(uploaded_path, username, threshold=0.2):
    try:

        template_path = os.path.join(FINGERPRINT_DIR, f"{username}.png")

        if not os.path.exists(template_path):
            print("[ERROR] Template fingerprint tidak ditemukan:", template_path)
            return False

        img1 = cv2.imread(uploaded_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if img1 is None or img2 is None:
            print("[ERROR] Gambar tidak dapat dibaca.")
            return False

        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            return False

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        good_matches = [m for m in matches if m.distance < 60]
        similarity = len(good_matches) / max(len(kp1), len(kp2))

        print(f"[INFO] Similarity: {similarity:.2f}")
        return similarity >= threshold

    except Exception as e:
        print(f"[ERROR] match_fingerprint: {e}")
        return False
