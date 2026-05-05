import streamlit as st
import pandas as pd
import joblib

# Must be the first Streamlit command
st.set_page_config(
    page_title="Music Mood Predictor",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    
    /* Title and text styling */
    h1, h2, h3, p, label {
        color: #f1f2f6 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .title-container {
        text-align: center;
        padding: 2rem 0;
        animation: fadeInDown 1s ease-out;
    }
    
    h1.main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #1db954, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #a4b0be !important;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Card/Container styling */
    .stForm {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        animation: fadeIn 1.5s ease-out;
    }
    
    /* Sliders styling */
    .stSlider > div > div > div {
        background-color: #1db954 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #1db954 0%, #1ed760 100%);
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.6);
        background: linear-gradient(90deg, #1ed760 0%, #1db954 100%);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 10px;
    }

    /* Result Box */
    .result-box {
        background: rgba(29, 185, 84, 0.15);
        border: 2px solid #1db954;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
        animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .mood-text {
        font-size: 3rem;
        font-weight: 900;
        color: #1db954;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        return joblib.load('best_model_logistic_regression.pkl')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Header Section
st.markdown("""
<div class="title-container">
    <h1 class="main-title">AI Music Mood Predictor</h1>
    <p class="subtitle">Discover the emotional vibe of any track using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

if model:
    # App Main Form
    with st.form("prediction_form"):
        st.markdown("### 🎹 Track Profile")
        
        # Genre Input
        text_feature = st.text_input("Enter Music Genre(s) (e.g., pop, rock, electronic, jazz chill)", value="pop dance")
        
        st.markdown("### 🎛️ Audio Features")
        
        # Audio feature sliders (split into 3 columns for better UI)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            danceability = st.slider("Danceability", 0.0, 1.0, 0.7, help="How suitable a track is for dancing.")
            energy = st.slider("Energy", 0.0, 1.0, 0.8, help="Intensity and activity measure.")
            valence = st.slider("Valence", 0.0, 1.0, 0.6, help="Musical positiveness (happy/sad).")
            
        with col2:
            loudness = st.slider("Loudness (dB)", -60.0, 0.0, -5.0, help="Overall loudness of a track in decibels.")
            speechiness = st.slider("Speechiness", 0.0, 1.0, 0.05, help="Presence of spoken words.")
            tempo = st.slider("Tempo (BPM)", 0.0, 250.0, 120.0, help="Overall estimated tempo in beats per minute.")
            
        with col3:
            acousticness = st.slider("Acousticness", 0.0, 1.0, 0.1, help="Confidence measure of track being acoustic.")
            instrumentalness = st.slider("Instrumentalness", 0.0, 1.0, 0.0, help="Predicts whether a track contains no vocals.")
            liveness = st.slider("Liveness", 0.0, 1.0, 0.1, help="Presence of an audience in the recording.")

        # Submit button
        submit_button = st.form_submit_button(label="Predict Mood 🚀")

    # Prediction Logic
    if submit_button:
        # Create a DataFrame matching the model's expected input
        input_data = pd.DataFrame({
            'danceability': [danceability],
            'energy': [energy],
            'loudness': [loudness],
            'speechiness': [speechiness],
            'acousticness': [acousticness],
            'instrumentalness': [instrumentalness],
            'liveness': [liveness],
            'valence': [valence],
            'tempo': [tempo],
            'text_feature': [text_feature]
        })

        # Make Prediction
        with st.spinner("Analyzing audio features..."):
            try:
                prediction = model.predict(input_data)[0]
                
                # Choose emoji based on mood
                emoji_map = {
                    'Energetic': '🔥',
                    'Happy': '☀️',
                    'Chill': '🍃',
                    'Sad': '🌧️'
                }
                mood_emoji = emoji_map.get(prediction, '🎵')
                
                # Display Results
                st.markdown(f"""
                <div class="result-box">
                    <h2>The Predicted Mood is:</h2>
                    <div class="mood-text">{prediction} {mood_emoji}</div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Prediction failed: {e}")
else:
    st.warning("⚠️ Could not load the model file 'best_model_logistic_regression.pkl'. Please ensure it exists in the same directory.")
