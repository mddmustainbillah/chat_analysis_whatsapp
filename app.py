import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import seaborn as sns


# st.sidebar.title("WhatsApp chat Analyzer")

st.set_page_config(page_title="Data Analysis", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: WhatsApp chat Analyzer")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df, use_container_width=True)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('ASDS 9thBatch Section B')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis", user_list)


    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    st.title("Top Statistics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Total Messages")
        st.title(num_messages)

    with col2:
        st.header("Total Words")
        st.title(words)

    with col3:
        st.header("Media shared")
        st.title(num_media_messages)

    with col4:
        st.header("Links Shared")
        st.title(num_links)



    # monthly timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    # daily timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    # activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)


    # Finding the busiest users in the group(group lever)
    if selected_user == "Overall":
        st.title('Most Busy Users')
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.dataframe(new_df, use_container_width=True)


    # WordCloud
    st.title("Wordcloud with Stopwords")
    df_wc = helper.create_worldcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    plt.axis("off") 
    plt.tight_layout(pad = 0)
    st.pyplot(fig, use_container_width=True)


    # WordCloud
    st.title("Wordcloud without Stopwords")
    df_wc = helper.create_wordcloud_without_stopwords(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    plt.axis("off") 
    plt.tight_layout(pad = 0)
    st.pyplot(fig, use_container_width=True)








    # most common words
    most_common_df = helper.most_common_words(selected_user,df)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

    st.title('Most commmon words')
    st.pyplot(fig, use_container_width=True)



    # # Emoji analysis
    # emoji_df = emoji_helper(selected_user, df)
    # st.title("Emoji Analysis")

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.dataframe(emoji_df)
    # with col2:
    #     fig, ax = plt.subplots()
    #     ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
    #     st.pyplot(fig)


