from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()


def fetch_stats(selected_user, df):
    # if selected_user == "Overall":
    #     # 1. fetch number of messages
    #     num_messages = df.shape[0]
    #     # 2. number of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
    #     return num_messages, len(words)
    # else:
    #     new_df = df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #     return num_messages, len(words)


    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Fetch the number of messages
    num_messages = df.shape[0]

    # Fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch the number of media messages
    num_media_message = df[df['message'].str.contains('image omitted')].shape[0]

    # Fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_message, len(links)



def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_worldcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        # Filter rows where 'Message' does not contain 'image omitted'
    df = df[~df['message'].str.contains('mitte')]
    
    wc = WordCloud(min_font_size=10)
    df_wc = wc.generate(df['message'].str.cat(sep=' '))

    return df_wc
