import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

df = pd.read_csv('data/uber_data.csv')

st.set_page_config('🚗 Uber Analytics Pro', layout='wide', page_icon='🚗')

# ─── GLOBAL CUSTOM CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root theme ── */
:root {
    --uber-black:   #000000;
    --uber-white:   #FFFFFF;
    --uber-green:   #00C853;
    --uber-teal:    #00BCD4;
    --uber-amber:   #FFB300;
    --uber-red:     #FF3D00;
    --card-bg:      #111111;
    --card-border:  #222222;
    --surface:      #0A0A0A;
    --text-muted:   #888888;
}

/* ── App background ── */
.stApp {
    background: var(--uber-black);
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header {visibility: hidden;}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0D0D0D !important;
    border-right: 1px solid #1F1F1F;
}
[data-testid="stSidebar"] * {
    color: #EEEEEE !important;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    text-align: center;
    padding: 20px 10px 10px;
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #FFFFFF;
}
.sidebar-logo span {
    color: var(--uber-green);
}

/* ── Page headings ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #FFFFFF !important;
    letter-spacing: -0.5px;
}

/* ── Glowing page title bar ── */
.page-title {
    background: linear-gradient(135deg, #111 0%, #1a1a1a 100%);
    border-left: 4px solid var(--uber-green);
    border-radius: 0 12px 12px 0;
    padding: 16px 24px;
    margin-bottom: 24px;
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #FFFFFF;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 20px !important;
    transition: transform 0.2s, border-color 0.2s;
}
[data-testid="stMetric"]:hover {
    border-color: var(--uber-green);
    transform: translateY(-3px);
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: var(--uber-green) !important;
    font-size: 0.8rem !important;
}

/* ── Dataframes / tables ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--card-border) !important;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--uber-green) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 10px 32px !important;
    letter-spacing: 0.3px;
    transition: opacity 0.2s, transform 0.15s;
}
.stButton > button:hover {
    opacity: 0.85;
    transform: translateY(-2px);
}

/* ── Select / multiselect ── */
[data-baseweb="select"] {
    background: #111 !important;
    border-color: #333 !important;
    border-radius: 10px !important;
    color: #eee !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--uber-green) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] > div {
    background: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 50px !important;
}

/* ── Dividers ── */
hr {
    border-color: #1F1F1F !important;
}

/* ── Info / warning boxes ── */
.stWarning {
    background: rgba(255,179,0,0.1) !important;
    border-left: 4px solid var(--uber-amber) !important;
    border-radius: 8px;
    color: var(--uber-amber) !important;
}

/* ── Section card wrapper ── */
.section-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
}

/* ── Stat pill ── */
.stat-pill {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 50px;
    padding: 4px 16px;
    font-size: 0.8rem;
    color: var(--uber-green);
    margin: 4px 4px 4px 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--uber-green); }
