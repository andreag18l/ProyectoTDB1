-- dtos prueba
COMMIT;
SET TRANSACTION READ WRITE;
INSERT INTO USUARIO (
    ID_USUARIO, NOMBRE, APELLIDO, CORREO_ELECTRONICO,
    FECHA_REGISTRO, SALARIO_MENSUAL_BASE,
    ESTADO, CREADO_EN, MODIFICADO_EN
)
VALUES (
    3,--cambia 
    'Andrea',
    'Leon',
    'andrea2@mail.com',
    CURRENT_DATE,
    15000.00,
    'ACTIVO',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
SELECT * FROM USUARIO;
SELECT * FROM PRESUPUESTO;


--prueba 2 
INSERT INTO CATEGORIA (
    ID_CATEGORIA,
    NOMBRE_CATEGORIA,
    TIPO,
    CREADO_POR,
    CREADO_EN,
    MODIFICADO_EN
)
VALUES (
    2,
    'Ingresos',
    'INGRESO',
    'admin',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

SELECT * FROM CATEGORIA;
SELECT * 
FROM SUBCATEGORIA
WHERE ID_CATEGORIA = 2;

from categorias_service import crear_categoria

crear_categoria(
    "Alimentación",
    "Gastos de comida",
    "Gasto",
    "food",
    "#FF5733",
    1,
    "frontend"
)

--dtos prueba 
EXECUTE PROCEDURE SP_CATEGORIA_INSERT(
  'Ingresos',
  'Ingresos mensuales',
  'ingreso',
  1,
  'admin'
);

EXECUTE PROCEDURE SP_CATEGORIA_INSERT(
  'Gastos',
  'Gastos del mes',
  'gasto',
  2,
  'admin'
);

EXECUTE PROCEDURE SP_CATEGORIA_INSERT(
  'Ahorro',
  'Ahorros personales',
  'ahorro',
  3,
  'admin'
);

SELECT * FROM USUARIO;
SELECT * FROM PRESUPUESTO;
SELECT * FROM CATEGORIA;


