import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(layout="wide",page_title="Startup Analysis")
df=pd.read_csv('startup_cleaned (1).csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')#date->datetime mai convert nhi hua tha
def load_overall_analysis():
    st.title("Overall Analysis")
    #total invested amount---
    total=round(df['amount'].sum())
    st.metric('Total Investement',str(total) +" cr")
    #max amount infused in a startup--
    max_fund=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    st.metric("max" ,str(max_fund)+" cr")
    avg=df.groupby("startup")["amount"].sum().mean()
    st.metric("Average", str(round(avg)) + " cr")
    # total startup---
    num_startup=df['startup'].nunique()
    st.metric("Funded Startup",  num_startup)

    #-------------------------------------------------------- df['year'] = df['date'].dt.year  # year ko extract kiya...
    df["month"] = df["date"].dt.month
    df['year'] = df['date'].dt.year  # year ko extract kiya...

    col1,col2=st.columns(2)
    with col1:
        st.header("MOM Graph")
        select_option=st.selectbox('Select Type',['Total','Count'])
        if select_option=='Total':
            temp_df = df.groupby(["year", "month"])['amount'].sum().reset_index()
            temp_df["x_axis"] = temp_df["month"].astype(str) + '-' + temp_df["year"].astype(str)

            fig3, ax3 = plt.subplots()
            ax3.plot(temp_df["x_axis"], temp_df["amount"], color='#5CB6C1')
            ax3.set_xlabel("month/year")
            ax3.set_ylabel("Total Funding")
            st.pyplot(fig3)
        else:
            temp_df = df.groupby(["year", "month"])['amount'].count().reset_index()

            temp_df["x_axis"] = temp_df["month"].astype(str) + '-' + temp_df["year"].astype(str)

            fig3, ax3 = plt.subplots()
            ax3.plot(temp_df["x_axis"],temp_df["amount"] ,color='#5CB6C1')
            ax3.set_xlabel("month/year")
            ax3.set_ylabel("NO_of Funding")
            st.pyplot(fig3)





