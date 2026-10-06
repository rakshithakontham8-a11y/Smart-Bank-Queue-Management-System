import streamlit as st
from datetime import datetime
from database import Customer, SessionLocal
import qrcode
from io import BytesIO


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Smart Bank Queue Management System",
    page_icon="🏦",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* ===============================
   MAIN BACKGROUND
================================ */

.stApp {
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at bottom right, #4c1d95 0%, transparent 40%),
        linear-gradient(135deg, #020617, #0f172a, #1e1b4b) !important;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}


/* ===============================
   HEADER
================================ */

.main-title {
    font-size: 38px;
    font-weight: 900;
    text-align: center;

    background: linear-gradient(
        90deg,
        #38bdf8,
        #818cf8,
        #c084fc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1 !important;
    font-size: 17px;
}


/* ===============================
   HEADINGS
================================ */

h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 800 !important;
}

p {
    color: #cbd5e1 !important;
}


/* ===============================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #020617,
            #172554,
            #312e81
        ) !important;

    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}


/* ===============================
   SIDEBAR RADIO
================================ */

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(148,163,184,0.2);
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(56,189,248,0.18) !important;
    border-color: #38bdf8;
}


/* ===============================
   BUTTONS
================================ */

.stButton > button {
    width: 100% !important;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 12px !important;

    box-shadow:
        0 5px 15px rgba(59,130,246,0.25);
}

.stButton > button:hover {
    background:
        linear-gradient(
            90deg,
            #06b6d4,
            #6366f1
        ) !important;

    transform: translateY(-2px);
}


/* ===============================
   INPUT BOXES
================================ */

.stTextInput input {
    background: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
}

.stTextInput input:focus {
    border: 2px solid #38bdf8 !important;

    box-shadow:
        0 0 10px rgba(56,189,248,0.25);
}


/* ===============================
   SELECT BOX
================================ */

div[data-baseweb="select"] {
    background: #1e293b !important;
    border-radius: 10px !important;
    border: 1px solid #475569 !important;
}


/* ===============================
   METRIC CARDS
================================ */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #1e293b,
            #312e81
        ) !important;

    border-radius: 18px !important;
    padding: 20px !important;

    border: 1px solid #475569 !important;
    border-top: 4px solid #38bdf8 !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.35) !important;
}

div[data-testid="stMetric"] label {
    color: #cbd5e1 !important;
}

div[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 900 !important;
}


.qr-box {
    background: rgba(255,255,255,0.04);

    border: 1px solid #334155;

    border-radius: 20px;

    padding: 20px;

    text-align: center;

    margin-top: 20px;
}


/* ===============================
   DOWNLOAD BUTTON
================================ */

.stDownloadButton > button {
    background:
        linear-gradient(
            90deg,
            #0891b2,
            #4f46e5
        ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
}


/* ===============================
   ALERTS
================================ */

div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid #475569 !important;
}


/* ===============================
   DIVIDERS
================================ */

hr {
    border-color: #334155 !important;
}


/* ===============================
   DATAFRAME
================================ */

div[data-testid="stDataFrame"] {
    border-radius: 15px !important;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# DATABASE
# ==========================================================

db = SessionLocal()


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">🏦 Smart Bank Queue Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart customer queue and token management for modern banks.</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🏦 Bank Menu")

page = st.sidebar.radio(
    "Select Page",
    [
        "Customer Registration",
        "Live Queue",
        "Now Serving",
        "Admin Dashboard"
    ]
)


# ==========================================================
# CUSTOMER REGISTRATION
# ==========================================================

