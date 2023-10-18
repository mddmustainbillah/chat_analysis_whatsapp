from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
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




def create_wordcloud_without_stopwords(selected_user,df):

    f = open('stopwords.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[~df['message'].str.contains('mitte')]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):

    f = open('stopwords.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[~df['message'].str.contains('mitte')]
    

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



# def emoji_helper(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []
#     for message in df['message']:
#         for word in message.split():
#             if any(char in emoji.UNICODE_EMOJI for char in word):
#                 emojis.append(word)

#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df



def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()



def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()



def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap