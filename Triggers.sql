/*DROP TRIGGER BI_SUBCATEGORIA_ID;
DROP TRIGGER TRG_CREAR_SUBCATEGORIA_DEFECTO;
DROP TRIGGER TRG_ACTUALIZAR_META_AHORRO;
DROP TRIGGER TRG_ALERTAS_PRESUPUESTO;

DELETE FROM SUBCATEGORIA;
COMMIT;
DROP GENERATOR GEN_SUBCATEGORIA_ID;
CREATE GENERATOR GEN_SUBCATEGORIA_ID;*/


--   TRIGGER AUTOINCREMENTO SUBCATEGORIA

SET TERM ^ ;

CREATE TRIGGER BI_SUBCATEGORIA_ID
FOR SUBCATEGORIA
ACTIVE BEFORE INSERT
AS
BEGIN
  IF (NEW.ID_SUBCATEGORIA IS NULL) THEN
    NEW.ID_SUBCATEGORIA = GEN_ID(GEN_SUBCATEGORIA_ID, 1);
END^

-- TRIGGER 1: SUBCATEGORÍA POR DEFECTO
  
CREATE TRIGGER TRG_CREAR_SUBCATEGORIA_DEFECTO
FOR CATEGORIA
ACTIVE AFTER INSERT
AS
BEGIN
  INSERT INTO SUBCATEGORIA (
      ID_CATEGORIA,
      NOMBRE_SUBCATEGORIA,
      DESCRIPCION,
      ACTIVA,
      ES_DEFECTO,
      CREADO_POR,
      CREADO_EN
  )
  VALUES (
      NEW.ID_CATEGORIA,
      'General',
      'Subcategoría generada automáticamente',
      1,
      1,
      NEW.CREADO_POR,
      CURRENT_TIMESTAMP
  );
END^


-- TRIGGER 2: ACTUALIZAR META AHORRO

CREATE TRIGGER TRG_ACTUALIZAR_META_AHORRO2
FOR TRANSACCION
ACTIVE AFTER INSERT
AS
DECLARE VARIABLE v_idMeta INT;
DECLARE VARIABLE v_acumulado NUMERIC(12,2);
DECLARE VARIABLE v_objetivo NUMERIC(12,2);
DECLARE VARIABLE v_nuevoMonto NUMERIC(12,2);
BEGIN
  /* Solo continuar si es ahorro */
  IF (NEW.TIPO = 'ahorro') THEN
  BEGIN
    /* Buscar meta activa */
    SELECT ID_META, MONTO_ACUMULADO, MONTO_OBJETIVO
    FROM META_AHORRO
    WHERE ID_SUBCATEGORIA = NEW.ID_SUBCATEGORIA
      AND ESTADO = 'en_progreso'
    INTO :v_idMeta, :v_acumulado, :v_objetivo;

    /* Si no hay meta activa, NO usar EXIT: simplemente no hacer nada */
    IF (v_idMeta IS NOT NULL) THEN
    BEGIN
      /* Calcular nuevo acumulado */
      v_nuevoMonto = COALESCE(v_acumulado, 0) + NEW.MONTO;

      /* Actualizar acumulado */
      UPDATE META_AHORRO
      SET MONTO_ACUMULADO = :v_nuevoMonto,
          MODIFICADO_EN = CURRENT_TIMESTAMP
      WHERE ID_META = :v_idMeta;

      /* Si completó la meta */
      IF (v_nuevoMonto >= v_objetivo) THEN
        UPDATE META_AHORRO
        SET ESTADO = 'completada',
            MODIFICADO_EN = CURRENT_TIMESTAMP
        WHERE ID_META = :v_idMeta;
    END
  END
END;



--   TRIGGER 3: ALERTAS PRESUPUESTO (80% y 100%) 

