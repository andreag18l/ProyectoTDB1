/* Usuarios y presupuestos */
SELECT u.nombre, u.apellido, p.nombre_presupuesto, p.estado
FROM usuario u
LEFT JOIN presupuesto p ON u.id_usuario = p.id_usuario;

/* Categorías y subcategorías */
SELECT c.nombre_categoria, s.nombre_subcategoria, s.activa
FROM categoria c
LEFT JOIN subcategoria s ON c.id_categoria = s.id_categoria;

/* Transacciones con usuario y categoría */
SELECT u.nombre, t.tipo, t.monto, t.fecha, c.nombre_categoria
FROM transaccion t
LEFT JOIN usuario u ON t.id_usuario = u.id_usuario
LEFT JOIN subcategoria s ON t.id_subcategoria = s.id_subcategoria
LEFT JOIN categoria c ON s.id_categoria = c.id_categoria;

/* Obligaciones fijas con usuario */
SELECT u.nombre, u.apellido, o.nombre_obligacion, o.monto_mensual, o.dia_vencimiento
FROM obligacion_fija o
LEFT JOIN usuario u ON o.id_usuario = u.id_usuario;

/* Metas de ahorro con usuario */
SELECT u.nombre, m.nombre_meta, m.monto_objetivo, m.monto_acumulado
FROM meta_ahorro m
LEFT JOIN usuario u ON m.id_usuario = u.id_usuario;

/* Alertas con información relacionada */
SELECT a.titulo, a.tipo_alerta, a.prioridad, u.nombre
FROM alerta a
LEFT JOIN usuario u ON a.id_usuario = u.id_usuario
LEFT JOIN presupuesto_detalle pd ON a.id_detalle_presupuesto = pd.id_detalle;