if page == "Customer Registration":

    st.header("🎫 Customer Registration")

    st.write(
        "Register a customer and generate a queue token."
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Customer Name",
            placeholder="Enter customer name"
        )

        phone = st.text_input(
            "Mobile Number",
            placeholder="Enter mobile number"
        )

    with col2:

        service = st.selectbox(
            "Banking Service",
            [
                "Cash Deposit",
                "Cash Withdrawal",
                "Account Opening",
                "Loan Enquiry",
                "Passbook Update",
                "Other"
            ]
        )

        priority = st.selectbox(
            "Customer Type",
            [
                "Normal",
                "Senior Citizen",
                "Emergency"
            ]
        )

    st.divider()

    if st.button(
        "🎫 Generate Token",
        use_container_width=True
    ):

        if name.strip() == "":

            st.warning(
                "Please enter customer name."
            )

        else:

            last_customer = (
                db.query(Customer)
                .order_by(Customer.token.desc())
                .first()
            )

            if last_customer:

                token = last_customer.token + 1

            else:

                token = 1


            # SAVE CUSTOMER
            customer = Customer(
                token=token,
                name=name,
                phone=phone,
                service=service,
                priority=priority,
                time=datetime.now().strftime("%H:%M:%S"),
                date=datetime.now().strftime("%Y-%m-%d"),
                status="Waiting"
            )

            db.add(customer)
            db.commit()


            st.success(
                f"✅ Token T{token:03d} generated successfully!"
            )


            # ==================================================
            # CREATE QR CODE
            # ==================================================

            qr_data = f"""
Smart Bank Queue Management System

Token: T{token:03d}
Customer: {name}
Service: {service}
Customer Type: {priority}
"""

            qr = qrcode.make(qr_data)

            buffer = BytesIO()

            qr.save(
                buffer,
                format="PNG"
            )

            qr_image = buffer.getvalue()


            # ==================================================
            # QR + TOKEN DETAILS
            # ==================================================

            st.subheader("🎫 Your Queue Token")

            qr_col, token_col = st.columns(
                [1, 1],
                gap="large"
            )


            # --------------------------------------------------
            # LEFT SIDE - QR CODE
            # --------------------------------------------------

            with qr_col:

                st.markdown(
                    '<div class="qr-box">',
                    unsafe_allow_html=True
                )

                st.image(
                    qr_image,
                    caption=f"QR Token - T{token:03d}",
                    width=250
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

                st.download_button(
                    label="⬇️ Download QR Token",
                    data=qr_image,
                    file_name=f"token_T{token:03d}.png",
                    mime="image/png",
                    use_container_width=True
                )


            # --------------------------------------------------
            # RIGHT SIDE - TOKEN CARD
            # --------------------------------------------------

            with token_col:

                st.markdown("### 🎫 Token Details")

                st.metric(
                    "YOUR TOKEN NUMBER",
                    f"T{token:03d}"
                )

                st.markdown(f"**👤 Customer:** {name}")
                st.markdown(f"**🏦 Service:** {service}")
                st.markdown(f"**Customer Type:** {priority}")

                st.info(
                    "Thank you for waiting. Please watch the Live Queue for your turn."
                )


# ==========================================================
# LIVE QUEUE
# ==========================================================

elif page == "Live Queue":

    st.header("📊 Live Queue")

    waiting_customers = (
        db.query(Customer)
        .filter(Customer.status == "Waiting")
        .order_by(Customer.token)
        .all()
    )

    if not waiting_customers:

        st.info(
            "No customers are currently waiting."
        )

    else:

        st.write(
            f"**{len(waiting_customers)} customer(s) waiting**"
        )

        st.divider()

        for position, customer in enumerate(
            waiting_customers,
            start=1
        ):

            estimated_time = position * 5

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.write(
                    f"### T{customer.token:03d}"
                )

            with col2:

                st.write(
                    f"**{customer.name}**"
                )

            with col3:

                st.write(
                    f"Position: **{position}**"
                )

            with col4:

                st.write(
                    f"Wait: **~{estimated_time} min**"
                )

            st.divider()


# ==========================================================
# NOW SERVING
# ==========================================================

elif page == "Now Serving":

    st.header("📢 Now Serving")

    st.write(
        "Manage the customer currently being served."
    )

    serving_customer = (
        db.query(Customer)
        .filter(Customer.status == "Serving")
        .first()
    )


    # CURRENTLY SERVING
    if serving_customer:

        st.success(
            "🟢 CUSTOMER IS CURRENTLY BEING SERVED"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎫 Token",
                f"T{serving_customer.token:03d}"
            )

        with col2:

            st.metric(
                "👤 Customer",
                serving_customer.name
            )

        with col3:

            st.metric(
                "🏦 Service",
                serving_customer.service
            )

        st.divider()

        st.subheader(
            f"🎫 Now Serving: T{serving_customer.token:03d}"
        )

        st.write(
            f"**Customer:** {serving_customer.name}"
        )

        st.write(
            f"**Service:** {serving_customer.service}"
        )

        st.write(
            f"**Customer Type:** {serving_customer.priority}"
        )


        if st.button(
            "✅ Complete Current Service",
            use_container_width=True
        ):

            serving_customer.status = "Completed"

            db.commit()

            st.success(
                f"T{serving_customer.token:03d} service completed successfully!"
            )

            st.rerun()


    # NO CUSTOMER SERVING
    else:

        st.info(
            "No customer is currently being served."
        )

        st.divider()

        next_customer = (
            db.query(Customer)
            .filter(Customer.status == "Waiting")
            .order_by(Customer.token)
            .first()
        )

        if next_customer:

            st.subheader("👤 Next Customer")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "🎫 Token",
                    f"T{next_customer.token:03d}"
                )

            with col2:

                st.metric(
                    "👤 Customer",
                    next_customer.name
                )

            with col3:

                st.metric(
                    "🏦 Service",
                    next_customer.service
                )


            if st.button(
                "📢 Call Next Customer",
                use_container_width=True
            ):

                next_customer.status = "Serving"

                db.commit()

                st.success(
                    f"T{next_customer.token:03d} is now being served!"
                )

                st.rerun()

        else:

            st.info(
                "Queue is empty. No customers are waiting."
            )


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