CREATE TRIGGER TRG_ALERTAS_PRESUPUESTO
FOR TRANSACCION
ACTIVE AFTER INSERT
AS
DECLARE VARIABLE v_asignado  NUMERIC(12,2);
DECLARE VARIABLE v_ejecutado NUMERIC(12,2);
DECLARE VARIABLE v_porcentaje NUMERIC(5,2);
BEGIN
  SELECT MONTO_MENSUAL_ASIGNADO
  FROM PRESUPUESTO_DETALLE
  WHERE ID_PRESUPUESTO = NEW.ID_PRESUPUESTO
    AND ID_SUBCATEGORIA = NEW.ID_SUBCATEGORIA
  INTO :v_asignado;

  IF (v_asignado IS NOT NULL) THEN
  BEGIN
    SELECT SUM(MONTO)
    FROM TRANSACCION
    WHERE ID_PRESUPUESTO = NEW.ID_PRESUPUESTO
      AND ID_SUBCATEGORIA = NEW.ID_SUBCATEGORIA
      AND ANO = NEW.ANO
      AND MES = NEW.MES
    INTO :v_ejecutado;

    v_ejecutado = COALESCE(v_ejecutado, 0);
    v_porcentaje = (v_ejecutado / v_asignado) * 100;

    IF (v_porcentaje >= 80 AND v_porcentaje < 100) THEN
    BEGIN
      INSERT INTO ALERTA (
        ID_USUARIO, TIPO_ALERTA, TITULO, MENSAJE,
        PRIORIDAD, FECHA_CREACION, CREADO_EN
      )
      VALUES (
        NEW.ID_USUARIO,
        'presupuesto_80',
        'Presupuesto al 80%',
        'Se ha consumido el 80% del presupuesto asignado.',
        'advertencia',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
      );
    END

    IF (v_porcentaje >= 100) THEN
    BEGIN
      INSERT INTO ALERTA (
        ID_USUARIO, TIPO_ALERTA, TITULO, MENSAJE,
        PRIORIDAD, FECHA_CREACION, CREADO_EN
      )
      VALUES (
        NEW.ID_USUARIO,
        'presupuesto_100',
        'Presupuesto agotado',
        'Has alcanzado o superado el presupuesto mensual.',
        'critica',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
      );
    END
  END
END;



--trigger 4
SET TERM !! ;

CREATE TRIGGER TRG_ALERTAS_META
FOR META_AHORRO
ACTIVE AFTER UPDATE
AS
DECLARE VARIABLE v_porcentaje NUMERIC(5,2);
BEGIN
  v_porcentaje = (NEW.MONTO_ACUMULADO / NEW.MONTO_OBJETIVO) * 100;

  IF (v_porcentaje >= 50 AND OLD.MONTO_ACUMULADO < (NEW.MONTO_OBJETIVO / 2)) THEN
  BEGIN
    INSERT INTO ALERTA (
      ID_USUARIO, ID_META, TIPO_ALERTA, TITULO, MENSAJE,
      PRIORIDAD, FECHA_CREACION, CREADO_EN
    )
    VALUES (
      NEW.ID_USUARIO,
      NEW.ID_META,
      'meta_50',
      'Meta al 50%',
      'Has alcanzado la mitad de tu meta de ahorro',
      'informativa',
      CURRENT_TIMESTAMP,
      CURRENT_TIMESTAMP
    );
  END

  IF (v_porcentaje >= 100 AND OLD.ESTADO <> 'completada') THEN
  BEGIN
    INSERT INTO ALERTA (
      ID_USUARIO, ID_META, TIPO_ALERTA, TITULO, MENSAJE,
      PRIORIDAD, FECHA_CREACION, CREADO_EN
    )
    VALUES (
      NEW.ID_USUARIO,
      NEW.ID_META,
      'meta_completada',
      'Meta completada',
      '¡Felicidades! Lograste tu meta de ahorro',
      'critica',
      CURRENT_TIMESTAMP,
      CURRENT_TIMESTAMP
    );
  END
END!!

SET TERM ;!!
