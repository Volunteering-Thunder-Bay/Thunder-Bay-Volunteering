import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
indices = pickle.load(open('indices', 'rb'))
sim_matrix = pickle.load(open('sim_matrix', 'rb'))
from PIL import Image

#design
img= Image.open('logo.png')
st.set_page_config(page_title='Thunder Bay Volunteering Event Recommendation', page_icon=img,)

# get colors from theme config file, or set the colours to altair standards



col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image(img, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

with col3:
    st.write(' ')


selected3 = option_menu(None, ["Home", "Recommend", "Contact Us"], 
    icons=['house', 'book', "envelope"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#purple"},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "purple"},
    }
)




#hide_menu_style = """
        #<style>
        #MainMenu {visibility:hidden;}
        #footer {visibility: hidden;}
        #</style>
        #"""
#st.markdown(hide_menu_style, unsafe_allow_html=True)


volunteering_dict = pickle.load(open('v.pkl','rb'))
df = pd.DataFrame(volunteering_dict)


#Functions
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{text}</a>'

# TRAILER is the column with hyperlinks
df['Url'] = df['Url'].apply(make_clickable)



def content_based_recommender(Event, sim_scores=sim_matrix):
    indices.to_frame()
    idx = indices[Event]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    event_indices = [i[0] for i in sim_scores]
    df.style.format({'Url': make_clickable})
    result = df['Event'].iloc[event_indices]
    rec_df = pd.DataFrame(result)
    rec_df['Url'] = df['Url'].iloc[event_indices]
    rec_df['Url'] = st.write(rec_df.to_html(escape=False, index=False), unsafe_allow_html=True)

def find_url(Event, sim_scores=sim_matrix):
    indices.to_frame()
    idx = indices[Event]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:1]
    event_indices = [i[0] for i in sim_scores]
    result = df['Event'].iloc[event_indices]
    rec_df = pd.DataFrame(result)
    rec_df['Url'] = df['Url'].iloc[event_indices]
    rec_df['Url'] = st.write(rec_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    #return rec_df
    
    
    #url = 
    #rec_df['Url'] = st.write("[Url](%s)" % url)
   



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



if selected3=='Home':
    st.markdown("<h1 style='text-align: center; color: purple;'>Thunder Bay Volunteering System</h1>", unsafe_allow_html=True)
    selected_volunteer_event = st.selectbox("Volunteering Events:", df['Event'].values)
    if st.button('Find'):
        search_url = find_url(selected_volunteer_event)
        st.write(search_url)

#Use a local css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



if selected3=='Recommend':
    st.markdown("<h1 style='text-align: center; color: purple;'>Thunder Bay Volunteering System</h1>", unsafe_allow_html=True)
    selected_volunteer_event = st.selectbox("Volunteering Events:", df['Event'].values)
    if st.button('Recommend'):
        recommendations = content_based_recommender(selected_volunteer_event)
        st.write(recommendations)

if selected3=='Contact Us':
    st.header(":mailbox: Send us an Event")
    st.markdown(contact_form, unsafe_allow_html=True)
    local_css("styles.css")
