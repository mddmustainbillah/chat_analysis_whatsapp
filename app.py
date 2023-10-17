import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

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
    df_wc = helper.create_worldcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    plt.axis("off") 
    plt.tight_layout(pad = 0)
    st.pyplot(fig, use_container_width=True)