def load_investor_details(investors):
    st.title(investors)

    # load the recent 5 investment of investor---
    last5_df=df[df['investor'].str.contains(investors, case=False, na=False)].head()[
        ['date', 'startup', 'verticle','city','round','amount']]
    #st.subheader('Most Recent Investments')
    #st.markdown("### :blue[Most Recent Investments]")
    st.markdown(
        "<h3 style='font-family: \"Segoe UI\", Tahoma, Geneva, sans-serif; color: #800080; font-weight: 600;'>"
        "Most Recent Investment"
        "</h3>",
        unsafe_allow_html=True
    )
    st.dataframe(last5_df)

    # biggest investement---(plot graph)
    col1,col2=st.columns(2,gap="large")
    with col1:
        big_series=df[df['investor'].str.contains(investors, case=False, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        #st.subheader('Biggest Investements')
        #st.markdown("### :blue[Biggest investment]")
        st.markdown("<h3 style='color: #800080;'>Biggest investment</h3>", unsafe_allow_html=True)
        #st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values,color='#5CB6C1')
        ax.set_xlabel("starup")
        ax.set_ylabel("inr_amount")
        st.pyplot(fig)
    with col2:

        #----------********sector wise investment******************------
        #jin investor ne koi invest nhi kiya hai yani amount 0 uske liye
        # niche hamne condition likha hai---
        # 1. Selected investor ka total amount calculate karein
        select_investor=investors
        investor_df=df[df['investor'].str.contains(select_investor,case=False,na=False)]
        st.subheader(f"Investment Breakdown for {selected_investor}")
        total_amount = investor_df['amount'].sum()

        # 2. Check karein ki total amount > 0 hai ya nahi
        if total_amount > 0: #agar sabhi amount ka sum milakr bhi 0 rha to direct else chalega
            # Graph data prepare karein
            data = investor_df.groupby('verticle')['amount'].sum().reset_index()
            #data mai hr vector or us sector me udaya gya total amount rahega

            #verticl ka group karne pr total amount agr 0 rahi to use hta dena
            data = data[data['amount'] > 0] #masking

            #Pie Chart
            fig = px.pie(data, values='amount', names='verticle', title='Sector-wise Investment')
            st.plotly_chart(fig, use_container_width=True)

        else:
            # Agar amount 0 ya missing hai toh Graph ki jagah HTML/CSS styled card show karein
            st.write("⚠️ Investment Amount Data Not Found (Undisclosed by Investor)")


    #st.divider()


    # Custom Divider Code
    st.markdown(
        """
        <hr style="border:none; height:3px; background-color: #ff4b4b; border-radius: 5px; margin: 30px 0;">
        """,
        unsafe_allow_html=True
    )
    # city wise investiment----

    select_investor1 = investors  # ya st.selectbox se aaya hua investor
    investor_df1 = df[df['investor'].str.contains(select_investor1, case=False, na=False)]

    total_amount1 = investor_df1['amount'].sum()

    st.subheader("***Investment In City****")

    # 2. Check karein ki total amount > 0 hai ya nahi
    if total_amount1 > 0:
        # Graph data prepare karein
        data1 = investor_df1.groupby('city')['amount'].sum().reset_index()

        # Amount 0 wali verticals ko remove karein taaki chart clean bane
        data1 = data1[data1['amount'] > 0]

        # Pie Chart / Bar Chart
        fig2 = px.pie(data1, values='amount', names='city')
        st.plotly_chart(fig2, use_container_width=True)

    else:
        # Agar amount 0 ya missing hai toh Graph ki jagah HTML/CSS styled card show karein
        st.write("⚠️ Investment Amount Data Not Found (Undisclosed by Investor)")

    #-------------------------------

    #year by year investiment---
    df['year'] = df['date'].dt.year #year ko extract kiya...
    data = df[df['investor'].str.contains(investors)].groupby('year')['amount'].sum().reset_index()
    st.markdown("<h3 style='color: #800080;'>YOY investiment</h3>", unsafe_allow_html=True)
    fig3 = px.line(
        data,
        x='year',
        y='amount',
        title='Year-wise Total Funding Amount',
        labels={'year': 'Year', 'amount': 'Total Amount (in Cr)'},
        markers=True,
        # text=data['amount'].round(4) # Line ke upar exact values dikhane ke liye

    )
    fig3.update_layout(
        template='plotly_white',  # Clean white background
        title_font_size=18,
        xaxis=dict(dtick=1, showgrid=True),  # Clean year ticks
        yaxis=dict(showgrid=True, gridcolor='LightGray'),
        hovermode='x unified'  # Interactive crosshair hover effect
    )
    st.plotly_chart(fig3)

    #-------------------round-------------

    st.markdown("<h3 style='color: #800080;'>Stage-wise Funding Portfolio</h3>", unsafe_allow_html=True)
    round_data= df[df['investor'].str.contains(investors, case=False, na=False)].groupby('round')['amount'].sum().reset_index()
    fig4=px.pie(round_data,values='amount',names='round',hole=0.4,
            color_discrete_sequence=['#1E3A8A', '#800080', '#008080', '#D97706', '#E53E3E'])
    st.plotly_chart(fig4)

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    #st.title('Overall Analysis')
    #st.markdown("<h1 style='color: #B35E4D;'>Overall Analysis</h1>", unsafe_allow_html=True)
    load_overall_analysis()# call kiya

elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    #st.title('Startup Analysis')
    st.markdown("<h1 style='color: #36E7DE;'>Startup Analysis</h1>", unsafe_allow_html=True)
    st.image("starup.jpg",width=200)
    # if btn1:




else :
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investor'].str.split(',').sum())))
    btn2= st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
    #st.title('Investor Analysis')


