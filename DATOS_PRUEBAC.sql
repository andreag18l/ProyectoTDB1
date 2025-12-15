
--DATOS DE PRUEBA 

COMMIT;
SET TRANSACTION READ WRITE;

--DATOS DE PRUEBA – USUARIO
INSERT INTO USUARIO (
    ID_USUARIO,
    NOMBRE,
    APELLIDO,
    CORREO_ELECTRONICO,
    FECHA_REGISTRO,
    SALARIO_MENSUAL_BASE,
    ESTADO,
    CREADO_POR,
    CREADO_EN,
    MODIFICADO_EN
)
VALUES (
    1,
    'Andrea',
    'Leon',
    'andrea@email.com',
    CURRENT_DATE,
    15000,
    'ACTIVO',
    'admin',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

--DATOS DE PRUEBA – CATEGORIA
EXECUTE PROCEDURE SP_CATEGORIA_INSERT(
    'Ingresos',
    'Ingresos mensuales',
    'ingreso',
    1,
    'admin'
);

--DATOS DE PRUEBA – SUBCATEGORIA
EXECUTE PROCEDURE SP_SUBCATEGORIA_INSERT(
    1,
    'Salario',
    'Salario mensual',
    1,
    0,
    'admin'
);

--DATOS DE PRUEBA – PRESUPUESTO
EXECUTE PROCEDURE SP_PRESUPUESTO_INSERT(
    1,
    'Presupuesto Enero 2025',
    2025,
    1,
    2025,
    1,
    15000,
    10000,
    5000,
    'admin'
);

--DATOS DE PRUEBA – DETALLE PRESUPUESTO
EXECUTE PROCEDURE SP_PRESUPUESTO_DETALLE_INSERT(
    1,
    5,
    4000,
    'Asignación mensual salario',
    'admin'
);

--DATOS DE PRUEBA – META DE AHORRO
EXECUTE PROCEDURE SP_META_INSERT(
    1,
    5,
    'Ahorro anual',
    'Meta de ahorro 2025',
    20000,
    0,
    '2025-01-01',
    '2025-12-31',
    'ALTA',
    'ACTIVA',
    'admin'
);


--DATOS DE PRUEBA – TRANSACCION (INg)
EXECUTE PROCEDURE SP_TRANSACCION_INSERT(
    1,
    1,
    5,
    NULL,
    'ingreso',
    2025,
    1,
    'Salario mensual',
    15000,
    '2025-01-01',
    'transferencia',
    NULL,
    NULL,
    'admin'
);


--DATOS DE PRUEBA – TRANSACCION (AHORRO)
EXECUTE PROCEDURE SP_TRANSACCION_INSERT(
    1,
    1,
    5,
    NULL,
    'ahorro',
    2025,
    1,
    'Ahorro enero',
    1000,
    '2025-01-10',
    'transferencia',
    NULL,
    NULL,
    'admin'
);


--   CONSULTAS DE VERIFICACION
SELECT * FROM USUARIO;
SELECT * FROM CATEGORIA;
SELECT * FROM SUBCATEGORIA;
SELECT * FROM PRESUPUESTO;
SELECT * FROM PRESUPUESTO_DETALLE;
SELECT * FROM META_AHORRO;
SELECT * FROM TRANSACCION;

COMMIT;

