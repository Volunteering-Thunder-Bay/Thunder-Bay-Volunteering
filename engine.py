
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd

#indices = pickle.load(open('indices', 'rb'))
#sim_matrix = pickle.load(open('sim_matrix', 'rb'))
from PIL import Image
#design
img= Image.open('logo.png')
st.set_page_config(page_title='Thunder Bay Volunteering Event Recommendation', page_icon=img)

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image(img, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

with col3:
    st.write(' ')


selected3 = option_menu(None, ["Home", "Recommend"], 
    icons=['house', 'book', "envelope"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#purple"},
        "icon": {"color": "purple", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "grey"},
    }
)
hide_menu_style = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

df = pd.read_csv("Volunteering - Sheet1.csv")
df.head()


indices = pd.Series(df.index, index=df['Event']).drop_duplicates()
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vector = TfidfVectorizer(stop_words='english')
df['Information'] = df['Information'].fillna('')
tfidf_matrix = tfidf_vector.fit_transform(df['Information'])
from sklearn.metrics.pairwise import linear_kernel
sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)


#Functions
def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)
    


df['link'] = df.apply(lambda x: make_clickable(x['Url'], x['Event']), axis=1)



def content_based_recommender(Event, sim_scores=sim_matrix):
    indices.to_frame()
    idx = indices[Event]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    event_indices = [i[0] for i in sim_scores]
    result = df['Event'].iloc[event_indices]
    rec_df = pd.DataFrame(result)
    rec_df['Url'] = df.apply(lambda x: make_clickable(x['Url'], x['Event']), axis=1).iloc[event_indices] 
    return rec_df

def find_url(Event, sim_scores=sim_matrix):
    indices.to_frame()
    idx = indices[Event]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:1]
    event_indices = [i[0] for i in sim_scores]
    result = df['Event'].iloc[event_indices]
    rec_df = pd.DataFrame(result)
    rec_df['Url'] = df.apply(lambda x: make_clickable(x['Url'], x['Event']), axis=1).iloc[event_indices] 
    return rec_df

st.markdown("<h1 style='text-align: center; color: purple;'>Thunder Bay Volunteering System</h1>", unsafe_allow_html=True)


contact_form = """
<form action="https://formsubmit.co/joshuaphilip2140@gmail.com" method="POST">
    <input type="text" name="name" placeholder="Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <textarea name="message" placeholder="Send us an Event"></textarea>
    <input type="hidden" name="_captcha" value="false">
    <button type="submit">Send</button>
</form>
"""


#design


selected_volunteer_event = st.selectbox("Volunteering Events:", df['Event'].values)
if selected3=='Home':
    if st.button('Find'):
        search_url = find_url(selected_volunteer_event)
        st.write(search_url)


#Use a local css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



if selected3=='Recommend':
    if st.button('Recommend'):
        recommendations = content_based_recommender(selected_volunteer_event)
        st.write(recommendations)


if selected3=='Contact Us':
    st.header(":mailbox: Send us an Event")
    st.markdown(contact_form, unsafe_allow_html=True)
    local_css("styles.css")   

