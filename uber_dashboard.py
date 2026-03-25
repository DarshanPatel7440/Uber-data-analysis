import streamlit as st 
import pandas as pd 
from streamlit_option_menu import option_menu
import plotly.express as px 

df = pd.read_csv('D:/Data Science and GEN AI/Streamlit/Uber data set ncr - ncr_ride_bookings.csv')
print(df.columns)

st.set_page_config('Uber Dashboard',layout='wide')

with st.sidebar:
    selected = option_menu(
        'Main Menu',
        ['Dataset','Overview','Ride Analytics','Data Assistance'],
        icons=['table','bar-chart','graph-up','robot'],
        menu_icon=['car-front']
    )

if selected == 'Dataset' :

    st.title("Dataset Explore")
    st.divider()


    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows: ",df.shape[0])
    col2.metric('Total Columns : ',df.shape[1])
    col3.metric("Null Values : ",df.isnull().sum().sum())


    # Column Selection

    st.header('Select Columns')

    selected_cols = st.multiselect(label="Select any columns",options=df.columns,default=df.columns)

    filter_df = df[selected_cols]

    st.dataframe(filter_df)

    st.header('Column Filter')

    col_fil1, col_fil2 = st.columns(2)

    with col_fil1:
        filter_column = st.selectbox('Select Column',filter_df.columns)

    with col_fil2:
        filter_value = st.selectbox('Select Value',filter_df[filter_column].dropna().unique())

    if st.button('Apply Filter'):
        filter_df = filter_df[filter_df[filter_column] == filter_value]

    # Row Disply

    st.subheader('Row Display')

    row = st.slider('Number of rows disply',min_value=10,max_value=len(filter_df),value=20)

    st.divider()

    # Dataset Tables

    st.header('Dataset Table')

    st.dataframe(filter_df.head(row))

    if st.checkbox('Check to see full dataset'):
        st.dataframe(filter_df,use_container_width=True)

if selected == "Overview" :

    st.title('Overview of Uber')
    st.divider()

    total_rides = len(df)

    completed_ride = df[df['Booking Status'] == 'Completed']
    total_revenue = completed_ride['Booking Value'].sum()

    avg_distance = completed_ride['Ride Distance'].mean()

    success_rate = (len(completed_ride) / len(df) ) * 100

    avg_rating = round(completed_ride['Driver Ratings'].mean(),1)

    over1, over2, over3, over4 = st.columns(4)

    over1.metric("Total Rides",total_rides)
    over2.metric("Total Revenue",total_revenue,"$120000")
    over3.metric("Success Rate",success_rate,"30%")
    over4.metric("Ave Rating",avg_rating)

    st.divider()

    st.subheader('Business Unit Performance Metrix')

    bu_metrics = df.groupby('Vehicle Type').agg(
        Total_Bookings = ('Booking ID','count'),
        Revenue_Generated = ('Booking Value','sum'),
        Avg_Distance = ('Ride Distance','mean'),
        Avg_Rating = ('Customer Rating','mean')
    )

    bu_metrics['Revenue share %'] = (bu_metrics['Revenue_Generated'] / total_revenue * 100 if total_revenue > 0 else 0)

    st.dataframe(bu_metrics.style.format({
        "Revenue_Generated" : "$ {:,.2f}",
        "Avg Distance" : "{:,.2f}km",
        "Avg_rating" : "{:,.1f}",
        "Revenue Share %": "{:,.1f}%"
    }))

    st.divider()

    col_eff, col_can = st.columns(2)

    with col_eff :
        st.subheader("Operation Effeciency")
        eff_df = df.groupby('Vehicle Type')[['Avg VTAT','Avg CTAT']].mean()

        st.dataframe(eff_df)

    with col_can :
        st.subheader('Cancellation Audit')
        status_count = df['Booking Status'].value_counts().to_frame(name='Count')

        status_count['Share %'] = (status_count['Count'] / total_rides * 100)
        st.dataframe(status_count, use_container_width=True)

    st.divider()

    st.header('Financial Deep Dive')

    pay_col, reason_col = st.columns([4,6])

    # Payment analysis

    with pay_col :
        st.markdown('Payment Method Preferences')

        pay_summary = (completed_ride['Payment Method'].value_counts(normalize=True)*100)

        st.dataframe(pay_summary)

    with reason_col :
        st.markdown('Primary Cancellation Triggers')
        cust_reason = (df['Reason for cancelling by Customer'].dropna().value_counts().head(3))
        drv_reason = (df['Driver Cancellation Reason'].dropna().value_counts().head(3))
        
        st.dataframe([cust_reason,drv_reason])

if selected == "Ride Analytics" :

    st.title('Advanced Ride intelligence dashboard.')
    st.divider()

    completed = df[df['Booking Status'] == 'Completed']
    # sunbust chart
    st.subheader('Sunburst')
    fig1 = px.sunburst(
        completed,
        path=['Vehicle Type','Payment Method'],
        values='Booking Value',
        color='Booking Value',
        color_continuous_scale='Turbo'
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Tree map
    st.divider()
    st.subheader('Tree map')
    fig2 = px.treemap(
        completed,
        path=['Payment Method','Vehicle Type'],
        values='Booking Value',
        color='Booking Value'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Box plot

    st.divider()
    st.subheader('Box plot')
    fig3 = px.box(
        completed,
        x='Vehicle Type',
        y='Customer Rating',
        color='Vehicle Type'
    )
    
    st.plotly_chart(fig3, use_container_width=True)

if selected == 'Data Assistance' :

    st.header('You can ask anything to this chat bot.')

    user_question = st.text_input('Enter want you want to analyze.')    

    completed = df[df['Booking Status'] == 'Completed']

    if user_question :
        que = user_question.lower()

        if 'ride' in que :
            
            fig = px.bar(
                completed,
                x = 'Vehicle Type',
                y = 'Booking Value',
                labels= 'Booking Value vs Vehicle Type',
                color= 'Vehicle Type'
            )

            st.plotly_chart(fig, use_container_width=True)

        if 'describe' in que :

            st.dataframe(completed.describe())


        if 'statics' in que:
            total_length = len(df)
            total_complete_booking = len(completed)
            incomplete_rides = total_length - total_complete_booking
            vehicle_type = completed['Vehicle Type'].unique()
            total_revenue = completed['Booking Value'].sum()
            avg_distance = round(completed['Ride Distance'].mean(),2)
            customer_rating = round( completed['Customer Rating'].mean(), 2)
            payment_method = completed['Payment Method'].value_counts()

            col1, col2 = st.columns(2)

            with col1:
                st.write("Total Customers",total_length)
                st.write("Completed Rides",total_complete_booking)
                st.write("Incompleted Rides",incomplete_rides)
                st.write('Avg Distance',avg_distance)
                st.write('Customer Avg Rating',customer_rating)

            with col2 :
                st.write("vehicel Type",vehicle_type)
                st.write('Most used payment method',payment_method)


        else :
            st.warning('Plese enter words like ride, describe, statics')