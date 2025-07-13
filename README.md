# 🎵 Back-End Development – Song Service (Python + Flask)

This project is a backend API service built in **Python** designed to manage a collection of songs. It includes RESTful endpoints for performing CRUD operations on songs and is containerized for deployment via **Docker** or **OpenShift**.

Developed as part of a backend development course, this service demonstrates core concepts in API design, software modularization, unit testing, and cloud-native deployment.

---

## 🧰 Tech Stack

- **Backend Framework**: Flask (or FastAPI, if applicable — please confirm)
- **Language**: Python 3.x
- **Containerization**: Docker (OpenShift-compatible)
- **Testing**: `pytest`
- **Deployment**: GitHub + OpenShift

---

## 📦 Features

- 🎧 Create, read, update, delete (CRUD) for song entities
- 🌐 RESTful API with JSON support
- 🧪 Unit tests using `pytest`
- 🐳 Dockerized for local and cloud deployment
- 🔐 Scalable and modular codebase for easy integration

---

## 🚀 Getting Started

### Clone and run locally

```bash
git clone https://github.com/Silvafox76/back-end-song-service.git
cd back-end-song-service
pip install -r requirements.txt
python app.py
