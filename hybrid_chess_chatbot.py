import streamlit as st
import chess
import chess.svg
import random

import io
board = chess.Board()

# Display SVG directly
svg_board = chess.svg.board(board=board)
st.markdown(f'<div style="text-align:center">{svg_board}</div>', unsafe_allow_html=True)
st.set_page_config(page_title="Hybrid Chess Chatbot", page_icon="♟️", layout="centered")

st.title("♟️ Hybrid Chess Chatbot")
st.markdown("Play chess and chat with an AI assistant that helps you learn!")

# --- Session State ---
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

board = st.session_state.board

# --- Render Board ---
def render_board(board):
    svg_data = chess.svg.board(board=board)
    drawing = svg2rlg(io.StringIO(svg_data))
    png_data = io.BytesIO()
    renderPM.drawToFile(drawing, png_data, fmt="PNG")
    png_data.seek(0)
    st.image(png_data, width=400, caption="Current Board")

# --- Chatbot Logic ---
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # Reset board
    if user_input == "reset":
        st.session_state.board.reset()
        return "Board has been reset!"

    # Legal move check
    try:
        move = chess.Move.from_uci(user_input)
        if move in board.legal_moves:
            board.push(move)
            # Bot move
            if not board.is_game_over():
                bot_move = random.choice(list(board.legal_moves))
                board.push(bot_move)
                return f"I played {bot_move.uci()}. Your turn!"
            else:
                return "Game over!"
        else:
            return "Illegal move! Try again."
    except:
        # Other chat
        if "hello" in user_input:
            return "Hello! Ready to play some chess?"
        elif "help" in user_input:
            return "Type a chess move in UCI format like 'e2e4', or type 'reset' to restart."
        else:
            return "I'm your chess assistant! Make a move like 'e2e4' or type 'help'."

# --- Handle input ---
def handle_input():
    user_msg = st.session_state.user_input
    if user_msg:
        bot_reply = chatbot_response(user_msg)
        st.session_state.chat_history.append(("You", user_msg))
        st.session_state.chat_history.append(("Bot", bot_reply))
        st.session_state.user_input = ""  # clear input

# --- Display ---
render_board(board)

st.text_input(
    "Enter move or chat:",
    key="user_input",
    on_change=handle_input,
    placeholder="Try 'e2e4', 'hello', 'help', or 'reset'"
)

st.subheader("💬 Chat History")
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")

