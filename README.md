# 🌸 MagicBloom

MagicBloom is a real-time Computer Vision project developed using Python, OpenCV, and MediaPipe.

The application detects two hands through the webcam and displays a flower between the hands. The flower grows as the distance between the hands increases and shrinks as the hands come closer together.

---

## ✨ Features

- 👋 Real-time hand tracking using MediaPipe
- 🌸 Flower displayed between two hands
- 🌱 Flower size changes based on hand distance
- 🎥 Live webcam feed
- ⚡ Lightweight and easy to run

---

## 🛠 Technologies Used

- Python 3.11
- OpenCV
- MediaPipe
- NumPy

---

## 📁 Project Structure

```
MagicBloom/
│
├── assets/
│   └── flower.png
│
├── hand_tracker.py
├── flower.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/MagicBloom.git
```

### 2. Go to the project directory

```bash
cd MagicBloom
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```bash
python main.py
```

Press **Q** to quit the application.

---

## 📸 How It Works

1. Open the webcam.
2. Detect up to two hands using MediaPipe.
3. Calculate the center point between the hands.
4. Measure the distance between the hands.
5. Display a flower at the center.
6. Increase the flower size as the hands move apart.

---

## 🚀 Future Enhancements

- ✨ Bloom animation
- 🌈 Glow effect
- 🌿 Stem and leaves
- 🦋 Butterfly animation
- 🎵 Background music
- 📷 Screenshot feature
- 🎮 Gesture-controlled interactions

---

## 👨‍💻 Author

**Sriram Gandhi Prabha Veluchamy**

Assistant Professor

M.E. Computer Science (Artificial Intelligence & Data Analytics)

Sri Vidya College of Engineering and Technology

Virudhunagar, Tamil Nadu, India

---

## 📜 License

This project is developed for educational and demonstration purposes.

Feel free to modify and extend it for learning and research.