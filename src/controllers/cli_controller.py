class CLIController:
    def __init__(self, poll_service, user_service, nft_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.usuario_actual = None

    def run(self):
        print("CLI Activa. Usa 'ayuda' para comandos.")
        while True:
            entrada = input(">> ").strip()
            if not entrada:
                continue

            partes = entrada.split()
            comando = partes[0]
            args = partes[1:]

            try:
                if comando == "salir":
                    break
                elif comando == "ayuda":
                    self.mostrar_ayuda()
                elif comando == "login":
                    self.login()
                elif comando == "registrar":
                    self.registrar()
                elif comando == "crear_encuesta":
                    self.crear_encuesta()
                elif comando == "listar":
                    self.listar_encuestas()
                elif comando == "cerrar_encuesta":
                    self.cerrar_encuesta(args)
                elif comando == "votar":
                    self.votar(args)
                elif comando == "ver_resultados":
                    self.ver_resultados(args)
                elif comando == "mis_tokens":
                    self.mostrar_tokens()
                elif comando == "transferir_token":
                    self.transferir_token(args)
                else:
                    print("Comando desconocido")
            except Exception as e:
                print("Error:", e)

    def mostrar_ayuda(self):
        print("""
Comandos disponibles:
  registrar                          → Crear usuario
  login                              → Iniciar sesión
  crear_encuesta                     → Crear una nueva encuesta
  listar                             → Listar encuestas activas
  cerrar_encuesta <id>              → Cerrar encuesta manualmente
  votar <id> <opcion>               → Votar en encuesta
  ver_resultados <id>               → Ver resultados finales
  mis_tokens                        → Ver mis NFTs
  transferir_token <id> <usuario>   → Transferir NFT
  salir                              → Terminar sesión
""")

    def login(self):
        username = input("Usuario: ")
        password = input("Contraseña: ")
        if self.user_service.login(username, password):
            self.usuario_actual = username
            print("Sesión iniciada.")
        else:
            print("Credenciales incorrectas.")

    def registrar(self):
        username = input("Nuevo usuario: ")
        password = input("Contraseña: ")
        self.user_service.register(username, password)
        print("Usuario registrado correctamente.")

    def crear_encuesta(self):
        pregunta = input("Pregunta: ")
        opciones = input("Opciones (coma separadas): ").split(",")
        duracion = int(input("Duración (segundos): "))
        poll_id = self.poll_service.create_poll(pregunta, opciones, duracion)
        print(f"Encuesta creada con ID: {poll_id}")

    def listar_encuestas(self):
        encuestas = self.poll_service.repo.listar_encuestas_activas()
        for e in encuestas:
            print(f"{e.id}: {e.pregunta} - Opciones: {list(e.opciones.keys())}")

    def cerrar_encuesta(self, args):
        if not args or len(args) < 1:
            print("Debe indicar ID de encuesta")
            return
        self.poll_service.close_poll(args[0])
        print("Encuesta cerrada.")

    def votar(self, args):
        if not args or len(args) < 2:
            print("Debe indicar ID de encuesta y opción")
            return
        poll_id, opcion = args[0], args[1]
        self.poll_service.vote(poll_id, self.usuario_actual, opcion)
        print("Voto registrado.")
        self.nft_service.mint_token(self.usuario_actual, poll_id, opcion)

    def ver_resultados(self, args):
        if not args or len(args) < 1:
            print("Debe indicar ID de encuesta")
            return
        res = self.poll_service.get_final_results(args[0])
        print("Resultados:", res)

    def mostrar_tokens(self):
        tokens = self.nft_service.get_tokens_by_user(self.usuario_actual)
        for t in tokens:
            print(t)

    def transferir_token(self, args):
        if not args or len(args) < 2:
            print("Debe indicar ID de token y usuario destino")
            return
        token_id, nuevo_usuario = args
        self.nft_service.transfer_token(token_id, self.usuario_actual, nuevo_usuario)
        print("Transferencia completada.")