</style>
""", unsafe_allow_html=True)


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🚗 UBER<span>IQ</span></div>', unsafe_allow_html=True)
    st.markdown("---")

    selected = option_menu(
        menu_title=None,
        options=['Dataset', 'Overview', 'Ride Analytics', 'Data Assistance'],
        icons=['table', 'bar-chart-line', 'graph-up-arrow', 'robot'],
        menu_icon='car-front',
        default_index=0,
        styles={
            "container": {"padding": "4px", "background-color": "transparent"},
            "icon": {"color": "#00C853", "font-size": "16px"},
            "nav-link": {
                "font-family": "'DM Sans', sans-serif",
                "font-size": "14px",
                "color": "#AAAAAA",
                "border-radius": "10px",
                "margin": "2px 0",
            },
            "nav-link-selected": {
                "background-color": "#1A1A1A",
                "color": "#FFFFFF",
                "font-weight": "600",
                "border": "1px solid #2a2a2a",
            },
        }
    )

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center;color:#555;font-size:0.72rem;padding:8px;">'
        '⚡ Powered by Streamlit<br>📊 Uber Analytics Pro v2.0'
        '</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# 📋  DATASET PAGE
# ══════════════════════════════════════════════════════════════════════════════
if selected == 'Dataset':

    st.markdown('<div class="page-title">📋 Dataset Explorer</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("🗂️ Total Rows", f"{df.shape[0]:,}")
    col2.metric("📐 Total Columns", df.shape[1])
    col3.metric("🚨 Null Values", f"{df.isnull().sum().sum():,}")

    st.divider()

    # ── Column Selection
    st.markdown("### 🎛️ Select Columns")
    selected_cols = st.multiselect(
        label="Choose which columns to display",
        options=df.columns,
        default=df.columns
    )
    filter_df = df[selected_cols]
    st.dataframe(filter_df, use_container_width=True)

    st.divider()

    # ── Column Filter
    st.markdown("### 🔍 Column Filter")
    col_fil1, col_fil2 = st.columns(2)
    with col_fil1:
        filter_column = st.selectbox('📌 Select Column', filter_df.columns)
    with col_fil2:
        filter_value = st.selectbox('🎯 Select Value', filter_df[filter_column].dropna().unique())

    if st.button('✅ Apply Filter'):
        filter_df = filter_df[filter_df[filter_column] == filter_value]
        st.success(f"✅ Filter applied — showing rows where **{filter_column}** = **{filter_value}**")

    st.divider()

    # ── Row Display
    st.markdown("### 🔢 Row Display")
    row = st.slider('📏 Number of rows to display', min_value=10, max_value=len(filter_df), value=20)

    st.divider()
    st.markdown("### 📊 Dataset Table")
    st.dataframe(filter_df.head(row), use_container_width=True)

    if st.checkbox('🔓 Show full dataset'):
        st.dataframe(filter_df, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 📈  OVERVIEW PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == "Overview":

    st.markdown('<div class="page-title">📈 Uber Overview Dashboard</div>', unsafe_allow_html=True)

    completed_ride = df[df['Booking Status'] == 'Completed']
    total_rides      = len(df)
    total_revenue    = completed_ride['Booking Value'].sum()
    avg_distance     = completed_ride['Ride Distance'].mean()
    success_rate     = (len(completed_ride) / len(df)) * 100
    avg_rating       = round(completed_ride['Driver Ratings'].mean(), 1)

    over1, over2, over3, over4 = st.columns(4)
    over1.metric("🚖 Total Rides",    f"{total_rides:,}")
    over2.metric("💰 Total Revenue",  f"${total_revenue:,.0f}", "▲ $120,000")
    over3.metric("✅ Success Rate",   f"{success_rate:.1f}%",   "▲ 30%")
    over4.metric("⭐ Avg Rating",     avg_rating)

    st.divider()

    # ── Business Unit Performance
    st.markdown("### 🏢 Business Unit Performance Metrics")

    bu_metrics = df.groupby('Vehicle Type').agg(
        Total_Bookings    = ('Booking ID',     'count'),
        Revenue_Generated = ('Booking Value',  'sum'),
        Avg_Distance      = ('Ride Distance',  'mean'),
        Avg_Rating        = ('Customer Rating','mean')
    )
    bu_metrics['Revenue_Share_%'] = (
        bu_metrics['Revenue_Generated'] / total_revenue * 100
        if total_revenue > 0 else 0
    )

    st.dataframe(
        bu_metrics.style.format({
            "Revenue_Generated": "$ {:,.2f}",
            "Avg_Distance":      "{:,.2f} km",
            "Avg_Rating":        "{:,.1f} ⭐",
            "Revenue_Share_%":   "{:,.1f}%"
        }).background_gradient(subset=['Revenue_Generated'], cmap='Greens'),
        use_container_width=True
    )

    st.divider()

    col_eff, col_can = st.columns(2)

    with col_eff:
        st.markdown("### ⚙️ Operational Efficiency")
        eff_df = df.groupby('Vehicle Type')[['Avg VTAT', 'Avg CTAT']].mean()
        st.dataframe(
            eff_df.style.format("{:.2f} min").background_gradient(cmap='Blues'),
            use_container_width=True
        )

    with col_can:
        st.markdown("### ❌ Cancellation Audit")
        status_count = df['Booking Status'].value_counts().to_frame(name='Count')
        status_count['Share %'] = (status_count['Count'] / total_rides * 100).round(1)

        emoji_map = {
            'Completed':                 '✅',
            'Cancelled by Customer':     '🙅',
            'Cancelled by Driver':       '🚫',
            'Driver Not Found':          '🔍'
        }
        status_count.index = [
            f"{emoji_map.get(s, '❓')} {s}" for s in status_count.index
        ]
        st.dataframe(status_count, use_container_width=True)

    st.divider()

    st.markdown("### 💳 Financial Deep Dive")
    pay_col, reason_col = st.columns([4, 6])

    with pay_col:
        st.markdown("#### 💵 Payment Method Preferences")
        pay_summary = (
            completed_ride['Payment Method']
            .value_counts(normalize=True) * 100
        ).round(1)
        pay_summary.index = [f"💳 {p}" for p in pay_summary.index]
        st.dataframe(pay_summary.rename("Share %"), use_container_width=True)

    with reason_col:
        st.markdown("#### 🔔 Primary Cancellation Triggers")
        cust_reason = (
            df['Reason for cancelling by Customer']
            .dropna().value_counts().head(3)
        )
        drv_reason = (
            df['Driver Cancellation Reason']
            .dropna().value_counts().head(3)
        )
        combined = pd.concat(
            [cust_reason.rename("🧑 Customer"), drv_reason.rename("🚗 Driver")],
            axis=1
        ).fillna(0).astype(int)
        st.dataframe(combined, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 📊  RIDE ANALYTICS PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == "Ride Analytics":

    st.markdown('<div class="page-title">📊 Advanced Ride Intelligence</div>', unsafe_allow_html=True)

    completed = df[df['Booking Status'] == 'Completed']

    DARK_TEMPLATE = dict(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # ── Sunburst
    st.markdown("### 🌀 Revenue by Vehicle Type & Payment Method")
    fig1 = px.sunburst(
        completed,
        path=['Vehicle Type', 'Payment Method'],
        values='Booking Value',
        color='Booking Value',
        color_continuous_scale='Turbo',
        title='🌀 Revenue Sunburst — Vehicle × Payment'
    )
    fig1.update_layout(**DARK_TEMPLATE, margin=dict(l=0, r=0, t=60, b=0))
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ── Treemap
    st.markdown("### 🗺️ Booking Value Treemap")
    fig2 = px.treemap(
        completed,
        path=['Payment Method', 'Vehicle Type'],
        values='Booking Value',
        color='Booking Value',
        color_continuous_scale='RdYlGn',
        title='🗺️ Treemap — Payment × Vehicle Type'
    )
    fig2.update_layout(**DARK_TEMPLATE, margin=dict(l=0, r=0, t=60, b=0))
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Box plot
    st.markdown("### 📦 Customer Rating Distribution by Vehicle")
    fig3 = px.box(
        completed,
        x='Vehicle Type',
        y='Customer Rating',
        color='Vehicle Type',
        title='📦 Rating Distribution per Vehicle Type',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig3.update_layout(**DARK_TEMPLATE, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ── Bonus: Revenue over ride distance scatter
    st.markdown("### 🔬 Revenue vs Ride Distance")
    fig4 = px.scatter(
        completed.sample(min(1500, len(completed))),
        x='Ride Distance',
        y='Booking Value',
        color='Vehicle Type',
        size='Booking Value',
        opacity=0.7,
        title='🔬 Booking Value vs Ride Distance (sample)',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig4.update_layout(**DARK_TEMPLATE)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 🤖  DATA ASSISTANCE PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == 'Data Assistance':

    st.markdown('<div class="page-title">🤖 AI Data Assistant</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="background:#111;border:1px solid #222;border-radius:16px;'
        'padding:16px 20px;margin-bottom:20px;color:#aaa;font-size:0.9rem;">'
        '💡 <b style="color:#fff;">Try asking:</b> &nbsp;'
        '<span class="stat-pill">ride</span>'
        '<span class="stat-pill">describe</span>'
        '<span class="stat-pill">statics</span>'
        '</div>',
        unsafe_allow_html=True
    )

    completed = df[df['Booking Status'] == 'Completed']

    user_question = st.chat_input('💬 Ask anything about the Uber data…')

    DARK_TEMPLATE = dict(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    if user_question:
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_question)

        with st.chat_message("assistant", avatar="🤖"):
            que = user_question.lower()
            answered = False

            if 'ride' in que:
                answered = True
                st.markdown("📊 Here's the **Booking Value by Vehicle Type**:")
                fig = px.bar(
                    completed,
                    x='Vehicle Type',
                    y='Booking Value',
                    color='Vehicle Type',
                    title='🚗 Booking Value by Vehicle Type',
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
                fig.update_layout(**DARK_TEMPLATE, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            if 'describe' in que:
                answered = True
                st.markdown("📋 Here's a **statistical summary** of completed rides:")
                st.dataframe(
                    completed.describe().style.format("{:.2f}").background_gradient(cmap='Greens'),
                    use_container_width=True
                )

            if 'statics' in que or 'statistics' in que:
                answered = True
                total_length            = len(df)
                total_complete_booking  = len(completed)
                incomplete_rides        = total_length - total_complete_booking
                vehicle_type            = completed['Vehicle Type'].unique()
                total_revenue           = completed['Booking Value'].sum()
                avg_distance            = round(completed['Ride Distance'].mean(), 2)
                customer_rating         = round(completed['Customer Rating'].mean(), 2)
                payment_method          = completed['Payment Method'].value_counts()

                st.markdown("📊 **Key Statistics at a Glance**")

                s1, s2, s3 = st.columns(3)
                s1.metric("🧍 Total Customers",   f"{total_length:,}")
                s2.metric("✅ Completed Rides",   f"{total_complete_booking:,}")
                s3.metric("❌ Incomplete Rides",  f"{incomplete_rides:,}")

                s4, s5 = st.columns(2)
                s4.metric("📏 Avg Distance",      f"{avg_distance} km")
                s5.metric("⭐ Avg Customer Rating", customer_rating)

                st.markdown(f"**🚗 Vehicle Types:** {', '.join(vehicle_type)}")
                st.markdown("**💳 Payment Methods:**")
                pm_df = payment_method.rename("Bookings").to_frame()
                pm_df.index = [f"💳 {p}" for p in pm_df.index]
                st.dataframe(pm_df, use_container_width=True)

            if not answered:
                st.warning(
                    "🤔 I didn't catch that. Try keywords like "
                    "**ride**, **describe**, or **statics**."
                )
