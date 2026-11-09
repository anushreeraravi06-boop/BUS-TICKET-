import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Bus Analytics Dashboard",
    page_icon="🚌",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FC;
}

h1, h2, h3 {
    color: #142D4E;
}

.metric-card {
    background: linear-gradient(135deg, #142D4E, #247BA0);
    padding: 22px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.metric-card h2 {
    color: white;
    font-size: 30px;
}

.metric-card p {
    color: #DCEEFF;
    font-size: 15px;
}

section[data-testid="stSidebar"] {
    background-color: #142D4E;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SAMPLE DATA ----------------

np.random.seed(42)

routes = [
    "Bangalore - Ballari",
    "Ballari - Hospet",
    "Bangalore - Mysore",
    "Ballari - Hubli",
    "Mysore - Bangalore",
    "Hubli - Bangalore",
    "Ballari - Hyderabad"
]

cities = [
    "Bangalore",
    "Ballari",
    "Hospet",
    "Mysore",
    "Hubli",
    "Hyderabad"
]

num_records = 1000

data = pd.DataFrame({
    "Ticket_ID": range(1001, 1001 + num_records),
    "Passenger": [
        f"Passenger {i}" for i in range(1, num_records + 1)
    ],
    "Route": np.random.choice(routes, num_records),
    "Ticket_Price": np.random.randint(200, 1500, num_records),
    "Status": np.random.choice(
        ["Confirmed", "Cancelled", "Pending"],
        num_records,
        p=[0.75, 0.15, 0.10]
    ),
    "Booking_Date": [
        datetime.now() - timedelta(days=int(x))
        for x in np.random.randint(0, 90, num_records)
    ],
    "Passengers": np.random.randint(1, 5, num_records),
    "Payment_Mode": np.random.choice(
        ["UPI", "Card", "Cash", "Net Banking"],
        num_records
    )
})

# ---------------- SIDEBAR ----------------

st.sidebar.title("🚌 BUS ANALYTICS")
st.sidebar.write("Intelligent Dashboard")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Dashboard",
        "Ticket Analytics",
        "Revenue Analysis",
        "Route Analysis",
        "Passenger Analysis",
        "Data Upload"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Bus Ticket Data Analytics System")


# ---------------- COMMON CALCULATIONS ----------------

confirmed = data[data["Status"] == "Confirmed"]

total_tickets = len(data)
total_revenue = confirmed["Ticket_Price"].sum()
total_passengers = confirmed["Passengers"].sum()
cancelled = len(data[data["Status"] == "Cancelled"])

# ---------------- HOME PAGE ----------------

if page == "Home":

    st.title("🚌 Bus Ticket Data Analytics")
    st.subheader("Intelligent Transportation Management System")

    st.markdown("""
    Welcome to our intelligent bus ticket analytics platform.

    Transform ordinary ticket booking information into meaningful
    insights using data analytics and visualisation.
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 Project Objectives

        - Analyse ticket booking patterns.
        - Monitor revenue.
        - Identify popular bus routes.
        - Understand passenger behaviour.
        - Analyse cancellation trends.
        - Predict future travel demand.
        """)

    with col2:
        st.markdown("""
        ### ⚡ Key Features

        - Interactive analytics dashboard.
        - Revenue monitoring.
        - Route performance analysis.
        - Passenger statistics.
        - Data visualisation.
        - Intelligent insights.
        """)

    st.markdown("---")

    st.success("Explore the dashboard using the navigation menu!")

    st.info(
        "This dashboard currently uses automatically generated "
        "sample data for demonstration."
    )


# ---------------- MAIN DASHBOARD ----------------

elif page == "Dashboard":

    st.title("📊 Analytics Dashboard")
    st.write("Overall bus ticket booking performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""<div class="metric-card">
            <p>🎟️ Total Tickets</p>
            <h2>{total_tickets:,}</h2>
            </div>""",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""<div class="metric-card">
            <p>💰 Total Revenue</p>
            <h2>₹{total_revenue:,}</h2>
            </div>""",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""<div class="metric-card">
            <p>👥 Passengers</p>
            <h2>{total_passengers:,}</h2>
            </div>""",
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""<div class="metric-card">
            <p>❌ Cancelled</p>
            <h2>{cancelled:,}</h2>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        status_counts = data["Status"].value_counts()

        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Ticket Booking Status",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        revenue_route = confirmed.groupby(
            "Route"
        )["Ticket_Price"].sum().reset_index()

        fig = px.bar(
            revenue_route,
            x="Route",
            y="Ticket_Price",
            title="Revenue by Route",
            color="Ticket_Price",
            labels={"Ticket_Price": "Revenue (₹)"}
        )

        st.plotly_chart(fig, use_container_width=True)


# ---------------- TICKET ANALYTICS ----------------

elif page == "Ticket Analytics":

    st.title("🎟️ Ticket Booking Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Bookings", total_tickets)

    with col2:
        st.metric(
            "Cancellation Rate",
            f"{cancelled / total_tickets * 100:.2f}%"
        )

    booking_trend = data.groupby(
        data["Booking_Date"].dt.date
    ).size().reset_index(name="Bookings")

    fig = px.line(
        booking_trend,
        x="Booking_Date",
        y="Bookings",
        title="Daily Ticket Booking Trends",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Booking Records")

    st.dataframe(
        data.sort_values("Booking_Date", ascending=False),
        use_container_width=True
    )


# ---------------- REVENUE ANALYSIS ----------------

elif page == "Revenue Analysis":

    st.title("💰 Revenue Analysis")

    st.metric("Total Revenue", f"₹{total_revenue:,}")

    revenue = confirmed.groupby(
        confirmed["Booking_Date"].dt.date
    )["Ticket_Price"].sum().reset_index()

    fig = px.area(
        revenue,
        x="Booking_Date",
        y="Ticket_Price",
        title="Daily Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    payment = confirmed.groupby(
        "Payment_Mode"
    )["Ticket_Price"].sum().reset_index()

    fig = px.pie(
        payment,
        names="Payment_Mode",
        values="Ticket_Price",
        title="Revenue by Payment Method",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------- ROUTE ANALYSIS ----------------

elif page == "Route Analysis":

    st.title("🚌 Route Performance Analysis")

    route_data = data.groupby("Route").agg(
        Total_Tickets=("Ticket_ID", "count"),
        Revenue=("Ticket_Price", "sum"),
        Passengers=("Passengers", "sum")
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            route_data,
            x="Route",
            y="Total_Tickets",
            title="Tickets by Route",
            color="Total_Tickets"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            route_data,
            x="Route",
            y="Passengers",
            title="Passenger Distribution",
            color="Passengers"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Route Performance Table")

    st.dataframe(route_data, use_container_width=True)

    popular = route_data.loc[
        route_data["Total_Tickets"].idxmax()
    ]

    st.success(
        f"Most booked route: {popular['Route']} "
        f"with {popular['Total_Tickets']} tickets."
    )


# ---------------- PASSENGER ANALYSIS ----------------

elif page == "Passenger Analysis":

    st.title("👥 Passenger Analytics")

    st.metric("Total Confirmed Passengers", total_passengers)

    passenger_distribution = confirmed.groupby(
        "Route"
    )["Passengers"].sum().reset_index()

    fig = px.bar(
        passenger_distribution,
        x="Route",
        y="Passengers",
        title="Passenger Distribution by Route",
        color="Passengers"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        confirmed,
        x="Ticket_Price",
        nbins=20,
        title="Passenger Ticket Price Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------- DATA UPLOAD ----------------

elif page == "Data Upload":

    st.title("📂 Upload Your Bus Ticket Dataset")

    st.write(
        "Upload a CSV file containing your actual bus ticket records."
    )

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        uploaded_data = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        st.subheader("Uploaded Data")

        st.dataframe(
            uploaded_data,
            use_container_width=True
        )

        st.subheader("Dataset Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Records", len(uploaded_data))

        with col2:
            st.metric(
                "Total Columns",
                len(uploaded_data.columns)
            )

        st.subheader("Missing Values")

        st.dataframe(
            uploaded_data.isnull().sum(),
            use_container_width=True
        )

        st.subheader("Numerical Data Summary")

        st.write(uploaded_data.describe())

        numerical_columns = uploaded_data.select_dtypes(
            include=np.number
        ).columns.tolist()

        if numerical_columns:

            selected_column = st.selectbox(
                "Select a numerical column",
                numerical_columns
            )

            fig = px.histogram(
                uploaded_data,
                x=selected_column,
                title=f"Distribution of {selected_column}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    "<center>🚌 Bus Ticket Data Analytics & Intelligent Dashboard"
    "<br>Powered by Python and Streamlit</center>",
    unsafe_allow_html=True
)
