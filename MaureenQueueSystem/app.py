import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import time

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maureen Queue Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DATABASE
# ============================================================

DB_NAME = "maureen_queue.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_number INTEGER NOT NULL,
            patient_name TEXT NOT NULL,
            service TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            served_at TEXT
        )
    """)

    conn.commit()
    conn.close()


initialize_database()


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def add_patient(name, service):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(queue_number), 0) + 1
        FROM patients
    """)

    queue_number = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO patients
        (queue_number, patient_name, service, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        queue_number,
        name,
        service,
        "Waiting",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return queue_number


def get_patients():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT
            queue_number AS Queue,
            patient_name AS Patient,
            service AS Service,
            status AS Status,
            created_at AS "Arrival Time",
            served_at AS "Served Time"
        FROM patients
        ORDER BY queue_number ASC
    """, conn)

    conn.close()

    return df


def call_next_patient():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, queue_number
        FROM patients
        WHERE status = 'Waiting'
        ORDER BY queue_number ASC
        LIMIT 1
    """)

    patient = cursor.fetchone()

    if patient:
        patient_id, queue_number = patient

        cursor.execute("""
            UPDATE patients
            SET status = 'Serving'
            WHERE id = ?
        """, (patient_id,))

        conn.commit()

    conn.close()

    return patient


def complete_patient(queue_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status = 'Completed',
            served_at = ?
        WHERE queue_number = ?
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        queue_number
    ))

    conn.commit()
    conn.close()


def reset_queue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients")

    conn.commit()
    conn.close()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #f7f1ec;
    }

    [data-testid="stSidebar"] {
        background-color: #4b1724;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #4b1724;
        margin-bottom: 0;
    }

    .subtitle {
        color: #756b68;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .metric-card {
        background-color: white;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.06);
        border-left: 5px solid #8f4b57;
    }

    .metric-title {
        color: #756b68;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .metric-value {
        color: #4b1724;
        font-size: 30px;
        font-weight: 700;
        margin-top: 5px;
    }

    .queue-number {
        font-size: 55px;
        font-weight: 800;
        color: #4b1724;
        text-align: center;
    }

    .queue-label {
        text-align: center;
        color: #756b68;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .section-title {
        color: #4b1724;
        font-size: 22px;
        font-weight: 700;
        margin-top: 15px;
    }

    .footer {
        text-align: center;
        color: #8a7d78;
        margin-top: 50px;
        padding: 20px;
        font-size: 13px;
    }

    div.stButton > button {
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h1 style="font-size:30px;">🏥 MAUREEN</h1>
        <p style="font-size:14px;">
        Queue Management System
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Register Patient",
            "Queue Management",
            "Records"
        ]
    )

    st.divider()

    st.markdown(
        """
        **Services**

        👁️ Optical  
        🩺 General Consultation  
        🦷 Dental
        """
    )


# ============================================================
# GET DATA
# ============================================================

patients = get_patients()

if not patients.empty:
    waiting = len(patients[patients["Status"] == "Waiting"])
    serving = len(patients[patients["Status"] == "Serving"])
    completed = len(patients[patients["Status"] == "Completed"])
