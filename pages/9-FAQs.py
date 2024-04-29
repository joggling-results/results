import streamlit as st

st.set_page_config(page_title='FAQs',
                   page_icon=':🔎:',
                   layout = 'wide',        ## 'centered','wide'
                   initial_sidebar_state = 'expanded'   ## 'auto','collapsed','expanded'
                   )

st.write("#### FAQ")

@st.cache_data
def make_faq_dict() -> dict:
    '''
    Create a dictionary of question:answer, key-values in a standard python dictionary.

    Returns:
        faq_dict: dict
    '''

    faq_dict = {'What is this site?':
                """Welcome to the Joggling Results Archive. Joggling is a sport combing running and juggling. 
                This site aims to present a holistic view of joggling results from it's creation in the 1980's, to the present day""",
                
                'Who are you?':
                """Hello! This site has been built and is maintained by Scott Jenkins and Chris Edwin,
                two jogglers from the UK. We created this archive to document and 
                celebrate the achievements of joggler's from around the world. Starting with endurance joggling results, 
                the scope has expanded to include events of all distances, and offer other insights into the joggling community.""",
                
                "I'm a joggler. How do I appear on this site?":
                """
                We'd love to include you in the archive! You can submit your 
                results here https://jogglingresults.streamlit.app/Results_Submission. Just include your name,
                the event, finish time, and evidence links to results / strava activity etc. and we'll add your results in. 
                """,

                "What evidence is required for my result to appear on this site?":
                """
                Please include links to race results and photos, strava activities, and other media in your result submission.
                But whilst there is an 'evidence' column in the results table, 
                this site is built on the trust of the joggling 
                community - we will accept unevidenced results if necessary.
                """,

                "I've submitted my result, when will it appear in the archive?":
                """
                Thanks for your submission! We aim to update the site with your latest results once a month - check back later.
                """,
    
                "What are the rules of competitive joggling?":
                """
                As first described by Bill Giduz,
                - Balls must be joggled in a regular, recognized pattern during every step of a race. 
                - Balls dropped during a race may be retrieved, but after retrieving the ball the joggler must return to the point of the drop to begin joggling again.  
                - Any racer who interferes with another racer by straying from a lane, or in retrieving a dropped ball, will be disqualified, and officials have the discretion to re-run a race if they feel interference affected the outcome. 
                - Jogglers must cross the finish line in full control of the juggle.
                - The balls must cross the finish line first, followed by the joggler’s torso. Jogglers may be disqualified for improper form or lack of control of the balls in crossing the finish line.
                - In relay races the approaching joggler may stop joggling as soon as he or she enters the handoff zone.  The handoff of one ball to the next joggler must be made inside the exchange zone, and the receiving joggler is allowed two steps before he or she must begin joggling.
                """,

                "Where can I find other jogglers?":
                """
                Whilst primarily an individual sport, you can find various communities of jogglers online. For example:
                - Joggler's United: https://www.facebook.com/groups/372157942956062
                - Joggling UK: https://www.facebook.com/groups/280873742742227
                - Strava Group: https://www.strava.com/clubs/jogglers
                """,

                "Are there any joggling bloggers?":
                """
                Yes! Check out:
                - Tim Butler, UK: https://www.joggling.co.uk/
                - Michal Kapral, CAN: https://thejoggler.blogspot.com/
                - Perry Romanowski, USA: https://justyouraveragejoggler.com/
                """,
    }
    
    return faq_dict


# Create dictionary
faq_dict = make_faq_dict()

# Questions are the keys of the dictionary.
option = st.selectbox(
    'Select FAQ',
    (faq_dict.keys()))

# Then print the corresponding answer based on the dictionary key
st.write(faq_dict[option])


