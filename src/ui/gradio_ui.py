import gradio as gr

class WebUI:
    def __init__(self, poll_service, chatbot_service, nft_service, user_service):
        self.poll_service = poll_service
        self.chatbot_service = chatbot_service
        self.nft_service = nft_service
        self.user_service = user_service
        self.usuario_actual = None

    def login_ui(self, username, password):
        success = self.user_service.login(username, password)
        if success:
            self.usuario_actual = username
            return f"Sesión iniciada como {username}"
        else:
            return "Error en las credenciales."

    def votar_ui(self, poll_id, opcion):
        try:
            self.poll_service.vote(poll_id, self.usuario_actual, opcion)
            self.nft_service.mint_token(self.usuario_actual, poll_id, opcion)
            return "¡Voto y NFT registrados!"
        except Exception as e:
            return str(e)

    def chatbot_ui(self, mensaje):
        return self.chatbot_service.responder(self.usuario_actual, mensaje)

    def mostrar_tokens_ui(self):
        tokens = self.nft_service.get_tokens_by_user(self.usuario_actual)
        return [f"Token: {t['id']}, Encuesta: {t['poll_id']}, Opción: {t['option']}" for t in tokens]

    def interfaz(self):
        with gr.Blocks() as demo:
            gr.Markdown("# Panel de Votación Interactivo")

            with gr.Tab("Login"):
                user = gr.Textbox(label="Usuario")
                pw = gr.Textbox(label="Contraseña", type="password")
                login_btn = gr.Button("Iniciar sesión")
                login_output = gr.Textbox()
                login_btn.click(fn=self.login_ui, inputs=[user, pw], outputs=login_output)

            with gr.Tab("Votar"):
                poll_id = gr.Textbox(label="ID de encuesta")
                opcion = gr.Textbox(label="Opción")
                voto_btn = gr.Button("Votar")
                voto_output = gr.Textbox()
                voto_btn.click(self.votar_ui, inputs=[poll_id, opcion], outputs=voto_output)

            with gr.Tab("Chatbot"):
                chat_input = gr.Textbox(label="Tu pregunta")
                chat_btn = gr.Button("Enviar")
                chat_output = gr.Textbox()
                chat_btn.click(self.chatbot_ui, inputs=[chat_input], outputs=chat_output)

            with gr.Tab("Mis Tokens"):
                tokens_btn = gr.Button("Mostrar NFTs")
                tokens_output = gr.Textbox(lines=10)
                tokens_btn.click(fn=self.mostrar_tokens_ui, outputs=tokens_output)

        return demo
