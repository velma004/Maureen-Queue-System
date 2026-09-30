 🏥 Maureen Queue System

A Python-based queue management system designed to help organize patient flow in a healthcare setting.

The system assigns queue numbers to patients based on the service they require, helping reduce confusion and providing a simple way for staff to manage patients waiting for consultation.

 📌 About the Project

The Maureen Queue System simulates a digital hospital reception and queue management system.

Patients can select the service they need and receive a queue number. The system organizes patients into separate service queues, making it easier to manage the order in which patients are attended to.

Available Services

* 👁️ **Optical Consultation (O)**
* 🩺 **General Consultation (G)**
* 🦷 **Dental Consultation (D)**

 🚀 Features

* 🧑🏽‍⚕️ Patient queue registration
* 🎫 Automatic queue number generation
* 🏥 Separate queues for different services
* 📋 Queue management dashboard
* 💾 SQLite database for storing queue information
* 🔄 Real-time queue updates
* 🖥️ Simple and user-friendly interface

 🛠️ Technologies Used

* **Python**
* **Streamlit** – web-based user interface
* **SQLite** – local database management
* **Python SQLite3** – database interaction

📂 Project Structure

```text
Maureen-Queue-System/
│
├── app.py
├── database/
│   └── queue.db
├── requirements.txt
└── README.md
```

 ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/maureen-queue-system.git
cd maureen-queue-system
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
streamlit run app.py
```

The application will open in your browser.

💡 How It Works

1. A patient selects the required service.
2. The system generates a queue number.
3. The patient's information is stored in the SQLite database.
4. The patient is added to the appropriate service queue.
5. Staff can view and manage the waiting queues from the dashboard.

 📚 What I Learned

This project helped me practice:

* Building practical applications with Python
* Creating interactive interfaces with Streamlit
* Working with SQLite databases
* Managing and organizing data
* Designing queue-management logic
* Connecting a user interface to a database
* Turning a real-world problem into a software solution

🔮 Future Improvements

Potential improvements include:

* 📱 Mobile-friendly interface
* 🔔 Patient notifications when their turn approaches
* 📊 Daily and monthly queue statistics
* 👩🏽‍⚕️ Staff login and role management
* 🗃️ Patient history and reporting
* ☁️ Cloud database integration
* 🖨️ Printable queue tickets

👩🏽‍💻 Author

Velma Wanyonyi
Statistics & Programming student interested in data, software development, and building practical technology solutions.

