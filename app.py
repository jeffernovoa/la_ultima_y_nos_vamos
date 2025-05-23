import firebase_admin
from firebase_admin import credentials
import argparse

from src.repositories.user_repository import UserRepository
from src.repositories.poll_repository import PollRepository
from src.repositories.nft_repository import NFTRepository

from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

from src.controllers.cli_controller import CLIController
from src.ui.gradio_ui import WebUI

# --- Inicialización de Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://usuarios-y-credenciales.firebaseio.com/"
    })

# --- Inicialización de repositorios ---
def init_repositories():
    mongo_uri = "mongodb://localhost:27017"

    user_repo = UserRepository(
        mongo_uri=mongo_uri, 
        firebase_root="usuarios"
    )
    
    poll_repo = PollRepository()
    
    nft_repo = NFTRepository(
        mongo_uri=mongo_uri,
        firebase_root="nfts"
    )

    return user_repo, poll_repo, nft_repo

# --- Inicialización de servicios ---
def create_services(user_repo, poll_repo, nft_repo):
    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    poll_service = PollService(poll_repo, nft_service)
    chatbot_service = ChatbotService(poll_service)
    return user_service, poll_service, nft_service, chatbot_service

# --- Gradio UI ---
def build_gradio_ui(poll_service, chatbot_service, nft_service, user_service):
    interfaz_web = WebUI(poll_service, chatbot_service, nft_service, user_service)
    return interfaz_web.interfaz()

# --- Función principal ---
def main():
    parser = argparse.ArgumentParser(description="App de votación interactiva")
    parser.add_argument("--ui", action="store_true", help="Lanzar la interfaz web (Gradio)")
    args = parser.parse_args()

    # Inicializar componentes
    user_repo, poll_repo, nft_repo = init_repositories()
    user_service, poll_service, nft_service, chatbot_service = create_services(user_repo, poll_repo, nft_repo)

    if args.ui:
        # Solo lanzar interfaz web
        ui_app = build_gradio_ui(poll_service, chatbot_service, nft_service, user_service)
        print("⚙️  Lanzando Gradio en http://localhost:7860 ...")
        ui_app.launch(server_name="0.0.0.0", server_port=7860, share=True)
    else:
        # CLI en modo terminal
        cli_controller = CLIController(user_service, poll_service, nft_service, chatbot_service)
        cli_controller.run()

if __name__ == "__main__":
    main()
