# 🚀 Hybrid Anime Recommendation System - End-to-End MLOps Project

Welcome to the **Hybrid Anime Recommendation System**, a full-scale end-to-end MLOps implementation project that delivers smart anime suggestions using content and collaborative filtering approaches — all powered by CI/CD automation and scalable deployment on **Google Kubernetes Engine (GKE)**.

🔗 **Live GitHub Repo:** [Click here to view](https://github.com/Chetan713205/mlops-project-2)

---

## 📌 Highlights

✅ **Hybrid Recommendation Model**
✅ **CI/CD Pipeline with Jenkins**
✅ **Dockerized Microservices**
✅ **Data & Model Versioning with DVC + GCP**
✅ **Kubernetes Deployment on GKE**
✅ **Real-time Flask Web App**
✅ **Automated Pipeline Triggers on GitHub Push**

> **🔍 For Jenkins CI/CD pipeline verification, refer to the attached file: [`Jenkins web logs.txt`](./Jenkins%20web%20logs.txt)**

---

## 🧠 Project Overview

This project combines content-based and collaborative filtering techniques to build a robust hybrid recommendation engine for anime lovers. Built with Python, Flask, and TensorFlow, and productionized using best practices in MLOps.

---

## ⚙️ Tech Stack

| Area            | Tools & Technologies             |
| --------------- | -------------------------------- |
| Backend         | Python, Flask                    |
| ML/DL           | Pandas, Scikit-learn, TensorFlow |
| CI/CD           | Jenkins, Docker, GitHub          |
| Orchestration   | Kubernetes (GKE)                 |
| Version Control | Git, DVC                         |
| Cloud           | Google Cloud Platform (GCP)      |
| Deployment      | Docker, GCR, GKE                 |

---

## 📂 Project Structure

```
├── application.py            # Flask App Entry
├── Jenkinsfile               # CI/CD Pipeline Definition
├── Dockerfile                # Project Dockerfile
├── deployment.yml            # Kubernetes Manifest
├── artifacts/                # Model artifacts tracked via DVC
├── pipeline/                 # Training and prediction pipeline
├── static/                   # CSS styling
├── templates/                # HTML front-end
├── utils/                    # Helper functions
├── requirements.txt          # Python dependencies
├── .dvc/ and .dvc files      # DVC metadata
├── Jenkins web logs.txt      # ✅ CI/CD build verification log
```

---

## 🔁 CI/CD Workflow Overview

**1. Jenkins Setup:**

* Docker-in-Docker Jenkins container
* Auto-trigger builds on GitHub push
* Virtual environment, training, and testing setup inside pipeline

**2. Docker & GCR:**

* Containerized app via Dockerfile
* Pushed to **Google Container Registry**

**3. Kubernetes:**

* `deployment.yml` creates GKE workload
* LoadBalancer service exposes the app

**4. Artifacts & Versioning:**

* Data/model artifacts tracked via **DVC**
* Stored in **GCP Bucket** and connected using `dvc remote`

---

## 📦 DVC Integration (Data Version Control)

* Buckets created and authenticated via GCP Service Accounts
* Raw/processed data, model weights, and checkpoints versioned with `.dvc` files
* Use `dvc push` / `dvc pull` to sync local and remote artifacts
* **Refer to** [`DVC.txt`](./DVC.txt) **for the detailed setup**

---

## 🖥️ Jenkins Deployment Logs

> ✅ CI/CD pipeline execution including:

* Repo cloning
* Virtual environment setup
* Dependency installation
* Model training
* Docker image building
* Kubernetes deployment

📄 **Check the full Jenkins log here:** [`Jenkins web logs.txt`](./Jenkins%20web%20logs.txt)

---

## 📌 How to Run This Project Locally

```bash
# Clone the repo
git clone https://github.com/Chetan713205/mlops-project-2.git
cd mlops-project-2

# Install dependencies
pip install -r requirements.txt

# Run Flask App
python application.py
```

---

## 🌐 Deployed On

✅ **Google Kubernetes Engine (GKE)**
✅ **Dockerized via GCR (Google Container Registry)**

---

## 📷 Link to the deployment

http://34.16.66.59/

---

## 🙌 Acknowledgments

Thanks to Anything AI Cyber Pvt. Ltd. for providing me the experience to complete this project.