else:
    waiting = 0
    serving = 0
    completed = 0


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Good day 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Maureen Healthcare Queue Management Dashboard</div>',
        unsafe_allow_html=True
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Patients</div>
                <div class="metric-value">{len(patients)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Waiting</div>
                <div class="metric-value">{waiting}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Serving</div>
                <div class="metric-value">{serving}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Completed</div>
                <div class="metric-value">{completed}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Current queue
    left, right = st.columns([1, 2])

    with left:

        st.markdown(
            '<div class="section-title">Current Patient</div>',
            unsafe_allow_html=True
        )

        if not patients.empty and serving > 0:

            current = patients[
                patients["Status"] == "Serving"
            ].iloc[0]

            st.markdown(
                f"""
                <div style="
                    background:white;
                    border-radius:15px;
                    padding:25px;
                    margin-top:15px;
                    box-shadow:0 3px 15px rgba(0,0,0,0.06);
                ">
                    <div class="queue-label">Now Serving</div>
                    <div class="queue-number">
                        #{int(current["Queue"])}
                    </div>

                    <p style="text-align:center;font-weight:600;">
                        {current["Patient"]}
                    </p>

                    <p style="text-align:center;color:#756b68;">
                        {current["Service"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Complete Patient",
                use_container_width=True
            ):
                complete_patient(int(current["Queue"]))
                st.success("Patient marked as completed.")
                time.sleep(0.5)
                st.rerun()

        else:

            st.markdown(
                """
                <div style="
                    background:white;
                    border-radius:15px;
                    padding:35px;
                    margin-top:15px;
                    text-align:center;
                    box-shadow:0 3px 15px rgba(0,0,0,0.06);
                ">
                    <div style="font-size:40px;">🩺</div>
                    <p style="color:#756b68;">
                        No patient currently being served.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:

        st.markdown(
            '<div class="section-title">Waiting Queue</div>',
            unsafe_allow_html=True
        )

        waiting_df = patients[
            patients["Status"] == "Waiting"
        ]

        if not waiting_df.empty:

            st.dataframe(
                waiting_df[
                    ["Queue", "Patient", "Service", "Arrival Time"]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No patients currently waiting.")


# ============================================================
# REGISTER PATIENT
# ============================================================

elif page == "Register Patient":

    st.markdown(
        '<div class="main-title">Register Patient</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Add a patient to the queue</div>',
        unsafe_allow_html=True
    )

    with st.form("patient_form"):

        name = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
        )

        service = st.selectbox(
            "Select Service",
            [
                "Optical",
                "General Consultation",
                "Dental"
            ]
        )

        submitted = st.form_submit_button(
            "Register Patient",
            use_container_width=True
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter the patient's name."
                )

            else:

                number = add_patient(
                    name.strip(),
                    service
                )

                st.success(
                    f"Patient registered successfully. Queue number: #{number}"
                )

                st.balloons()


# ============================================================
# QUEUE MANAGEMENT
# ============================================================

elif page == "Queue Management":

    st.markdown(
        '<div class="main-title">Queue Management</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Control and manage the active patient queue</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div style="
                background:white;
                padding:25px;
                border-radius:15px;
                text-align:center;
            ">
                <div style="
                    color:#756b68;
                    font-size:13px;
                    text-transform:uppercase;
                ">
                    Patients Waiting
                </div>

                <div style="
                    font-size:45px;
                    font-weight:800;
                    color:#4b1724;
                ">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"{waiting}</div></div>",
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "📢 CALL NEXT PATIENT",
            use_container_width=True
        ):

            patient = call_next_patient()

            if patient:

                st.success(
                    f"Now serving patient #{patient[1]}"
                )

                time.sleep(0.5)
                st.rerun()

            else:

                st.warning(
                    "There are no patients waiting."
                )

    with col2:

        st.markdown(
            """
            <div style="
                background:white;
                padding:25px;
                border-radius:15px;
                text-align:center;
            ">
                <div style="
                    color:#756b68;
                    font-size:13px;
                    text-transform:uppercase;
                ">
                    Completed Today
                </div>

                <div style="
                    font-size:45px;
                    font-weight:800;
                    color:#4b1724;
                ">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"{completed}</div></div>",
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🗑️ RESET QUEUE",
            use_container_width=True
        ):

            reset_queue()

            st.success(
                "Queue has been reset."
            )

            time.sleep(0.5)
            st.rerun()

    st.divider()

    if not patients.empty:

        st.dataframe(
            patients[
                [
                    "Queue",
                    "Patient",
                    "Service",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# RECORDS
# ============================================================

elif page == "Records":

    st.markdown(
        '<div class="main-title">Patient Records</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">View registered patients and queue history</div>',
        unsafe_allow_html=True
    )

    if patients.empty:

        st.info(
            "No patient records available yet."
        )

    else:

        service_filter = st.selectbox(
            "Filter by Service",
            [
                "All",
                "Optical",
                "General Consultation",
                "Dental"
            ]
        )

        status_filter = st.selectbox(
            "Filter by Status",
            [
                "All",
                "Waiting",
                "Serving",
                "Completed"
            ]
        )

        filtered = patients.copy()

        if service_filter != "All":

            filtered = filtered[
                filtered["Service"] == service_filter
            ]

        if status_filter != "All":

            filtered = filtered[
                filtered["Status"] == status_filter
            ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Records as CSV",
            filtered.to_csv(index=False),
            file_name="maureen_patient_records.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Maureen Queue Management System<br>
        Designed & Developed by <strong>Velma Wanyonyi</strong>
    </div>
    """,
    unsafe_allow_html=True
)