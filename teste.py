import streamlit as st

# Função para tocar o som automaticamente com autoplay e oculto
def audio_player():
    st.components.v1.html(
        """
        <audio id="audio-player" src="som/som.mp3" style="display: none;" autoplay></audio>
        <script>
            const audio = document.getElementById("audio-player");
            audio.currentTime = 0; // Reinicia o áudio
            audio.play(); // Toca o áudio automaticamente
        </script>
        """,
        height=0,
    )

# Interface do Streamlit
st.title("Pomodoro Timer com Som 🎵")

st.write("Clique no botão abaixo para iniciar o som automaticamente.")
play_button = st.button("Tocar som")

# Chama a função `audio_player` quando o botão é clicado
if play_button:
    audio_player()