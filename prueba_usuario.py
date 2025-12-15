from usuarios_service import crear_usuario, listar_usuarios

crear_usuario(
    "Andrea",
    "Garcia",
    "andrea.defensa@test.com",
    18000,
    "ACTIVO",
    "frontend"
)

print(listar_usuarios())
