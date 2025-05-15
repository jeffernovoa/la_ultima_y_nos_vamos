class CLIController:
    def __init__(self, poll_service, user_service, nft_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.usuario_actual = None

    def loop(self):
        while True:
            cmd = input("$ ").strip().split()
            if not cmd: continue
            if cmd[0] == "registrar":
                self.user_service.register(cmd[1], cmd[2])
                print("Registrado.")
            elif cmd[0] == "login":
                token = self.user_service.login(cmd[1], cmd[2])
                self.usuario_actual = cmd[1]
                print(f"Login exitoso. Sesión: {token}")
            elif cmd[0] == "crear_encuesta":
                pregunta = input("Pregunta: ")
                opciones = input("Opciones separadas por coma: ").split(',')
                duracion = int(input("Duración en segundos: "))
                poll_id = self.poll_service.crear_encuesta(pregunta, opciones, duracion)
                print(f"Encuesta creada con ID: {poll_id}")
            elif cmd[0] == "votar":
                if not self.usuario_actual:
                    print("Inicia sesión primero")
                    continue
                self.poll_service.votar(cmd[1], self.usuario_actual, cmd[2])
                self.nft_service.mint_token(self.usuario_actual, cmd[1], cmd[2])
                print("Voto registrado y NFT generado.")
            elif cmd[0] == "mis_tokens":
                tokens = self.nft_service.get_tokens(self.usuario_actual)
                for t in tokens:
                    print(vars(t))
            elif cmd[0] == "transferir_token":
                self.nft_service.transfer_token(cmd[1], self.usuario_actual, cmd[2])
                print("Transferencia exitosa.")
            elif cmd[0] == "salir":
                break
            else:
                print("Comando no reconocido")