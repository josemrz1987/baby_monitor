# 👶🐾 AI Camera Baby & Pet Activity Monitor

A lightweight and robust computer vision system developed in **Python** for monitoring rooms, **babies**, or **pets** using IP cameras (compatible with Tapo cameras via RTSP). Its design focuses on filtering out false positives (such as adults casually walking across the room) to detect only **continuous, repetitive, and localized movements**—providing early automated alerts via **Telegram** when immediate attention might be needed.

---

## 🎯 Practical Use Cases & Critical Alerts

Rather than triggering on transient motion, the system tracks sustained restlessness to capture early warning signs:

* **👶 Infant Care & Safety:**
  * **Fever & Discomfort:** Early detection of continuous tossing, turning, or physical restlessness caused by high fever or pain.
  * **Distress & Breathing / Choking Hazards:** Immediate notifications triggered by abnormal, vigorous limb movements or struggling in the crib (e.g., blanket covers, choking hazards, or positional distress).
* **🐾 Pet Behavior Monitoring:**
  * **Urgent Bathroom Needs:** Detects repetitive pacing, scratching, or pacing near doors indicating an urgent need to go outside.
  * **Anxiety or Pain Signals:** Flags continuous, abnormal movement patterns caused by separation anxiety or physical distress while you are away.

---

## 🚀 Key Features

* **Direct RTSP Connection:** Low-latency real-time streaming using `cv2.VideoCapture`.
* **Intelligent Background Subtraction:** Optimized implementation of **OpenCV MOG2** with history and median filtering to isolate real silhouettes.
* **Range-Specific Size Filter (`MIN_AREA_MOVIMIENTO` / `MAX_AREA_MOVIMIENTO`):** 
  * Ignores small objects (insects, lighting changes).
  * Discards massive passing movements (adults walking across the room).
  * Focuses exclusively on localized, steady movements typical of restless pets or babies.
* **"Water Bucket" Persistence Algorithm:** A progressive integration system that evaluates movement consistency over time before triggering an alarm, preventing false alerts from isolated spikes.
* **Telegram Notifications:** Instant asynchronous alert delivery via the Telegram Bot API with built-in anti-spam protection.
* **Environment Security:** Credential and token loading using `python-dotenv` (the `.env` file is excluded from version control).