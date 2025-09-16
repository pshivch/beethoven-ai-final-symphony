# gesture/pose_extract.py
# Extract conductor hand/upper-body keypoints with MediaPipe and save to .npz.
# pip install mediapipe opencv-python numpy

import argparse, time, numpy as np, cv2

try:
    import mediapipe as mp
except Exception as e:
    mp = None
    print("WARNING: mediapipe not available in this environment. Install it in your runtime.")

def extract(video_path, out_path, fps_target=120):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or fps_target
    pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) if mp else None
    hands = mp.solutions.hands.Hands(max_num_hands=2) if mp else None

    frames, confs = [], []
    while True:
        ret, frame = cap.read()
        if not ret: break
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        kpts = []
        conf = []
        # Pose (upper body)
        if pose:
            res_p = pose.process(rgb)
            L = res_p.pose_landmarks
            if L:
                for lm in L.landmark:
                    kpts.append([lm.x, lm.y])
                    conf.append(lm.visibility)
        # Hands (overwrite/add last 42 points for hands)
        if hands:
            res_h = hands.process(rgb)
            if res_h.multi_hand_landmarks:
                for handLms in res_h.multi_hand_landmarks:
                    for lm in handLms.landmark:
                        kpts.append([lm.x, lm.y])
                        conf.append(1.0)
        if not kpts:
            # pad empty frame with zeros (e.g., 0 joints)
            kpts = np.zeros((0,2)); conf = np.zeros((0,))
        else:
            kpts = np.array(kpts, dtype=np.float32)
            conf = np.array(conf, dtype=np.float32)
        frames.append(kpts)
        confs.append(conf)

    # Pad to same joint count
    J = max(k.shape[0] for k in frames) if frames else 0
    K = np.zeros((len(frames), J, 2), dtype=np.float32)
    C = np.zeros((len(frames), J), dtype=np.float32)
    for i,(k,c) in enumerate(zip(frames, confs)):
        K[i,:k.shape[0],:] = k
        C[i,:c.shape[0]] = c

    # placeholders for labels; fill later during alignment
    dyn = np.zeros((K.shape[0],), np.float32)
    tempo = np.zeros((K.shape[0],), np.float32)
    artic = np.zeros((K.shape[0],), np.float32)
    cue = np.zeros((K.shape[0],), np.float32)

    np.savez_compressed(out_path, keypoints=K, conf=C, fps=int(fps),
                        dyn=dyn, tempo=tempo, artic=artic, cue=cue)
    print(f"Saved {out_path} :: frames={K.shape[0]}, joints={J}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=120)
    args = ap.parse_args()
    extract(args.video, args.out, fps_target=args.fps)
