Final Symphony – CV/ML Toolkit (Starter Pack)
=============================================

This bundle contains three build-ready pieces requested:

1) MusicXML <-> Token converter (music21-based)
2) Constrained beam search for OMR decoding
3) Pose extractor script to build gesture datasets (.npz)

Note: These scripts are templates that assume you have the required
libraries installed in your own environment:

- music21 (for MusicXML parsing/writing)
- numpy, opencv-python, mediapipe (for pose extraction)
- torch (only if you integrate with the training code we discussed)

Directory layout
----------------
tokenization/
  musicxml_tokens.py      # token vocabulary + helpers
  musicxml_token_converter.py  # MusicXML <-> token conversion (loss-aware)

omr/
  constrained_beam.py     # constrained beam search utilities for OMR

gesture/
  pose_extract.py         # MediaPipe/OpenCV-based keypoint extractor to .npz

Usage quickstart
----------------
# Convert MusicXML to tokens
python tokenization/musicxml_token_converter.py --to-tokens input.musicxml --out tokens.json

# Convert tokens back to MusicXML (round trip)
python tokenization/musicxml_token_converter.py --to-musicxml tokens.json --out out.musicxml

# Run constrained beam search (example stub)
python omr/constrained_beam.py

# Extract conductor keypoints to .npz
python gesture/pose_extract.py --video input.mp4 --out data/sample_01.npz --fps 120

License: MIT (feel free to adapt).
