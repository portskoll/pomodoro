import time
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Pomodoro Timer - v1.1", page_icon="🍅")

# Função para o cronômetro
def countdown_timer(total_seconds, placeholder):
    while total_seconds >= 0:  # Inclui o 0 no final
        if st.session_state["paused"]:
            time.sleep(0.1)  # Aguarda enquanto está pausado
            continue
        mins, secs = divmod(total_seconds, 60)
        timer = f"{mins:02}:{secs:02}"
        placeholder.markdown(f"## ⏳ {timer}")
        time.sleep(1)
        total_seconds -= 1
        st.session_state["current_timer"] = total_seconds

# Função para exibir notificações no navegador
def show_browser_notification(title, message):
    st.components.v1.html(
        f"""
        <script>
        if (Notification.permission === "granted") {{
            new Notification("{title}", {{
                body: "{message}",
                icon: "https://cdn-icons-png.flaticon.com/512/2907/2907254.png"
            }});
        }} else if (Notification.permission !== "denied") {{
            Notification.requestPermission().then(permission => {{
                if (permission === "granted") {{
                    new Notification("{title}", {{
                        body: "{message}",
                        icon: "https://cdn-icons-png.flaticon.com/512/2907/2907254.png"
                    }});
                }}
            }});
        }}
        </script>
        """,
        height=0,
    )

# Inicializa os estados da sessão
if "current_timer" not in st.session_state:
    st.session_state["current_timer"] = 0
if "paused" not in st.session_state:
    st.session_state["paused"] = False
if "running" not in st.session_state:
    st.session_state["running"] = False
if "cycle_count" not in st.session_state:
    st.session_state["cycle_count"] = 0
if "interval_active" not in st.session_state:
    st.session_state["interval_active"] = False  # Controle do estado de intervalo

# Sidebar com barras deslizantes
st.sidebar.title("Configurações do Pomodoro")
pomodoro_time = st.sidebar.slider("Tempo Total do Pomodoro (min)", 0, 60, 25)
interval_time = st.sidebar.slider("Intervalo entre Atividades (min)", 0, 10, 5)
long_break_time = st.sidebar.slider("Intervalo após 3 Atividades (min)", 0, 40, 15)

# Campo de texto e botões
st.title("Pomodoro Timer 🍅")
#para ouvir musicas externas ff
st.markdown('[🎵 Curtir um som para animar o trabalho?](https://radioplayer.mundotela.com.br/)', unsafe_allow_html=True)
name = st.text_input("Digite seu nome")
placeholder = st.empty()

# Checkbox para ciclo automático
auto_cycle = st.checkbox("Alternar ciclos automaticamente", value=False)

start_button = st.button("Start")
pause_continue_button = st.button("Pause" if not st.session_state["paused"] else "Continuar")
reset_button = st.button("Reiniciar")

# Funções dos botões
if start_button:
    if not st.session_state["running"]:
        st.session_state["current_timer"] = pomodoro_time * 60
        st.session_state["running"] = True
        st.session_state["paused"] = False
        st.session_state["cycle_count"] = 0
        st.session_state["interval_active"] = False

if pause_continue_button:
    st.session_state["paused"] = not st.session_state["paused"]

if reset_button:
    st.session_state["current_timer"] = pomodoro_time * 60
    st.session_state["running"] = False
    st.session_state["paused"] = False
    st.session_state["cycle_count"] = 0
    st.session_state["interval_active"] = False
    placeholder.markdown("## ⏳ 00:00")

# Função principal
if st.session_state["running"]:
    while st.session_state["running"]:
        if not st.session_state["interval_active"]:
            # Pomodoro (atividade)
            activity_message = f"Ciclo {st.session_state['cycle_count'] + 1} - Atividade de {pomodoro_time} minutos."
            st.write(activity_message)
            show_browser_notification("Pomodoro Timer", activity_message)  # Notificação no navegador
            countdown_timer(st.session_state["current_timer"], placeholder)

            # Após o Pomodoro, configura o próximo intervalo
            st.session_state["interval_active"] = True
            if (st.session_state["cycle_count"] + 1) % 3 == 0:  # Pausa longa após 3 ciclos
                st.session_state["current_timer"] = long_break_time * 60
                break_message = f"Pausa longa de {long_break_time} minutos! 🌴"
            else:
                st.session_state["current_timer"] = interval_time * 60
                break_message = f"Intervalo curto de {interval_time} minutos! 🛋️"
            st.write(break_message)
            show_browser_notification("Pomodoro Timer", break_message)  # Notificação no navegador
        else:
            # Intervalo
            countdown_timer(st.session_state["current_timer"], placeholder)

            # Após o intervalo, prepara para o próximo Pomodoro
            st.session_state["cycle_count"] += 1
            st.session_state["current_timer"] = pomodoro_time * 60
            st.session_state["interval_active"] = False

            # Verifica se deve alternar automaticamente
            if not auto_cycle:
                break

