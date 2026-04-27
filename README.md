# 🚗 VOLog
### Vehicle & Occupancy Logging System
> A vision-based gate entry security system built for large outdoor events. Detects vehicle occupants through windscreens, reads number plates, and logs every entry to a live dashboard — replacing paper logs and radio coordination with a real-time digital pipeline.

---

## 📌 What It Does

- **Occupancy Detection** — YOLOv8s model counts visible passengers through the windscreen of each vehicle
- **Number Plate Recognition** — Plate Recognizer API reads and returns the UK number plate string
- **Centralised Logging** — Every entry (plate, headcount, gate, timestamp) is written to a SQLite database
- **Live Dashboard** — React frontend polls the Flask backend every 5 seconds and displays the entry log in real time
- **Gate Filtering** — Filter the log by gate number for targeted oversight
- **Submit Entry UI** — Upload an image and select a gate directly from the dashboard — no terminal needed

---

## 🧱 Architecture

```
VOLog/
├── app.py                          # Flask entry point
├── volog.db                        # SQLite database (auto-created)
├── weights/
│   └── best.pt                     # Trained YOLOv8s model weights
├── uploads/                        # Temporary image storage
└── mvc/
    ├── controller/
    │   └── entry_controller.py     # Route handlers
    ├── model/
    │   ├── inference.py            # YOLOv8 + Plate Recognizer logic
    │   └── database.py             # SQLite read/write
    └── view/
        └── volog-dashboard/        # React frontend (Vite)
```

**Pipeline flow:**

```
Image Upload → Flask Controller → YOLOv8 Inference (headcount)
                                → Plate Recognizer API (number plate)
                                → SQLite Write
                                → React Dashboard (polled every 5s)
```

---

## 🤖 Model

| Detail | Value |
|---|---|
| Architecture | YOLOv8s (small) |
| Pretrained on | COCO |
| Fine-tuned on | 297 curated parking lot surveillance images |
| Train / Val / Test split | 238 / 28 / 31 |
| Training hardware | NVIDIA Tesla T4 (Kaggle Kernels) |
| Inference hardware | Intel Iris Xe (local CPU via PyTorch) |
| Classes | `person`, `car` |
| mAP@0.5 | 0.945 |
| Person recall | 0.821 |
| Car recall | 1.000 |
| Training converged at | Epoch 38 (best checkpoint: Epoch 18) |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Plate Recognizer](https://platerecognizer.com) account (free tier: 2,500 calls/month)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/VOLog.git
cd VOLog
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install flask flask-cors ultralytics requests
```

### 4. Add your Plate Recognizer API token

Open `mvc/model/inference.py` and replace:

```python
PLATE_RECOGNIZER_TOKEN = 'your_api_token_here'
```

with your actual token from your Plate Recognizer dashboard.

### 5. Add model weights

Place your trained `best.pt` file in the `weights/` folder. If you need to retrain, the Kaggle notebook is included in the repository.

### 6. Start the Flask backend

```bash
python app.py
```

Flask runs on `http://127.0.0.1:5000`

### 7. Start the React dashboard

```bash
cd mvc/view/volog-dashboard
npm install
npm run dev
```

React runs on `http://localhost:5173`

---

## 📱 Running on a Phone (Same Network)

To access the dashboard on a mobile device during a demo:

1. Connect your phone and laptop to the same WiFi or use iPhone hotspot
2. Find your laptop IP: run `ipconfig` (Windows) or `ifconfig` (Mac) and note the IPv4 address
3. In `mvc/view/volog-dashboard/src/App.jsx` change:
   ```js
   const API = "http://127.0.0.1:5000"
   ```
   to:
   ```js
   const API = "http://YOUR_IP_HERE:5000"
   ```
4. In `app.py` change:
   ```python
   app.run(debug=True)
   ```
   to:
   ```python
   app.run(debug=True, host='0.0.0.0')
   ```
5. Restart Flask and run Vite with:
   ```bash
   npm run dev -- --host
   ```
6. Open the Network URL printed by Vite on your phone browser

---

## 🧪 Testing the Pipeline (Without Dashboard)

Send a test image via curl:

```bash
curl -X POST http://127.0.0.1:5000/api/entry \
  -F "image=@path/to/your/image.jpg" \
  -F "gate_id=1"
```

Expected response:
```json
{
  "headcount": 2,
  "number_plate": "AB12CDE"
}
```

Check all logged entries:
```bash
curl http://127.0.0.1:5000/api/entries
```

---

## 🔮 Future Work

- **Federated learning** — distribute model training across gate devices so each gate improves the shared model locally without sending raw data centrally
- **Exit logging** — track vehicle departures to maintain an accurate on-site occupant count
- **Live video stream** — replace image upload with a continuous camera feed
- **Edge deployment** — optimise inference using Intel OpenVINO or model quantisation for low-power gate hardware
- **Larger, more diverse dataset** — address demographic representation gaps and add edge cases (child passengers, reclining occupants, high window tint) using synthetic data generation (CARLA / NVIDIA Omniverse)
- **IR/NIR camera support** — improve detection through tinted glass in varied lighting conditions

---

## 👩‍💻 Author

**Hala Bakhtiar**
BSc Software Engineering — University of Roehampton
Final Year Project, 2026
Supervisor: Dr Sameena

---

> *VOLog was built as a Final Year Project to address real coordination and security gaps at large outdoor events. The system is a research prototype and is not intended for production deployment in its current form.*