elif page == "Admin Dashboard":

    st.header("📊 Admin Dashboard")

    st.write(
        "Monitor bank queue performance and customer activity."
    )

    all_customers = db.query(Customer).all()

    total = len(all_customers)

    waiting = len([
        c for c in all_customers
        if c.status == "Waiting"
    ])

    serving = len([
        c for c in all_customers
        if c.status == "Serving"
    ])

    completed = len([
        c for c in all_customers
        if c.status == "Completed"
    ])


    # ======================================================
    # MAIN STATISTICS
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Customers",
            total
        )

    with col2:

        st.metric(
            "⏳ Waiting",
            waiting
        )

    with col3:

        st.metric(
            "🟢 Now Serving",
            serving
        )

    with col4:

        st.metric(
            "✅ Completed",
            completed
        )

    st.divider()


    # ======================================================
    # TODAY'S STATISTICS
    # ======================================================

    today = datetime.now().strftime("%Y-%m-%d")

    today_customers = [
        c for c in all_customers
        if c.date == today
    ]

    st.subheader(
        "📅 Today's Queue Statistics"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Today's Customers",
            len(today_customers)
        )

    with col2:

        today_completed = len([
            c for c in today_customers
            if c.status == "Completed"
        ])

        st.metric(
            "Today's Completed",
            today_completed
        )

    with col3:

        today_waiting = len([
            c for c in today_customers
            if c.status == "Waiting"
        ])

        st.metric(
            "Today's Waiting",
            today_waiting
        )

    st.divider()


    # ======================================================
    # MOST REQUESTED SERVICE
    # ======================================================

    st.subheader(
        "⭐ Most Requested Service"
    )

    if all_customers:

        service_counts = {}

        for customer in all_customers:

            if customer.service in service_counts:

                service_counts[customer.service] += 1

            else:

                service_counts[customer.service] = 1


        most_requested = max(
            service_counts,
            key=service_counts.get
        )


        st.success(
            f"🏆 Most Requested Service: "
            f"**{most_requested}** "
            f"({service_counts[most_requested]} customers)"
        )


        st.write(
            "### Service-wise Customer Count"
        )

        max_count = max(
            service_counts.values()
        )


        for service_name, count in service_counts.items():

            st.write(
                f"**{service_name}** — {count} customer(s)"
            )

            st.progress(
                count / max_count
            )

    else:

        st.info(
            "No service data available yet."
        )

    st.divider()


    # ======================================================
    # QUEUE OVERVIEW
    # ======================================================

    st.subheader(
        "📈 Queue Overview"
    )

    col1, col2 = st.columns(2)

    with col1:

        if total > 0:

            completion_rate = (
                completed / total
            ) * 100

        else:

            completion_rate = 0


        st.metric(
            "Completion Rate",
            f"{completion_rate:.1f}%"
        )


    with col2:

        average_wait = waiting * 5

        st.metric(
            "Estimated Queue Wait",
            f"~{average_wait} min"
        )

    st.divider()


    # ======================================================
    # CUSTOMER RECORDS
    # ======================================================

    st.subheader(
        "👥 Customer Records"
    )

    if all_customers:

        for customer in all_customers:

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:

                st.write(
                    f"**T{customer.token:03d}**"
                )

            with col2:

                st.write(
                    customer.name
                )

            with col3:

                st.write(
                    customer.service
                )

            with col4:

                st.write(
                    customer.status
                )

            with col5:

                if customer.status == "Waiting":

                    if st.button(
                        "📢 Call",
                        key=f"call_{customer.id}"
                    ):

                        current = (
                            db.query(Customer)
                            .filter(
                                Customer.status == "Serving"
                            )
                            .first()
                        )

                        if current:

                            st.warning(
                                "Another customer is already being served."
                            )

                        else:

                            customer.status = "Serving"

                            db.commit()

                            st.rerun()

                elif customer.status == "Serving":

                    st.write(
                        "🟢 Serving"
                    )

                else:

                    st.write(
                        "✅ Done"
                    )

            st.divider()

    else:

        st.info(
            "No customer records available."
        )


# ==========================================================
# CLOSE DATABASE SESSION
# ==========================================================

db.close()