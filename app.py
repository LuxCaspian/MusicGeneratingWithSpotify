import streamlit as st
import pandas as pd

# Must be the first Streamlit command
st.set_page_config(
    page_title="Music Generator UI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@500;700&display=swap');
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
        font-family: 'Dancing Script', cursive !important;
        font-size: 1.8rem;
        color: #a4b0be !important;
        font-weight: 500;
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

    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px;
    }
    
    .result-container {
        margin-top: 2rem;
        animation: fadeIn 1s ease-out;
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
</style>
""", unsafe_allow_html=True)

# Helper function to generate Moods using Audio Features + Text
def assign_accurate_mood(row):
    valence = pd.to_numeric(row.get('valence', 0.5), errors='coerce')
    energy = pd.to_numeric(row.get('energy', 0.5), errors='coerce')
    genre = str(row.get('artist_genres', '')).lower()

    if pd.isna(valence) or pd.isna(energy):
        valence, energy = 0.5, 0.5

    # 1. STRICT Chill Override: Only allow actual chill genres into "Chill"
    # This prevents Pop/Country songs (like Taylor Swift) from accidentally being labeled Chill
    is_chill_genre = any(k in genre for k in ['lo-fi', 'classical', 'jazz', 'ambient', 'acoustic', 'chill', 'r&b', 'rnb', 'blues', 'soul'])
    if is_chill_genre:
        return 'Chill'

    # 2. Strong Genre Overrides for Energetic
    if any(k in genre for k in ['metal', 'punk', 'hardcore', 'dance', 'electronic', 'house']):
        return 'Energetic'
    
    # Hip Hop is rarely "Sad" in the traditional sense; usually anger/aggression.
    if 'hip hop' in genre or 'rap' in genre:
        return 'Energetic'

    # 3. Spotify Audio Features (For all remaining genres like Pop, Indie, Country, etc.)
    if valence <= 0.5 and energy <= 0.65:
        return 'Sad'
    elif valence >= 0.6:
        return 'Happy'
    elif energy > 0.7:
        return 'Energetic'
    else:
        # High valence but moderate/low energy (e.g. acoustic pop) now defaults to Happy instead of Chill
        return 'Happy'

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('merged_spotify_data.csv')
        # Apply the accurate mood logic using axis=1 to pass the entire row
        df['mood'] = df.apply(assign_accurate_mood, axis=1)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Header Section
st.markdown("""
<div class="title-container">
    <h1 class="main-title">🎵 Music Generator UI </h1>
    <p class="subtitle">Select your vibe and let AI curate your playlist</p>
</div>
""", unsafe_allow_html=True)

if not df.empty:
    # Setup options
    common_genres = [
        'Pop', 'Rock', 'Hip Hop', 'R&B', 'Country',
        'Jazz', 'Electronic', 'Classical', 'Blues',
        'Indie', 'Metal', 'Reggae', 'Dance'
    ]
    unique_moods = sorted(df['mood'].unique().tolist())
    
    # UI Form
    with st.form("generator_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_mood = st.selectbox("Mood:", ['Any'] + unique_moods)
        with col2:
            selected_genre = st.selectbox("Genre:", ['Any'] + common_genres)
            
        # Submit button
        submit_button = st.form_submit_button(label="Generate Music 🚀")

    # Generation Logic
    if submit_button:
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        filtered_df = df.copy()

        if selected_genre != 'Any':
            search_term = selected_genre.lower()
            filtered_df = filtered_df[filtered_df['artist_genres'].str.contains(search_term, case=False, na=False)]

        if selected_mood != 'Any':
            filtered_df = filtered_df[filtered_df['mood'] == selected_mood]

        if filtered_df.empty:
            st.error(f"❌ No songs found for Genre: **{selected_genre}** and Mood: **{selected_mood}**. Try another combination!")
        else:
            st.success(f"✅ AI recommends songs for Genre: **'{selected_genre}'** & Mood: **'{selected_mood}'**!")
            
            sample_size = min(3, len(filtered_df))
            recommendations = filtered_df.sample(sample_size)
            
            st.markdown("### Your Curated Tracks:")
            for idx, row in recommendations.iterrows():
                track_id = row['track_id']
                # Embed the Spotify Player
                spotify_player = f"""
                <iframe src="https://open.spotify.com/embed/track/{track_id}"
                        width="100%" height="152" frameborder="0"
                        allowtransparency="true" allow="encrypted-media">
                </iframe>
                <br><br>
                """
                st.components.v1.html(spotify_player, height=160)
                
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ Could not load 'merged_spotify_data.csv'. Please make sure the file exists in the directory.")
