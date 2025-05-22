
import argparse
import threading
import sys

from src.repositories.user_repository import UserRepository
from src.repositories.poll_repository import PollRepository
from src.repositories.nft_repository import NFTRepository

from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

from src.controllers.cli_controller import CLIController

import gradio as gr

# Inicialización de conexiones de bases de datos y Firebase
def init_repositories():
    # Paths/configuración
    mongo_uri = "mongodb://localhost:27017"
    firebase_cred_path = "firebase_config.json"
    firebase_db_url = "https://usuarios-y-credenciales.firebaseio.com/"

    # Repositorios
    user_repo = UserRepository(
        mongo_uri=mongo_uri, 
        firebase_root=firebase_cred_path
    )
    
    poll_repo = PollRepository(
        firebase_root=firebase_cred_path,
        firebase_db_url=firebase_db_url
    )
    
    nft_repo = NFTRepository(
        mongo_uri=mongo_uri,
        firebase_root=firebase_cred_path,
        firebase_db_url=firebase_db_url
    )

    return user_repo, poll_repo, nft_repo

def create_services(user_repo, poll_repo, nft_repo):
    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    poll_service = PollService(poll_repo, nft_service)
    chatbot_service = ChatbotService(poll_service)
    return user_service, poll_service, nft_service, chatbot_service


# --- GRADIO UI setup ---
def build_gradio_ui(poll_service, chatbot_service, nft_service, user_service):
    # Funciones para Gradio

    def vote_ui(poll_id, username, option):
        success, msg = poll_service.vote(poll_id, username, option)
        return msg

    def chatbot_ui(username, user_message):
        return chatbot_service.get_response(username, user_message)

    def tokens_ui(username):
        tokens = nft_service.get_tokens_by_owner(username)
        # Convierte tokens a tabla simple para mostrar
        return "\n".join([f"{t.token_id} - {t.option} (Poll {t.poll_id})" for t in tokens])

    # Layout básico
    with gr.Blocks() as demo:
        gr.Markdown("# Streaming Interactive App")
        
        with gr.Tab("Encuestas"):
            poll_id = gr.Textbox(label="ID Encuesta")
            username = gr.Textbox(label="Usuario")
            option = gr.Textbox(label="Opción")
            vote_btn = gr.Button("Votar")
            vote_out = gr.Textbox(label="Resultado")
            vote_btn.click(vote_ui, inputs=[poll_id, username, option], outputs=vote_out)
        
        with gr.Tab("Chatbot"):
            chat_username = gr.Textbox(label="Usuario")
            chat_input = gr.Textbox(label="Mensaje")
            chat_output = gr.Textbox(label="Respuesta")
            chat_btn = gr.Button("Enviar")
            chat_btn.click(chatbot_ui, inputs=[chat_username, chat_input], outputs=chat_output)

        with gr.Tab("Tokens NFT"):
            tokens_username = gr.Textbox(label="Usuario")
            tokens_btn = gr.Button("Mostrar tokens")
            tokens_out = gr.Textbox(label="Tokens")
            tokens_btn.click(tokens_ui, inputs=tokens_username, outputs=tokens_out)

    return demo


def main():
    parser = argparse.ArgumentParser(description="Streaming interactive app")
    parser.add_argument("--ui", action="store_true", help="Lanzar interfaz web Gradio")
    args = parser.parse_args()

    # Inicializar repositorios y servicios
    user_repo, poll_repo, nft_repo = init_repositories()
    user_service, poll_service, nft_service, chatbot_service = create_services(user_repo, poll_repo, nft_repo)
    
    # Crear controlador CLI
    cli_controller = CLIController(user_service, poll_service, nft_service, chatbot_service)

    if args.ui:
        # Ejecutar Gradio UI en hilo aparte
        ui_app = build_gradio_ui(poll_service, chatbot_service, nft_service, user_service)

        def run_ui():
            ui_app.launch(server_name="0.0.0.0", server_port=7860, share=False)

        ui_thread = threading.Thread(target=run_ui)
        ui_thread.start()

        # También lanzar CLI para admin
        try:
            cli_controller.run()
        except KeyboardInterrupt:
            print("Cerrando aplicación...")

    else:
        # Solo CLI
        cli_controller.run()


if __name__ == "__main__":
    main()
