# fingerprint_verify.py
import cv2
import numpy as np
import os

def match_fingerprint(uploaded_path, template_path, threshold=0.2):
    try:
        img1 = cv2.imread(uploaded_path, 0)  # Gambar yang diupload user
        img2 = cv2.imread(template_path, 0)  # Template yang tersimpan

        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            return False

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        good_matches = [m for m in matches if m.distance < 60]
        similarity = len(good_matches) / max(len(kp1), len(kp2))

        return similarity >= threshold
    except Exception as e:
        print(f"[ERROR] match_fingerprint: {e}")
        return False