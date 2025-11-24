/* TABLA USUARIO*/
CREATE TABLE usuario (
  id_usuario INTEGER NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  correo_electronico VARCHAR(150) NOT NULL,
  fecha_registro DATE NOT NULL,
  salario_mensual_base NUMERIC(10,2) NOT NULL,
  estado VARCHAR(20) NOT NULL,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_usuario),
  UNIQUE(correo_electronico)
);

/*TABLA PRESUPUESTO */
CREATE TABLE presupuesto (
  id_presupuesto INTEGER NOT NULL,
  id_usuario INTEGER NOT NULL,
  nombre_presupuesto VARCHAR(100) NOT NULL,
  ano_inicio INTEGER NOT NULL,
  mes_inicio INTEGER NOT NULL,
  ano_fin INTEGER NOT NULL,
  mes_fin INTEGER NOT NULL,
  total_ingresos_planificados NUMERIC(10,2),
  total_gastos_planificados NUMERIC(10,2),
  total_ahorro_planificado NUMERIC(10,2),
  fecha_creacion TIMESTAMP NOT NULL,
  estado VARCHAR(20) NOT NULL,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_presupuesto),
  FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)
);


/* TABLA CATEGORIA*/
CREATE TABLE categoria (
  id_categoria INTEGER NOT NULL,
  nombre_categoria VARCHAR(100) NOT NULL,
  descripcion BLOB SUB_TYPE TEXT,
  tipo VARCHAR(20) NOT NULL,
  icono VARCHAR(100),
  color VARCHAR(20),
  orden_presentacion INTEGER,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_categoria)
);

/* TABLA SUBCATEGORIA*/
CREATE TABLE subcategoria (
  id_subcategoria INTEGER NOT NULL,
  id_categoria INTEGER NOT NULL,
  nombre_subcategoria VARCHAR(100) NOT NULL,
  descripcion BLOB SUB_TYPE TEXT,
  activa BOOLEAN,
  es_defecto BOOLEAN,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_subcategoria),
  FOREIGN KEY(id_categoria) REFERENCES categoria(id_categoria)
);

/* TABLA PRESUPUESTO_DETALLE */
CREATE TABLE presupuesto_detalle (
  id_detalle INTEGER NOT NULL,
  id_presupuesto INTEGER NOT NULL,
  id_subcategoria INTEGER NOT NULL,
  monto_mensual_asignado NUMERIC(10,2),
  observaciones BLOB SUB_TYPE TEXT,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_detalle),
  FOREIGN KEY(id_presupuesto) REFERENCES presupuesto(id_presupuesto),
  FOREIGN KEY(id_subcategoria) REFERENCES subcategoria(id_subcategoria)
);

/* TABLA OBLIGACION_FIJA */
CREATE TABLE obligacion_fija (
  id_obligacion INTEGER NOT NULL,
  id_usuario INTEGER NOT NULL,
  id_subcategoria INTEGER NOT NULL,
  nombre_obligacion VARCHAR(100) NOT NULL,
  descripcion BLOB SUB_TYPE TEXT,
  monto_mensual NUMERIC(10,2) NOT NULL,
  dia_vencimiento INTEGER NOT NULL,
  vigente BOOLEAN,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_obligacion),
  FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario),
  FOREIGN KEY(id_subcategoria) REFERENCES subcategoria(id_subcategoria)
);

/* TABLA TRANSACCION */
CREATE TABLE transaccion (
  id_transaccion INTEGER NOT NULL,
  id_usuario INTEGER NOT NULL,
  id_presupuesto INTEGER NOT NULL,
  id_subcategoria INTEGER NOT NULL,
  id_obligacion INTEGER,
  tipo VARCHAR(20) NOT NULL,
  ano INTEGER NOT NULL,
  mes INTEGER NOT NULL,
  descripcion BLOB SUB_TYPE TEXT,
  monto NUMERIC(10,2) NOT NULL,
  fecha DATE NOT NULL,
  metodo_pago VARCHAR(50),
  num_factura VARCHAR(50),
  observaciones BLOB SUB_TYPE TEXT,
  fecha_registro TIMESTAMP NOT NULL,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_transaccion),
  FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario),
  FOREIGN KEY(id_presupuesto) REFERENCES presupuesto(id_presupuesto),
  FOREIGN KEY(id_subcategoria) REFERENCES subcategoria(id_subcategoria),
  FOREIGN KEY(id_obligacion) REFERENCES obligacion_fija(id_obligacion)
);

/* TABLA META_AHORRO*/
CREATE TABLE meta_ahorro (
  id_meta INTEGER NOT NULL,
  id_usuario INTEGER NOT NULL,
  id_subcategoria INTEGER NOT NULL,
  nombre_meta VARCHAR(100) NOT NULL,
  descripcion BLOB SUB_TYPE TEXT,
  monto_objetivo NUMERIC(10,2) NOT NULL,
  monto_acumulado NUMERIC(10,2),
  fecha_inicio DATE NOT NULL,
  fecha_objetivo DATE NOT NULL,
  prioridad VARCHAR(20),
  estado VARCHAR(20),
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_meta),
  FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario),
  FOREIGN KEY(id_subcategoria) REFERENCES subcategoria(id_subcategoria)
);

/* TABLA ALERTA*/
CREATE TABLE alerta (
  id_alerta INTEGER NOT NULL,
  id_usuario INTEGER NOT NULL,
  id_detalle_presupuesto INTEGER,
  id_obligacion INTEGER,
  id_meta INTEGER,
  tipo_alerta VARCHAR(50),
  titulo VARCHAR(100),
  mensaje BLOB SUB_TYPE TEXT,
  prioridad VARCHAR(20),
  fecha_creacion TIMESTAMP NOT NULL,
  vista BOOLEAN,
  fecha_leida TIMESTAMP,
  creado_por VARCHAR(100),
  modificado_por VARCHAR(100),
  creado_en TIMESTAMP NOT NULL,
  modificado_en TIMESTAMP NOT NULL,
  PRIMARY KEY(id_alerta),
  FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario),
  FOREIGN KEY(id_detalle_presupuesto) REFERENCES presupuesto_detalle(id_detalle),
  FOREIGN KEY(id_obligacion) REFERENCES obligacion_fija(id_obligacion),
  FOREIGN KEY(id_meta) REFERENCES meta_ahorro(id_meta)
);
