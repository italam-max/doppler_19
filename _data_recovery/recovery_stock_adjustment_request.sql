-- Recuperacion de historial: stock.adjustment.request (almx_stock_adjustment_approval)
-- Origen: produccion 16, 434 solicitudes (folios AJU/2026/0001 a AJU/2026/0448), ids conservados.
-- Despues de correr: la secuencia de folios (ir.sequence) se ajusta por ORM a 449.
BEGIN;
INSERT INTO stock_adjustment_request (id,name,state,requester_id,approver_id,reason,rejection_reason,date_request,date_resolved,adjustment_lines_json,quant_ids_json,create_date,create_uid,write_date,write_uid) VALUES
(1,'AJU/2026/0001','rejected',35656,12,'prueba','prueba','2026-04-06 18:02:07','2026-04-18 00:40:23','[{"product": "PRUEBA PRUEBA", "location": "Merma Alamex/TI", "qty_system": 87.0, "qty_counted": 1.0, "diff": -86.0, "lot": ""}]','[{"id": 203166, "inventory_quantity": 1.0}]','2026-04-06 18:02:07',35656,'2026-04-18 00:40:23',12),
(2,'AJU/2026/0002','rejected',35656,12,'prueba','test','2026-04-06 18:03:43','2026-04-06 18:04:19','[{"product": "Mult\u00edmetro Digital KN8056", "location": "Alamex / Herramientas de Trabajo Cris", "qty_system": 0.0, "qty_counted": 4.0, "diff": 4.0, "lot": ""}]','[{"id": 148238, "inventory_quantity": 4.0}]','2026-04-06 18:03:43',35656,'2026-04-06 18:04:19',12),
(3,'AJU/2026/0003','approved',1247,12,'Se solicita ajuste de 1 pc positiva por cambio de motor de operador de acuerdo al OUT29501, realiza Mantenimiento el cambio.',NULL,'2026-04-06 19:06:17','2026-04-06 20:50:57','[{"product": "[ALAM-5003-2] Motor con Engrane de Operador H (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 2/ALM-3 2-D1", "qty_system": 48.0, "qty_counted": 49.0, "diff": 1.0, "lot": ""}]','[{"id": 205950, "inventory_quantity": 49.0}]','2026-04-06 19:06:17',1247,'2026-04-06 20:50:56',12),
(4,'AJU/2026/0004','approved',882,12,'Laboratorio nos dio estos imanes para poder validar el pick completo.',NULL,'2026-04-07 17:00:14','2026-04-07 17:03:55','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 25", "qty_system": 0.0, "qty_counted": 4.0, "diff": 4.0, "lot": ""}]','[{"id": 208130, "inventory_quantity": 4.0}]','2026-04-07 17:00:14',882,'2026-04-07 17:03:54',12),
(5,'AJU/2026/0005','approved',1054,12,'Se necesita el ajuste para el ingreso de las computadoras para GDL',NULL,'2026-04-09 16:46:41','2026-04-18 00:40:35','[{"product": "[LPT-ASUS-X1504VA] Laptop Asus (Plateada, X1504VA)", "location": "Physical Locations/WHTL/Information Technologies/IT Stock", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": "T7N0CX05F066318"}]','[{"id": 208245, "inventory_quantity": 1.0}]','2026-04-09 16:46:41',1054,'2026-04-18 00:40:34',12),
(6,'AJU/2026/0006','approved',1054,12,'Se necesita el ajuste para el ingreso de la laptop para GDL',NULL,'2026-04-09 16:48:05','2026-04-11 19:19:17','[{"product": "[LPT-ASUS-X1504VA] Laptop Asus (Plateada, X1504VA)", "location": "Physical Locations/WHTL/Information Technologies/IT Stock", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": "T7N0CX05E932316"}]','[{"id": 208246, "inventory_quantity": 1.0}]','2026-04-09 16:48:05',1054,'2026-04-11 19:19:16',12),
(7,'AJU/2026/0007','approved',1247,12,'Necesito el ingreso de 1 pz del motor izq el cual se tomo del operador',NULL,'2026-04-10 19:46:21','2026-04-11 19:19:04','[{"product": "[ALAM-5003-1] Motor con Engrane de Operador H (Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 3/ALM-3 3-D1", "qty_system": 54.0, "qty_counted": 55.0, "diff": 1.0, "lot": ""}]','[{"id": 194291, "inventory_quantity": 55.0}]','2026-04-10 19:46:21',1247,'2026-04-11 19:19:04',12),
(8,'AJU/2026/0008','approved',1247,12,'Me ayudas con ingreso de la puerta que se armo con el operador derecho.',NULL,'2026-04-10 19:48:21','2026-04-11 19:17:51','[{"product": "[CR80 21 H2 INOX] Puerta de Cabina H Autom\u00e1tico Inoxidable (800 x 2100 mm, Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208331, "inventory_quantity": 1.0}]','2026-04-10 19:48:21',1247,'2026-04-11 19:17:51',12),
(9,'AJU/2026/0009','approved',1247,12,'Motivo: Necesito el ingreso de 1 pz del motor izq el cual se tomo del operador',NULL,'2026-04-10 20:16:16','2026-04-11 19:17:37','[{"product": "[ALAM-5003-2] Motor con Engrane de Operador H (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 2/ALM-3 2-D1", "qty_system": 49.0, "qty_counted": 50.0, "diff": 1.0, "lot": ""}]','[{"id": 205950, "inventory_quantity": 50.0}]','2026-04-10 20:16:16',1247,'2026-04-11 19:17:36',12),
(10,'AJU/2026/0010','rejected',1247,12,'cambia variante','error de Diego','2026-04-11 19:37:02','2026-04-18 00:41:09','[{"product": "[CL90 21 H2 INOX] Puerta de Cabina H Autom\u00e1tico Inoxidable (900 x 2100 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 20.0, "qty_counted": 0.0, "diff": -20.0, "lot": ""}]','[{"id": 200405, "inventory_quantity": 0.0}]','2026-04-11 19:37:02',1247,'2026-04-18 00:41:09',12),
(11,'AJU/2026/0011','rejected',1247,12,'xambio varinate','error Diego','2026-04-11 19:37:53','2026-04-18 00:41:28','[{"product": "[CR90 21 H2 INOX] Puerta de Cabina H Autom\u00e1tico Inoxidable (900 x 2100 mm, Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 7.0, "qty_counted": 0.0, "diff": -7.0, "lot": ""}]','[{"id": 200407, "inventory_quantity": 0.0}]','2026-04-11 19:37:53',1247,'2026-04-18 00:41:28',12),
(12,'AJU/2026/0012','approved',1247,12,'Me ayudas ingresando una pieza, esta no se tiene en stock ya que se armo OUT29593',NULL,'2026-04-14 15:01:34','2026-04-18 00:41:57','[{"product": "[AREID-BCV-Nj] Display Binario de Cabina Vertical (Naranja, Cuadrado)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208396, "inventory_quantity": 1.0}]','2026-04-14 15:01:34',1247,'2026-04-18 00:41:56',12),
(13,'AJU/2026/0013','approved',1247,12,'Me ayudas ingresando 1 pz a inventario debido a que el control que se tomo no estaba registrado en inventario .OUT29034',NULL,'2026-04-14 15:06:44','2026-04-18 00:42:06','[{"product": "[ARElC-02MR40A15kw] Control MR VVVF (Alam 02 -40A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208397, "inventory_quantity": 1.0}]','2026-04-14 15:06:44',1247,'2026-04-18 00:42:06',12),
(14,'AJU/2026/0014','approved',1247,12,'ME ayudas realizao ingresando 1 caja de inspeccion para el OUT 29034',NULL,'2026-04-14 15:09:58','2026-04-18 00:42:50','[{"product": "[ALAM-1031] Caja De Inspecci\u00f3n Paralelo", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208398, "inventory_quantity": 1.0}]','2026-04-14 15:09:58',1247,'2026-04-18 00:42:50',12),
(15,'AJU/2026/0015','approved',1247,12,'Daniel Benitez, me regreso dos valvulas ue tenua en su lugar de trabajo',NULL,'2026-04-14 17:33:23','2026-04-18 00:43:08','[{"product": "[ALAM-4009-2] Valvula Para Bomba Hidr\u00e1ulica 12L / 3Kw (24v. dc)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 5/ALM-3 5-A1", "qty_system": 17.0, "qty_counted": 19.0, "diff": 2.0, "lot": ""}]','[{"id": 205042, "inventory_quantity": 19.0}]','2026-04-14 17:33:23',1247,'2026-04-18 00:43:08',12),
(16,'AJU/2026/0016','approved',1247,12,'ajuste inventario por cambio de variante',NULL,'2026-04-14 17:53:39','2026-04-18 00:47:21','[{"product": "Base para Zapata (5 mm 650 kg)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 54.0, "diff": 54.0, "lot": ""}]','[{"id": 208404, "inventory_quantity": 54.0}]','2026-04-14 17:53:39',1247,'2026-04-18 00:47:20',12),
(17,'AJU/2026/0017','approved',1247,12,'ingreso por ajuste de inventario de variante se agrgaron kilogramos de la zapata',NULL,'2026-04-14 17:55:33','2026-04-18 00:47:52','[{"product": "Base para Zapata (9 mm 1350 kg)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 26.0, "diff": 26.0, "lot": ""}]','[{"id": 208405, "inventory_quantity": 26.0}]','2026-04-14 17:55:33',1247,'2026-04-18 00:47:52',12),
(18,'AJU/2026/0018','approved',1247,12,'ingreso por ajuste de inventario de variante se agrego kilogramos de la zapata',NULL,'2026-04-14 17:57:03','2026-04-18 00:50:35','[{"product": "Base para Zapata (16 mm 1730 kg)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 291.0, "diff": 291.0, "lot": ""}]','[{"id": 208406, "inventory_quantity": 291.0}]','2026-04-14 17:57:03',1247,'2026-04-18 00:50:34',12),
(19,'AJU/2026/0019','approved',1247,12,'Me ayudas a ingresar a INV 6 soportes que se tienen en stock',NULL,'2026-04-14 22:24:48','2026-04-18 00:50:43','[{"product": "[ARMS-AMRL-L] Soporte Alamex MRL-L ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 6.0, "diff": 6.0, "lot": ""}]','[{"id": 208410, "inventory_quantity": 6.0}]','2026-04-14 22:24:48',1247,'2026-04-18 00:50:43',12),
(20,'AJU/2026/0020','rejected',1247,12,'me ayudas con un ajuste positivo','duplicado','2026-04-14 23:09:22','2026-04-18 00:52:34','[{"product": "[ARMS-AMRL-L] Soporte Alamex MRL-L ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 7.0, "diff": 7.0, "lot": ""}]','[{"id": 208410, "inventory_quantity": 7.0}]','2026-04-14 23:09:22',1247,'2026-04-18 00:52:34',12),
(21,'AJU/2026/0021','approved',1247,12,'Me ayudas con ingreso, teniamos duda con el amperaje de este variador y los HP pero este es el dato correcto',NULL,'2026-04-15 16:04:19','2026-04-18 00:53:14','[{"product": "[ALAM-1181-7] Variador Yaskawa L1000E (380V/25hp/39A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208422, "inventory_quantity": 1.0}]','2026-04-15 16:04:19',1247,'2026-04-18 00:53:13',12),
(22,'AJU/2026/0022','approved',1247,12,'e ayudas con ajuste marco negativo en stock doppler por tema de la validacion del OUT29417',NULL,'2026-04-15 18:02:32','2026-04-18 00:53:25','[{"product": "[01-CNT-MR02-65A-11] Control MR Hidr\u00e1ulico (Alam 02- 65A)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 208447, "inventory_quantity": 0.0}]','2026-04-15 18:02:31',1247,'2026-04-18 00:53:24',12),
(23,'AJU/2026/0023','approved',1247,12,'por favor a cero existencia  de stockoppler',NULL,'2026-04-15 22:24:01','2026-04-18 00:53:33','[{"product": "[ALAM-2012] Base Para Mini Relevador 8 Pins", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -10.0, "qty_counted": 0.0, "diff": 10.0, "lot": ""}]','[{"id": 208464, "inventory_quantity": 0.0}]','2026-04-15 22:24:01',1247,'2026-04-18 00:53:33',12),
(24,'AJU/2026/0024','approved',1247,12,'ME ayudas a hacer el ajuste por 2 piezas que se fueron en el OUT29276 el cual cacelo sinue y el pick se valido con el SKU anterior 01-RES-ALU-019H-300W',NULL,'2026-04-15 22:41:51','2026-04-18 00:53:43','[{"product": "[ALAM-1191-018] Resistencia De Aluminio (19 Ohms - 3 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 95.0, "qty_counted": 97.0, "diff": 2.0, "lot": ""}]','[{"id": 207900, "inventory_quantity": 97.0}]','2026-04-15 22:41:51',1247,'2026-04-18 00:53:43',12),
(25,'AJU/2026/0025','approved',1247,12,'me ayudas aponer en cero se transfierieron a almacen 2  para el OUT 29637',NULL,'2026-04-16 16:54:39','2026-04-18 00:53:58','[{"product": "[ALAM-2178] Sardinel Para Puerta Autom\u00e1tica (45 mm)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 146807, "inventory_quantity": 0.0}]','2026-04-16 16:54:39',1247,'2026-04-18 00:53:57',12),
(26,'AJU/2026/0026','approved',1247,12,'ME ayudas a hacer el ajuste por 2 piezas que se fueron en el OUT29276 el cual cacelo sinue y el pick se valido con el SKU anterior 01-RES-ALU-019H-300W',NULL,'2026-04-16 17:47:15','2026-04-18 00:54:56','[{"product": "[ALAM-1191-018] Resistencia De Aluminio (19 Ohms - 3 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 95.0, "qty_counted": 93.0, "diff": -2.0, "lot": ""}]','[{"id": 207900, "inventory_quantity": 93.0}]','2026-04-16 17:47:15',1247,'2026-04-18 00:54:55',12),
(27,'AJU/2026/0027','approved',1247,12,'Por favor me ayudas a generar este ingreso ya que las puertas de pieso estan invnertidas con las de cabina',NULL,'2026-04-16 19:47:55','2026-04-18 00:56:12','[{"product": "[PPCMIS8021] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Central)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 63.0, "diff": 63.0, "lot": ""}]','[{"id": 208484, "inventory_quantity": 63.0}]','2026-04-16 19:47:55',1247,'2026-04-18 00:56:12',12),
(28,'AJU/2026/0028','approved',1247,12,'Por favor me ayudas a generar esta salida ya que las puertas de cabina estan inverrtidas con las de piso',NULL,'2026-04-16 19:49:06','2026-04-18 00:56:43','[{"product": "[PUE-CAB-MIT-800x2100-CEN] Puerta de Cabina Autom\u00e1tica Inoxidable (MITSUBISHI) (Central)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 62.0, "qty_counted": 0.0, "diff": -62.0, "lot": ""}]','[{"id": 201579, "inventory_quantity": 0.0}]','2026-04-16 19:49:06',1247,'2026-04-18 00:56:43',12),
(29,'AJU/2026/0029','approved',1247,12,'Para Validar el OUT 29654',NULL,'2026-04-16 22:41:56','2026-04-18 00:58:14','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 12.0, "diff": 12.0, "lot": ""}]','[{"id": 208498, "inventory_quantity": 12.0}]','2026-04-16 22:41:56',1247,'2026-04-18 00:58:14',12),
(30,'AJU/2026/0030','approved',1247,12,'me ayudas a Ajustar cantidad en el Inv estos imanes los proporciono Lab  OUT 29585',NULL,'2026-04-17 15:23:44','2026-04-18 00:58:26','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 16.0, "diff": 16.0, "lot": ""}]','[{"id": 208498, "inventory_quantity": 16.0}]','2026-04-17 15:23:43',1247,'2026-04-18 00:58:25',12),
(31,'AJU/2026/0031','approved',1247,12,'Me ayudas a poner en Cero salida con el OUT29637',NULL,'2026-04-20 14:58:46','2026-04-21 17:55:12','[{"product": "[ALAM-2178] Sardinel Para Puerta Autom\u00e1tica (45 mm)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -4.38, "qty_counted": 0.0, "diff": 4.38, "lot": ""}]','[{"id": 208478, "inventory_quantity": 0.0}]','2026-04-20 14:58:45',1247,'2026-04-21 17:55:12',12),
(32,'AJU/2026/0032','approved',1247,12,'Ajuste de Puerta Mitsubishi  SKU incorrecto  y se archiva PPCMIS8021 63 pz',NULL,'2026-04-20 15:26:56','2026-04-21 17:55:01','[{"product": "[PUE-CAB-MIT-800x2100-CEN] Puerta de Cabina Autom\u00e1tica Inoxidable (MITSUBISHI) (Central)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 63.0, "diff": 63.0, "lot": ""}]','[{"id": 208553, "inventory_quantity": 63.0}]','2026-04-20 15:26:56',1247,'2026-04-21 17:55:01',12),
(33,'AJU/2026/0033','approved',1247,12,'Ajuste inventarios cambio de sku se archiva este.',NULL,'2026-04-20 15:28:56','2026-04-21 17:54:14','[{"product": "[PPRMIS8021] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 205302, "inventory_quantity": 0.0}]','2026-04-20 15:28:56',1247,'2026-04-21 17:54:14',12),
(34,'AJU/2026/0034','approved',1247,12,'Ajuste inventarios cambio de sku se archiva este.',NULL,'2026-04-20 15:29:08','2026-04-21 17:53:56','[{"product": "[LL80X] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 25.0, "qty_counted": 0.0, "diff": -25.0, "lot": ""}]','[{"id": 202013, "inventory_quantity": 0.0}]','2026-04-20 15:29:08',1247,'2026-04-21 17:53:55',12),
(35,'AJU/2026/0035','approved',1247,12,'Ajuste inventarios cambio de sku se archiva este.',NULL,'2026-04-20 15:29:16','2026-04-21 17:53:07','[{"product": "[PPRMIS8021] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 25.0, "qty_counted": 0.0, "diff": -25.0, "lot": ""}]','[{"id": 202014, "inventory_quantity": 0.0}]','2026-04-20 15:29:16',1247,'2026-04-21 17:53:07',12),
(36,'AJU/2026/0036','approved',1247,12,'Ajuste inventarios cambio de sku se archiva este.',NULL,'2026-04-20 15:29:28','2026-04-21 17:51:10','[{"product": "[PPCMIS8021] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Central)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 63.0, "qty_counted": 0.0, "diff": -63.0, "lot": ""}]','[{"id": 208484, "inventory_quantity": 0.0}]','2026-04-20 15:29:28',1247,'2026-04-21 17:51:09',12),
(37,'AJU/2026/0037','approved',1247,12,'Me ayudas a actualizar el Inve +1',NULL,'2026-04-20 19:31:20','2026-04-21 17:48:58','[{"product": "[ALAM-1132-022] Bot\u00f3n Slim Cuadrado (5)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 13/ALM-3 13-F1", "qty_system": 164.0, "qty_counted": 165.0, "diff": 1.0, "lot": ""}]','[{"id": 207251, "inventory_quantity": 165.0}]','2026-04-20 19:31:20',1247,'2026-04-21 17:48:57',12),
(38,'AJU/2026/0038','approved',1247,12,'me ayudas a actualizar el inve +1',NULL,'2026-04-20 19:32:09','2026-04-21 17:47:30','[{"product": "[ALAM-1132-039] Bot\u00f3n Slim Cuadrado (PB)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 13/ALM-3 13-F1", "qty_system": 44.0, "qty_counted": 45.0, "diff": 1.0, "lot": ""}]','[{"id": 207289, "inventory_quantity": 45.0}]','2026-04-20 19:32:09',1247,'2026-04-21 17:47:29',12),
(39,'AJU/2026/0039','approved',1247,12,'Me ayudas con ingresar 1 Tarjeta para validar el OUT 29690 esta tarjeta se retiro de un variador de Merma .',NULL,'2026-04-21 15:24:35','2026-04-21 17:47:20','[{"product": "[ALAM-1238] Tarjeta Cerebro Para Control Alamex Inteligente ICM", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208610, "inventory_quantity": 1.0}]','2026-04-21 15:24:35',1247,'2026-04-21 17:47:19',12),
(40,'AJU/2026/0040','approved',1247,12,'ajuste',NULL,'2026-04-21 18:02:06','2026-04-21 18:39:26','[{"product": "[PUE-CAB-MIT-800x2100-CEN] Puerta de Cabina Autom\u00e1tica Inoxidable (MITSUBISHI) (Central)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 63.0, "qty_counted": 3.0, "diff": -60.0, "lot": ""}]','[{"id": 208553, "inventory_quantity": 3.0}]','2026-04-21 18:02:06',1247,'2026-04-21 18:39:26',12),
(41,'AJU/2026/0041','approved',1247,12,'ajuste',NULL,'2026-04-21 18:03:49','2026-04-21 18:39:36','[{"product": "[PUE-PIS-MIT-800x2100-CEN] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Central)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 21.0, "qty_counted": 63.0, "diff": 42.0, "lot": ""}]','[{"id": 201580, "inventory_quantity": 63.0}]','2026-04-21 18:03:49',1247,'2026-04-21 18:39:35',12),
(42,'AJU/2026/0042','rejected',1247,12,'ajuste','codigo mal','2026-04-21 18:04:58','2026-04-21 18:40:08','[{"product": "[LL80X] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Izquierda)", "location": "Physical Locations/WHTL/Recepci\u00f3n", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208631, "inventory_quantity": 3.0}]','2026-04-21 18:04:58',1247,'2026-04-21 18:40:08',12),
(43,'AJU/2026/0043','approved',1247,12,'ajuste',NULL,'2026-04-21 18:07:28','2026-04-21 18:16:30','[{"product": "Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2000 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208632, "inventory_quantity": 3.0}]','2026-04-21 18:07:28',1247,'2026-04-21 18:16:29',12),
(44,'AJU/2026/0044','approved',1247,12,'ajuste',NULL,'2026-04-21 18:12:32','2026-04-21 18:16:20','[{"product": "[LL80X] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2100 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208636, "inventory_quantity": 3.0}]','2026-04-21 18:12:32',1247,'2026-04-21 18:16:19',12),
(45,'AJU/2026/0045','approved',1247,12,'ajuste',NULL,'2026-04-21 18:12:59','2026-04-21 18:16:15','[{"product": "Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2000 mm, Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208637, "inventory_quantity": 3.0}]','2026-04-21 18:12:59',1247,'2026-04-21 18:16:14',12),
(46,'AJU/2026/0046','approved',1247,12,'ajuste',NULL,'2026-04-21 18:41:54','2026-04-21 18:42:28','[{"product": "[PUE-PIS-MIT-800x2100-DER] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208639, "inventory_quantity": 3.0}]','2026-04-21 18:41:54',1247,'2026-04-21 18:42:27',12),
(47,'AJU/2026/0047','approved',1247,12,'ajuste',NULL,'2026-04-21 18:43:04','2026-04-21 18:45:10','[{"product": "[xx] Puerta de Piso Autom\u00e1tica Inoxidable (MITSUBISHI) (800 x 2000 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 3.0, "qty_counted": 0.0, "diff": -3.0, "lot": ""}]','[{"id": 208632, "inventory_quantity": 0.0}]','2026-04-21 18:43:04',1247,'2026-04-21 18:45:10',12),
(48,'AJU/2026/0048','approved',1247,12,'Por favor ajustar la cantidad a Cero en Almacén 1 en el siguiente movimiento ajustar a +3',NULL,'2026-04-23 16:57:24','2026-04-25 17:47:33','[{"product": "[04-MAQ-TREN-1000-9KW] M\u00e1quina Tracci\u00f3n Con Engrane 1000 Kg 1 m/s 9 Kw ALMSTRG", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 207873, "inventory_quantity": 0.0}]','2026-04-23 16:57:24',1247,'2026-04-25 17:47:33',12),
(49,'AJU/2026/0049','approved',1247,12,'Por favor ajustar la cantidad +4 para un total de 4 maquinas en stock en almacén 2.',NULL,'2026-04-23 16:58:24','2026-04-25 17:42:26','[{"product": "[04-MAQ-TREN-1000-9KW] M\u00e1quina Tracci\u00f3n Con Engrane 1000 Kg 1 m/s 9 Kw ALMSTRG", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 4.0, "diff": 3.0, "lot": ""}]','[{"id": 199848, "inventory_quantity": 4.0}]','2026-04-23 16:58:24',1247,'2026-04-25 17:42:26',12),
(50,'AJU/2026/0050','approved',1247,12,'Por favor ajustar la cantidad A +3 para un tptal de 6 pz en stock estas maquinas son de 1.2 m/s',NULL,'2026-04-23 17:07:47','2026-04-25 17:41:28','[{"product": "[04-MAQ-TRA-1300-11KW-530x6x12 Strong] M\u00e1quina Tracci\u00f3n Con Engrane 1300 Kg 1 m/s 11 Kw Strong", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 3.0, "qty_counted": 6.0, "diff": 3.0, "lot": ""}]','[{"id": 199849, "inventory_quantity": 6.0}]','2026-04-23 17:07:47',1247,'2026-04-25 17:41:27',12),
(51,'AJU/2026/0051','approved',1247,12,'Por favor ajustar la cantidad  +1 por conteo de Inv',NULL,'2026-04-23 17:38:32','2026-04-25 17:29:18','[{"product": "[MAQ-TRAC-ENG-800KG-7.5kw-220v] M\u00e1quina Tracci\u00f3n Con Engrane 800 Kg 1 m/s 7.5 Kw 220V AC ALAMPLUS (530 x 5 x 10 m)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 5.0, "qty_counted": 6.0, "diff": 1.0, "lot": ""}]','[{"id": 208728, "inventory_quantity": 6.0}]','2026-04-23 17:38:32',1247,'2026-04-25 17:29:18',12),
(52,'AJU/2026/0052','approved',1247,12,'Por favor ajustar la cantidad a +1 por conteo en Inv',NULL,'2026-04-23 17:43:40','2026-04-25 17:24:33','[{"product": "[04-MTGEA-1000-10.4Kw-1.6m/s] M\u00e1quina Tracci\u00f3n Gearless  1000 Kg 1.6 m/s 10.4 Kw ALMK200 2:1", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208729, "inventory_quantity": 1.0}]','2026-04-23 17:43:40',1247,'2026-04-25 17:24:33',12),
(53,'AJU/2026/0053','approved',1247,12,'Por favor ajuste al Inve por conteo positivo +3 estas maquinas son de 2.8 kw',NULL,'2026-04-23 17:45:43','2026-04-25 17:21:47','[{"product": "[MAQ-TRAC-GEAR-450kg-3.0KW] M\u00e1quina Tracci\u00f3n Gearless 450 Kg 1m/s 3 Kw", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208730, "inventory_quantity": 3.0}]','2026-04-23 17:45:43',1247,'2026-04-25 17:21:46',12),
(54,'AJU/2026/0054','approved',882,12,'Se retira esta tarjeta PG-3 de un Variador Black Model 1387 Monarch, para surtir el OUT/29730 de Juan Manuel Espinoza Lopez y solicitan para envio urgente.',NULL,'2026-04-23 18:51:18','2026-04-25 17:20:51','[{"product": "[ALAM-1171-2] Tarjeta Encoder Variador Monarch ME320LN (PG-3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208731, "inventory_quantity": 1.0}]','2026-04-23 18:51:18',882,'2026-04-25 17:20:51',12),
(55,'AJU/2026/0055','approved',1247,12,'Tarjeta extradid de un Variador al cual se le retiro la tarjeta ICM',NULL,'2026-04-23 20:56:14','2026-04-25 17:20:41','[{"product": "[ALAM-1276] Tarjeta Preapertura y Renivelaci\u00f3n - Control Inteligente", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 12/ALM-3 12-B1", "qty_system": 13.0, "qty_counted": 14.0, "diff": 1.0, "lot": ""}]','[{"id": 206603, "inventory_quantity": 14.0}]','2026-04-23 20:56:14',1247,'2026-04-25 17:20:41',12),
(56,'AJU/2026/0056','approved',1054,12,'BUEN DÍA, SOLICITO EL AJUSTE DE INVENTARIO PARA PODER DAR INGRESO A CAMISAS DEL ÁREA DE RH',NULL,'2026-04-24 16:48:28','2026-04-25 17:20:09','[{"product": "[CAM8-RH-46] Camisola  de 8oz (46)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 208771, "inventory_quantity": 3.0}]','2026-04-24 16:48:28',1054,'2026-04-25 17:20:09',12),
(57,'AJU/2026/0057','approved',1054,12,'BUEN DÍA, SOLICITO EL AJUSTE DE INVENTARIO PARA PODER DAR INGRESO A CAMISAS DEL ÁREA DE RH',NULL,'2026-04-24 16:50:31','2026-04-25 17:19:51','[{"product": "[CAM8-RH-34] Camisola  de 8oz (34)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 7.0, "qty_counted": 9.0, "diff": 2.0, "lot": ""}]','[{"id": 125345, "inventory_quantity": 9.0}]','2026-04-24 16:50:31',1054,'2026-04-25 17:19:51',12),
(58,'AJU/2026/0058','approved',1054,12,'BUEN DÍA, SOLICITO EL AJUSTE DE INVENTARIO PARA PODER DAR INGRESO A CAMISAS DEL ÁREA DE RH',NULL,'2026-04-24 16:51:59','2026-04-25 17:19:44','[{"product": "[CAM8-RH-38] Camisola  de 8oz (38)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 12.0, "qty_counted": 13.0, "diff": 1.0, "lot": ""}]','[{"id": 136698, "inventory_quantity": 13.0}]','2026-04-24 16:51:59',1054,'2026-04-25 17:19:44',12),
(59,'AJU/2026/0059','approved',1054,12,'BUEN DÍA, SOLICITO EL AJUSTE DE INVENTARIO PARA PODER DAR INGRESO A GUANTES ANTICORTE DEL ÁREA DE RH',NULL,'2026-04-24 16:54:41','2026-04-25 17:19:29','[{"product": "[G-ANT-CH] Guantes Anticorte (Ch)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 1.0, "qty_counted": 13.0, "diff": 12.0, "lot": ""}]','[{"id": 194077, "inventory_quantity": 13.0}]','2026-04-24 16:54:41',1054,'2026-04-25 17:19:29',12),
(60,'AJU/2026/0060','approved',1054,12,'BUEN DÍA, SOLICITO EL AJUSTE DE INVENTARIO PARA PODER DAR INGRESO A GUANTES ANTICORTE DEL ÁREA DE RH',NULL,'2026-04-24 16:56:21','2026-04-25 17:19:21','[{"product": "[G-ANT-G] Guantes Anticorte (G)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 1.0, "qty_counted": 13.0, "diff": 12.0, "lot": ""}]','[{"id": 136753, "inventory_quantity": 13.0}]','2026-04-24 16:56:21',1054,'2026-04-25 17:19:21',12),
(61,'AJU/2026/0061','approved',1054,12,'BUEN DÍA, SOLICITO EL AJUSTE DE INVENTARIO PARA PODER DAR INGRESO A GUANTES ANTICORTE DEL ÁREA DE RH',NULL,'2026-04-24 17:06:56','2026-04-25 17:19:12','[{"product": "[G-ANT-M] Guantes Anticorte (M)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 0.0, "qty_counted": 12.0, "diff": 12.0, "lot": ""}]','[{"id": 208772, "inventory_quantity": 12.0}]','2026-04-24 17:06:56',1054,'2026-04-25 17:19:12',12),
(62,'AJU/2026/0062','approved',1247,12,'Me ayudas con ajuste positivo +9',NULL,'2026-04-24 20:32:35','2026-04-25 17:19:02','[{"product": "[ALAM-10009-1] Puerta Manual Chapa Chica (Derecha 800x2000)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 13.0, "qty_counted": 22.0, "diff": 9.0, "lot": ""}]','[{"id": 198132, "inventory_quantity": 22.0}]','2026-04-24 20:32:35',1247,'2026-04-25 17:19:02',12),
(63,'AJU/2026/0063','approved',1247,12,'Ajuste positivo +2',NULL,'2026-04-24 20:33:03','2026-04-25 17:18:36','[{"product": "[ALAM-10009-2] Puerta Manual Chapa Chica (Derecha 900x2000)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 15.0, "qty_counted": 17.0, "diff": 2.0, "lot": ""}]','[{"id": 198134, "inventory_quantity": 17.0}]','2026-04-24 20:33:03',1247,'2026-04-25 17:18:36',12),
(64,'AJU/2026/0064','approved',1247,12,'Ajuste positivo +1',NULL,'2026-04-24 20:33:38','2026-04-25 17:18:25','[{"product": "[ALAM-10009-4] Puerta Manual Chapa Chica (izquierda 900x2000)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 11.0, "qty_counted": 12.0, "diff": 1.0, "lot": ""}]','[{"id": 199141, "inventory_quantity": 12.0}]','2026-04-24 20:33:38',1247,'2026-04-25 17:18:24',12),
(65,'AJU/2026/0065','approved',1247,12,'AJuste de +2',NULL,'2026-04-24 20:38:57','2026-04-25 17:17:56','[{"product": "Puerta Manual Chapa Grande (izquiedra 800x2000)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 208782, "inventory_quantity": 2.0}]','2026-04-24 20:38:57',1247,'2026-04-25 17:17:56',12),
(66,'AJU/2026/0066','approved',1247,12,'Ajuste -3',NULL,'2026-04-24 20:40:32','2026-04-25 17:17:26','[{"product": "Puerta Manual Chapa Grande (izquierda 900x2000)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 0.0, "diff": -3.0, "lot": ""}]','[{"id": 207937, "inventory_quantity": 0.0}]','2026-04-24 20:40:32',1247,'2026-04-25 17:17:25',12),
(67,'AJU/2026/0067','rejected',1247,12,'ajuste positivo +1','error Diego','2026-04-27 20:50:37','2026-05-07 21:13:03','[{"product": "[ALAM-1156-2] LOP Botonera de Piso 1 Bot\u00f3n Touch con Display LCD  (1 Boton Subida + Display AZUL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 15/ALM-3 15-B1", "qty_system": 10.0, "qty_counted": 1.0, "diff": -9.0, "lot": ""}]','[{"id": 195064, "inventory_quantity": 1.0}]','2026-04-27 20:50:37',1247,'2026-05-07 21:13:03',12),
(68,'AJU/2026/0068','approved',1247,12,'Me ayudas con el ajuste para poder validar el OUT 29709 este se realizo en Lab',NULL,'2026-04-28 20:19:49','2026-04-29 23:51:13','[{"product": "[ARElC-02MR40A15kw] Control MR VVVF (Alam 02 -40A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208845, "inventory_quantity": 1.0}]','2026-04-28 20:19:49',1247,'2026-04-29 23:51:13',12),
(69,'AJU/2026/0069','approved',1247,12,'Ajuste para validar el OUT 29709',NULL,'2026-04-28 20:20:55','2026-04-29 23:51:06','[{"product": "[ALAM-1033] Caja De Inspecci\u00f3n Serial 02-16 Salida", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 208846, "inventory_quantity": 1.0}]','2026-04-28 20:20:55',1247,'2026-04-29 23:51:06',12),
(70,'AJU/2026/0070','approved',1247,12,'ME ayudas con ajuste psostivo por +1 para validar el OUT 29607',NULL,'2026-04-29 17:03:01','2026-04-29 23:50:59','[{"product": "[ARMS-AMRL-L] Soporte Alamex MRL-L ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 6.0, "qty_counted": 7.0, "diff": 1.0, "lot": ""}]','[{"id": 208410, "inventory_quantity": 7.0}]','2026-04-29 17:03:01',1247,'2026-04-29 23:50:59',12),
(71,'AJU/2026/0071','approved',1247,12,'Me ayudas a ajustar esta cantidad para validar el OUT',NULL,'2026-04-29 18:48:01','2026-05-07 21:11:41','[{"product": "[ALAM-2177] Sardinel Doble para Puerta Telesc\u00f3pica (9 cm )", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.35, "qty_counted": 3.0, "diff": 4.35, "lot": ""}]','[{"id": 207481, "inventory_quantity": 3.0}]','2026-04-29 18:48:01',1247,'2026-05-07 21:11:40',12),
(72,'AJU/2026/0072','approved',1247,12,'Estas puertas se armaron con algunas que teníamos en merma    validar el OUT29694',NULL,'2026-04-29 18:58:50','2026-04-29 23:49:05','[{"product": "Puerta de Piso H Autom\u00e1tico Inoxidable (900 x 2100 mm, Central, 2 Hojas)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 208868, "inventory_quantity": 2.0}]','2026-04-29 18:58:50',1247,'2026-04-29 23:49:05',12),
(73,'AJU/2026/0073','approved',1247,12,'OUT29540 me ayudas con ajuste de +2 para validar el OUT',NULL,'2026-04-29 19:04:24','2026-04-29 23:48:44','[{"product": "[ALAM-1138-007] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 2)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 3.0, "diff": 2.0, "lot": ""}]','[{"id": 208022, "inventory_quantity": 3.0}]','2026-04-29 19:04:24',1247,'2026-04-29 23:48:43',12),
(74,'AJU/2026/0074','approved',1054,12,'Buenos días!, solicito un ajuste de inventario para poder asignar este cargador a un usuario',NULL,'2026-04-29 20:44:30','2026-04-29 23:48:34','[{"product": "[CAR-LPT-LEN0DLX] Cargador Lenovo", "location": "Physical Locations/WHTL/Information Technologies/IT Stock", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": "8SSA10M42697C1SG884171C"}]','[{"id": 208877, "inventory_quantity": 1.0}]','2026-04-29 20:44:30',1054,'2026-04-29 23:48:34',12),
(75,'AJU/2026/0075','approved',1247,12,'Ajuste positivo +1 en sistema 10 total 11',NULL,'2026-04-30 14:42:59','2026-05-07 21:11:27','[{"product": "[ALAM-1156-2] LOP Botonera de Piso 1 Bot\u00f3n Touch con Display LCD  (1 Boton Subida + Display AZUL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 15/ALM-3 15-B1", "qty_system": 10.0, "qty_counted": 11.0, "diff": 1.0, "lot": ""}]','[{"id": 195064, "inventory_quantity": 11.0}]','2026-04-30 14:42:59',1247,'2026-05-07 21:11:27',12),
(76,'AJU/2026/0076','approved',1247,12,'Me ayudas con este ajuste por fa,',NULL,'2026-05-06 16:29:27','2026-05-07 21:10:24','[{"product": "[ALAM-2260] Pasamanos de Cabina 1.41 Mt Terminado Acero Anodizado", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 208991, "inventory_quantity": 2.0}]','2026-05-06 16:29:27',1247,'2026-05-07 21:10:24',12),
(77,'AJU/2026/0077','approved',1247,12,'Me ayudas con ajuste positivo',NULL,'2026-05-06 20:59:10','2026-05-07 21:08:19','[{"product": "[01-DIS-7SE-VERT] Display 7 Segmentos Sin Caja (Rojo) (Vertical)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 14/ALM-3 14-B1", "qty_system": 82.0, "qty_counted": 116.0, "diff": 34.0, "lot": ""}]','[{"id": 195035, "inventory_quantity": 116.0}]','2026-05-06 20:59:10',1247,'2026-05-07 21:08:18',12),
(78,'AJU/2026/0078','approved',1247,12,'Me ayudas a realizar ingreso es para validar el OUT29822',NULL,'2026-05-07 15:24:50','2026-05-07 21:07:59','[{"product": "[ALAM-1042] Caja de inspecci\u00f3n para Control Alamex Inteligente y 02 S (Tarjeta PWL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209003, "inventory_quantity": 1.0}]','2026-05-07 15:24:50',1247,'2026-05-07 21:07:58',12),
(79,'AJU/2026/0079','approved',1247,12,'Por favor ajustar por que se corrije la cantidad de mm la cantidad esta bien lo que no estava correcto era la medida',NULL,'2026-05-07 20:39:57','2026-05-12 22:35:50','[{"product": "Resorte para Puerta de Piso Autom\u00e1tica (400mm x 11 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 27.0, "diff": 27.0, "lot": ""}]','[{"id": 209037, "inventory_quantity": 27.0}]','2026-05-07 20:39:57',1247,'2026-05-12 22:35:49',12),
(80,'AJU/2026/0080','rejected',1247,12,'Ajuste a 0','error encntramos mas 3','2026-05-07 20:40:12','2026-05-07 21:15:10','[{"product": "[ALAM-2224-1] Resorte para Puerta de Piso Autom\u00e1tica (40mm x 11 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 27.0, "qty_counted": 0.0, "diff": -27.0, "lot": ""}]','[{"id": 202614, "inventory_quantity": 0.0}]','2026-05-07 20:40:12',1247,'2026-05-07 21:15:10',12),
(81,'AJU/2026/0081','approved',1247,12,'ajuste',NULL,'2026-05-07 21:14:50','2026-05-07 21:15:17','[{"product": "Resorte para Puerta de Piso Autom\u00e1tica (400mm x 11 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 30.0, "diff": 30.0, "lot": ""}]','[{"id": 209037, "inventory_quantity": 30.0}]','2026-05-07 21:14:50',1247,'2026-05-07 21:15:16',12),
(82,'AJU/2026/0082','approved',1247,12,'ajustes',NULL,'2026-05-07 21:16:08','2026-05-07 21:16:21','[{"product": "[ALAM-2224-1] Resorte para Puerta de Piso Autom\u00e1tica (40mm x 11 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 24.0, "qty_counted": 0.0, "diff": -27.0, "lot": ""}]','[{"id": 202614, "inventory_quantity": 0.0}]','2026-05-07 21:16:08',1247,'2026-05-07 21:16:21',12),
(83,'AJU/2026/0083','approved',1247,12,'La existencias no aplico en almacen 2',NULL,'2026-05-07 22:17:44','2026-05-12 22:35:39','[{"product": "Plataforma Hidr\u00e1ulica 4 Postes (N/A, N/A, Acero Inoxidable Mate, L\u00e1mina Antiderrapante, 2, 1, 220 V. 3F, Thin Film-Transistor (FTF), No Pit, 1550-1649 mm, 1550-1599 mm, Izquierda, 1, 4,000 Kg.)", "location": "Physical Locations/WHTL/Recepci\u00f3n", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208971, "inventory_quantity": 0.0}]','2026-05-07 22:17:44',1247,'2026-05-12 22:35:39',12),
(84,'AJU/2026/0084','approved',1247,12,'Me ayudas con este ingreso, por fa',NULL,'2026-05-07 23:02:16','2026-05-12 22:35:10','[{"product": "[07-PIS-ANIL-130-00] Anillo de sellado para pist\u00f3n 130", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209092, "inventory_quantity": 1.0}]','2026-05-07 23:02:16',1247,'2026-05-12 22:35:09',12),
(85,'AJU/2026/0085','approved',1247,12,'Me ayudas con ajuste, este SKU fue el que creaste ayer, para Hacene.',NULL,'2026-05-08 16:08:19','2026-05-12 22:34:28','[{"product": "[MSI-Disco] Motor Sin Engrane Disco", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209094, "inventory_quantity": 1.0}]','2026-05-08 16:08:19',1247,'2026-05-12 22:34:28',12),
(86,'AJU/2026/0086','approved',1247,12,'ME ayudas con ajuste de menos 1 pieza ya que cuanos de genero el ingreso por medio del IN se recibió 1 pz y cuanso hice la transferencia la hice por 2',NULL,'2026-05-09 16:42:23','2026-05-12 22:33:25','[{"product": "[ALAM-1181-13] Variador Yaskawa L1000E (220/7.5Hp/22A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 5.0, "qty_counted": 4.0, "diff": -1.0, "lot": ""}]','[{"id": 199187, "inventory_quantity": 4.0}]','2026-05-09 16:42:23',1247,'2026-05-12 22:33:24',12),
(87,'AJU/2026/0087','approved',1247,12,'ajuste a cero para dejar en recepción limpio',NULL,'2026-05-09 16:42:55','2026-05-12 22:27:37','[{"product": "[ALAM-1181-13] Variador Yaskawa L1000E (220/7.5Hp/22A)", "location": "Physical Locations/WHTL/Recepci\u00f3n", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 209046, "inventory_quantity": 0.0}]','2026-05-09 16:42:55',1247,'2026-05-12 22:27:36',12),
(88,'AJU/2026/0088','approved',1247,12,'Me ayudas a ingresar una pieza mas por que fue la que se le quito al OUT de Burgos  29560',NULL,'2026-05-12 23:08:45','2026-05-13 19:34:41','[{"product": "[ALAM-5003-2] Motor con Engrane de Operador H (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 2/ALM-3 2-D1", "qty_system": 50.0, "qty_counted": 51.0, "diff": 1.0, "lot": ""}]','[{"id": 205950, "inventory_quantity": 51.0}]','2026-05-12 23:08:45',1247,'2026-05-13 19:34:40',12),
(89,'AJU/2026/0089','rejected',1247,12,'Para Validar OUT29373','fue serial','2026-05-12 23:28:57','2026-05-13 19:34:33','[{"product": "[ALAM-1031] Caja De Inspecci\u00f3n Paralelo", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 2.0, "diff": 1.0, "lot": ""}]','[{"id": 208398, "inventory_quantity": 2.0}]','2026-05-12 23:28:57',1247,'2026-05-13 19:34:33',12),
(90,'AJU/2026/0090','approved',1247,12,'Para Validar OUT29373',NULL,'2026-05-12 23:29:29','2026-05-13 19:34:00','[{"product": "Control MR VVVF (alam 02 - 32 A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209244, "inventory_quantity": 1.0}]','2026-05-12 23:29:29',1247,'2026-05-13 19:34:00',12),
(91,'AJU/2026/0091','approved',1247,12,'ajuste a cero tenemos negativo',NULL,'2026-05-13 00:00:38','2026-05-13 19:33:15','[{"product": "[ALAM-1229] Tarjeta ALPK para Llamadas y Display Tipo Paralelo Para Control Inteligente Alamex y 02S", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -3.0, "qty_counted": 0.0, "diff": 3.0, "lot": ""}]','[{"id": 203911, "inventory_quantity": 0.0}]','2026-05-13 00:00:38',1247,'2026-05-13 19:33:14',12),
(92,'AJU/2026/0092','approved',1247,12,'ajuste a cero tenemos  negativo -2',NULL,'2026-05-13 00:01:12','2026-05-13 19:29:31','[{"product": "[ALAM-1229] Tarjeta ALPK para Llamadas y Display Tipo Paralelo Para Control Inteligente Alamex y 02S", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -2.0, "qty_counted": 0.0, "diff": 2.0, "lot": ""}]','[{"id": 204686, "inventory_quantity": 0.0}]','2026-05-13 00:01:12',1247,'2026-05-13 19:29:30',12),
(93,'AJU/2026/0093','rejected',1247,12,'Sobrantes de Proyecto Valquirico','error diego','2026-05-13 18:07:27','2026-05-13 19:28:11','[{"product": "[ALAM-6005] Amortiguador ALAM 01", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209263, "inventory_quantity": 2.0}]','2026-05-13 18:07:27',1247,'2026-05-13 19:28:11',12),
(94,'AJU/2026/0094','approved',1247,12,'Me ayudas con el ajuste, son lo que llegaron de ope.',NULL,'2026-05-13 19:10:42','2026-05-13 19:26:20','[{"product": "[ALAM-6008] Amortiguador MP 6", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209267, "inventory_quantity": 2.0}]','2026-05-13 19:10:42',1247,'2026-05-13 19:26:19',12),
(95,'AJU/2026/0095','approved',1247,12,'Me ayudas para validar el OUT 29967',NULL,'2026-05-14 15:51:32','2026-05-14 18:20:16','[{"product": "[ALAM-6011] Anclas 10 mm Cable 9-11 con goma (Plateada)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 5.0, "diff": 4.0, "lot": ""}]','[{"id": 202101, "inventory_quantity": 5.0}]','2026-05-14 15:51:32',1247,'2026-05-14 18:20:16',12),
(96,'AJU/2026/0096','approved',1247,12,'Me ayudas con ajuste de 1 pieza para validar el 
NWH/OUT/29973 material entregado a OPE',NULL,'2026-05-14 16:40:32','2026-05-14 18:20:09','[{"product": "[ALAM-1192] Tarjeta Inversor OLVF200-5/V1-E  200w", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209284, "inventory_quantity": 1.0}]','2026-05-14 16:40:32',1247,'2026-05-14 18:20:08',12),
(97,'AJU/2026/0097','approved',1247,12,'Me ayudas a poner en  cero por creación de variante',NULL,'2026-05-15 16:37:30','2026-05-20 20:04:54','[{"product": "[ARMS-90-4] Soporte 90-4 ", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 5.0, "qty_counted": 0.0, "diff": -5.0, "lot": ""}]','[{"id": 209023, "inventory_quantity": 0.0}]','2026-05-15 16:37:30',1247,'2026-05-20 20:04:53',12),
(98,'AJU/2026/0098','approved',1247,12,'Me ayudas a poner en  cero por creación de variante',NULL,'2026-05-15 16:37:38','2026-05-20 20:05:05','[{"product": "[ARMS-90-4] Soporte 90-4 ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 214.0, "qty_counted": 0.0, "diff": -214.0, "lot": ""}]','[{"id": 201996, "inventory_quantity": 0.0}]','2026-05-15 16:37:38',1247,'2026-05-20 20:05:05',12),
(99,'AJU/2026/0099','approved',1247,12,'Me ayudas a poner en  cero por creación de variante',NULL,'2026-05-15 16:38:02','2026-05-20 20:05:11','[{"product": "[ARMS-90-5] Soporte 90-5 ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 201997, "inventory_quantity": 0.0}]','2026-05-15 16:38:02',1247,'2026-05-20 20:05:11',12),
(100,'AJU/2026/0100','approved',1247,12,'por creación de variante',NULL,'2026-05-15 16:41:51','2026-06-02 18:59:27','[{"product": "[ALAM-2127-1] Soporte Alamex para Riel (90-3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 644.0, "diff": 644.0, "lot": ""}]','[{"id": 209311, "inventory_quantity": 644.0}]','2026-05-15 16:41:51',1247,'2026-06-02 18:59:27',12),
(101,'AJU/2026/0101','approved',1247,12,'por creación de variante',NULL,'2026-05-15 16:42:21','2026-06-02 18:59:34','[{"product": "[ALAM-2127-2] Soporte Alamex para Riel (90-4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 219.0, "diff": 219.0, "lot": ""}]','[{"id": 209312, "inventory_quantity": 219.0}]','2026-05-15 16:42:21',1247,'2026-06-02 18:59:33',12),
(102,'AJU/2026/0102','approved',1247,12,'Estas tarjetas fueron las que se le quitaron al controles de rodher',NULL,'2026-05-15 17:27:47','2026-05-15 20:10:03','[{"product": "[ALAM-1230] Tarjeta ALSK", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 11/ALM-3 11-B1", "qty_system": 63.0, "qty_counted": 66.0, "diff": 3.0, "lot": ""}]','[{"id": 206478, "inventory_quantity": 66.0}]','2026-05-15 17:27:47',1247,'2026-05-15 20:10:02',12),
(103,'AJU/2026/0103','approved',1247,12,'cargar existencia para OUT de HACEN',NULL,'2026-05-15 20:06:36','2026-05-15 20:09:56','[{"product": "[ALAM-2014-2 16 mm] INSERTO PARA BASE 28 (16 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 4.0, "diff": 4.0, "lot": ""}]','[{"id": 209323, "inventory_quantity": 4.0}]','2026-05-15 20:06:36',1247,'2026-05-15 20:09:56',12),
(104,'AJU/2026/0104','approved',1247,12,'se saca pieza de LAB',NULL,'2026-05-20 16:15:04','2026-05-20 16:22:38','[{"product": "[ALAM-2072] Cargador De Cable Viajero Plano", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": -1.0, "qty_counted": 1.0, "diff": 2.0, "lot": ""}]','[{"id": 209281, "inventory_quantity": 1.0}]','2026-05-20 16:15:04',1247,'2026-05-20 16:22:37',12),
(105,'AJU/2026/0105','rejected',1247,12,'por creación de variante','son 13 no 10','2026-05-20 22:05:39','2026-05-22 23:49:44','[{"product": "[ALAM-6097-2] Polea de Desvio de Nylon con Flecha (Nylamid 2Gx8x150 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 10.0, "diff": 10.0, "lot": ""}]','[{"id": 209507, "inventory_quantity": 10.0}]','2026-05-20 22:05:39',1247,'2026-05-22 23:49:44',12),
(106,'AJU/2026/0106','approved',1247,12,'ajuste por creación de variación',NULL,'2026-05-20 22:12:49','2026-05-22 23:04:04','[{"product": "[ALAM-6097-1] Polea de Desvio de Nylon con Flecha (Nylamid 9Gx6.5x240 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 4.0, "diff": 4.0, "lot": ""}]','[{"id": 209508, "inventory_quantity": 4.0}]','2026-05-20 22:12:49',1247,'2026-05-22 23:04:03',12),
(107,'AJU/2026/0107','approved',35656,35656,'test',NULL,'2026-05-21 12:37:39','2026-05-21 12:47:06','[{"product": "Ghassan test", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -10.0, "qty_counted": 1.0, "diff": 11.0, "lot": ""}]','[{"id": 209398, "inventory_quantity": 1.0}]','2026-05-21 12:37:39',35656,'2026-05-21 12:47:05',35656),
(108,'AJU/2026/0108','approved',35656,35656,'test',NULL,'2026-05-21 12:38:01','2026-05-21 12:46:51','[{"product": "Ghassan test", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 1", "qty_system": -6.0, "qty_counted": 1.0, "diff": 7.0, "lot": ""}]','[{"id": 209399, "inventory_quantity": 1.0}]','2026-05-21 12:38:01',35656,'2026-05-21 12:46:50',35656),
(109,'AJU/2026/0109','approved',35656,35656,'Ghassan Test',NULL,'2026-05-21 12:59:56','2026-05-21 13:00:26','[{"product": "Ghassan test", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 10.0, "diff": 9.0, "lot": ""}]','[{"id": 209398, "inventory_quantity": 10.0}]','2026-05-21 12:59:56',35656,'2026-05-21 13:00:25',35656),
(110,'AJU/2026/0110','approved',1247,12,'me ayudas con este ajuste, se toma la tarjeta de la devolucion de Lab.',NULL,'2026-05-21 16:45:58','2026-05-22 23:03:43','[{"product": "[ALAM-1254] Tarjeta Encoder E3 - Yaskawa", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209532, "inventory_quantity": 1.0}]','2026-05-21 16:45:58',1247,'2026-05-22 23:03:43',12),
(111,'AJU/2026/0111','approved',1247,12,'Validar OUT29467',NULL,'2026-05-21 18:16:21','2026-05-22 23:03:36','[{"product": "[ALAM-2072] Cargador De Cable Viajero Plano", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209536, "inventory_quantity": 2.0}]','2026-05-21 18:16:21',1247,'2026-05-22 23:03:36',12),
(112,'AJU/2026/0112','approved',1247,12,'me ayudas con el ajuste por el ingreso duplicado del ultimo contenedor',NULL,'2026-05-22 19:12:16','2026-05-28 22:41:42','[{"product": "[ALAM-7049-5] Cable de Acero (Traccion 13 mm 9x19S Nucleo acero)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 10043.0, "qty_counted": 0.0, "diff": -10043.0, "lot": ""}]','[{"id": 198383, "inventory_quantity": 0.0}]','2026-05-22 19:12:16',1247,'2026-05-28 22:41:42',12),
(113,'AJU/2026/0113','approved',1247,12,'cantidad dusplicado por sistema entrada de contenedor.',NULL,'2026-05-22 19:18:00','2026-05-22 23:20:49','[{"product": "[ALAM-7049-4] Cable de Acero (12 mm 8x19 Traccion Alma Fibra)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 11267.0, "qty_counted": 9267.0, "diff": -2000.0, "lot": ""}]','[{"id": 198363, "inventory_quantity": 9267.0}]','2026-05-22 19:18:00',1247,'2026-05-22 23:20:48',12),
(114,'AJU/2026/0114','rejected',1247,12,'cantidad dusplicado por sistema entrada de contenedor.','error dedo','2026-05-22 19:19:26','2026-05-22 23:03:15','[{"product": "[ALAM-7049-12] Cable de Acero (8x19s-CSC 10mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 7470.0, "qty_counted": 0.0, "diff": -7470.0, "lot": ""}]','[{"id": 209428, "inventory_quantity": 0.0}]','2026-05-22 19:19:26',1247,'2026-05-22 23:03:15',12),
(115,'AJU/2026/0115','approved',1247,12,'ajuste a cero',NULL,'2026-05-22 22:26:15','2026-05-22 22:26:31','[{"product": "[01-CAJ-INSP-SER-0208] Caja De Inspecci\u00f3n Serial 02-08 Salidas", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 208445, "inventory_quantity": 0.0}]','2026-05-22 22:26:15',1247,'2026-05-22 22:26:30',12),
(116,'AJU/2026/0116','approved',1247,12,'ajuste',NULL,'2026-05-22 23:05:39','2026-05-22 23:05:53','[{"product": "[ALAM-7049-12] Cable de Acero (8x19s-CSC 10mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 5470.0, "qty_counted": 3470.0, "diff": -2000.0, "lot": ""}]','[{"id": 209428, "inventory_quantity": 3470.0}]','2026-05-22 23:05:39',1247,'2026-05-22 23:05:52',12),
(117,'AJU/2026/0117','approved',1247,12,'ajuste',NULL,'2026-05-22 23:08:26','2026-05-22 23:21:45','[{"product": "[ALAM-7049-5] Cable de Acero (Traccion 13 mm 9x19S Nucleo acero)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 10043.0, "qty_counted": 5043.0, "diff": -5000.0, "lot": ""}]','[{"id": 198383, "inventory_quantity": 5043.0}]','2026-05-22 23:08:26',1247,'2026-05-22 23:21:45',12),
(118,'AJU/2026/0118','approved',1247,12,'ajuste positivo',NULL,'2026-05-22 23:52:08','2026-05-22 23:57:15','[{"product": "[04-MTGEA-1000-10.4Kw-1.6m/s] M\u00e1quina Tracci\u00f3n Gearless  1000 Kg 1.6 m/s 10.4 Kw ALMK200 2:1", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 3.0, "diff": 2.0, "lot": "975684"}]','[{"id": 201548, "inventory_quantity": 3.0}]','2026-05-22 23:52:08',1247,'2026-05-22 23:57:15',12),
(119,'AJU/2026/0119','approved',1247,12,'ajuste',NULL,'2026-05-22 23:55:40','2026-05-22 23:56:18','[{"product": "[ALAM-6097-1] Polea de Desvio de Nylon con Flecha (Nylamid 9Gx6.5x240 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 4.0, "qty_counted": 13.0, "diff": 9.0, "lot": ""}]','[{"id": 209508, "inventory_quantity": 13.0}]','2026-05-22 23:55:40',1247,'2026-05-22 23:56:17',12),
(120,'AJU/2026/0120','approved',1247,12,'Me ayudas con ajuste de 2 piezas para validar el OUT30156',NULL,'2026-05-25 22:30:02','2026-05-27 18:19:04','[{"product": "[02-ANC-BCR-0010] Anclas 10 mm Cable 9-11 con resorte (Plateada)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209722, "inventory_quantity": 2.0}]','2026-05-25 22:30:02',1247,'2026-05-27 18:19:04',12),
(121,'AJU/2026/0121','approved',1247,12,'Me ayudas con ajuste de 2 piezas para validar el OUT30156',NULL,'2026-05-25 22:30:29','2026-05-27 18:18:54','[{"product": "[ALAM-6011] Anclas 10 mm Cable 9-11 con goma (Plateada)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 2.0, "diff": 1.0, "lot": ""}]','[{"id": 202101, "inventory_quantity": 2.0}]','2026-05-25 22:30:29',1247,'2026-05-27 18:18:53',12),
(122,'AJU/2026/0122','approved',1247,12,'ajuste inve',NULL,'2026-05-26 20:49:03','2026-05-28 22:40:28','[{"product": "[ALAM-6097-1] Polea de Desvio de Nylon con Flecha (Nylamid 9Gx6.5x240 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 13.0, "qty_counted": 0.0, "diff": -13.0, "lot": ""}]','[{"id": 209508, "inventory_quantity": 0.0}]','2026-05-26 20:49:03',1247,'2026-05-28 22:40:27',12),
(123,'AJU/2026/0123','approved',1247,12,'ajuste inv',NULL,'2026-05-26 20:51:56','2026-05-27 18:18:04','[{"product": "[ALAM-6097-2] Polea de Desvio de Nylon con Flecha (Nylamid 2Gx8x150 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 13.0, "diff": 13.0, "lot": ""}]','[{"id": 209750, "inventory_quantity": 13.0}]','2026-05-26 20:51:56',1247,'2026-05-27 18:18:04',12),
(124,'AJU/2026/0124','approved',1247,12,'ajuste al inv por tema de medida incorrecta',NULL,'2026-05-26 22:12:23','2026-05-28 22:39:42','[{"product": "[ALAM-6050-014] Piston Hidr\u00e1ulico (70X50X3950 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 18.0, "qty_counted": 23.0, "diff": 5.0, "lot": ""}]','[{"id": 206540, "inventory_quantity": 23.0}]','2026-05-26 22:12:22',1247,'2026-05-28 22:39:41',12),
(125,'AJU/2026/0125','approved',1247,12,'ajuste al inv por tema de medida incorrecta',NULL,'2026-05-26 22:12:38','2026-05-27 18:15:45','[{"product": "[ALAM-6050-017] Piston Hidr\u00e1ulico (Resd 70/50-3300)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 5.0, "qty_counted": 0.0, "diff": -5.0, "lot": ""}]','[{"id": 207698, "inventory_quantity": 0.0}]','2026-05-26 22:12:38',1247,'2026-05-27 18:15:44',12),
(126,'AJU/2026/0126','approved',1247,12,'Se debe a que hubo un IN el cual se regreso a almacen 1 por 6 pz IN4439',NULL,'2026-05-27 19:29:42','2026-05-28 22:39:35','[{"product": "[ALAM-6059-1] Set de Riel (T50 (50x50x5mm))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 228.0, "qty_counted": 234.0, "diff": 6.0, "lot": ""}]','[{"id": 198541, "inventory_quantity": 234.0}]','2026-05-27 19:29:42',1247,'2026-05-28 22:39:35',12),
(127,'AJU/2026/0127','approved',1247,12,'Material regresado de Lab, se ingresa a almacen',NULL,'2026-05-27 22:40:20','2026-05-28 22:39:29','[{"product": "[ALAM-2264] Transformador TRF113 60-60 Hz - 900VA", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209769, "inventory_quantity": 2.0}]','2026-05-27 22:40:20',1247,'2026-05-28 22:39:29',12),
(128,'AJU/2026/0128','approved',1247,12,'ajuste por ingreso duplicado incorrecto',NULL,'2026-05-28 20:30:55','2026-05-28 22:39:18','[{"product": "[ALAM-7049-12] Cable de Acero (8x19s-CSC 10mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 2217.0, "qty_counted": 217.0, "diff": -2000.0, "lot": ""}]','[{"id": 209428, "inventory_quantity": 217.0}]','2026-05-28 20:30:55',1247,'2026-05-28 22:39:17',12),
(129,'AJU/2026/0129','approved',1247,12,'Solicito Ajuste de 4 piz para validar OUT30185',NULL,'2026-05-29 18:30:31','2026-06-01 23:59:46','[{"product": "[ALAM-2032-1] Base para Zapata traccion (9 mm 1350 kg)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 8.0, "qty_counted": 12.0, "diff": 4.0, "lot": ""}]','[{"id": 208405, "inventory_quantity": 12.0}]','2026-05-29 18:30:30',1247,'2026-06-01 23:59:46',12),
(130,'AJU/2026/0130','approved',1247,12,'Ajuste de 3 piezas para validar el OUT 30224',NULL,'2026-05-30 15:19:17','2026-06-01 23:59:40','[{"product": "[ALAM-6024] Inserto Duro de Zapatas Para Rieles T89 y T90 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 9/ALM-3 9-B1", "qty_system": 5.0, "qty_counted": 8.0, "diff": 3.0, "lot": ""}]','[{"id": 206323, "inventory_quantity": 8.0}]','2026-05-30 15:19:17',1247,'2026-06-01 23:59:39',12),
(131,'AJU/2026/0131','approved',1247,12,'Puerta se armo de Merma para Validar OUT29560',NULL,'2026-05-30 16:33:59','2026-06-01 23:59:34','[{"product": "[CL70 21 H2 INOX] Puerta de Cabina H Autom\u00e1tico Inoxidable (700 x 2100 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209838, "inventory_quantity": 1.0}]','2026-05-30 16:33:59',1247,'2026-06-01 23:59:33',12),
(132,'AJU/2026/0132','approved',1247,12,'AJUSTE out297257 29726',NULL,'2026-06-01 23:59:24','2026-06-02 00:00:15','[{"product": "[ALAM-1042] Caja de inspecci\u00f3n para Control Alamex Inteligente y 02 S (Tarjeta PWL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209947, "inventory_quantity": 2.0}]','2026-06-01 23:59:24',1247,'2026-06-02 00:00:14',12),
(133,'AJU/2026/0133','approved',1247,12,'para validar OUT30253',NULL,'2026-06-02 17:52:02','2026-06-02 18:57:21','[{"product": "[ALAM-6068] Paraca\u00eddas Hidr\u00e1ulico 6500 Kg M\u00e1x", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209961, "inventory_quantity": 1.0}]','2026-06-02 17:52:02',1247,'2026-06-02 18:57:20',12),
(134,'AJU/2026/0134','approved',1247,12,'ajuste',NULL,'2026-06-02 18:48:09','2026-06-02 18:56:50','[{"product": "[ALAM-10022-2] Puerta de Piso S Autom\u00e1tico Panoramico 2 Panel (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209962, "inventory_quantity": 2.0}]','2026-06-02 18:48:09',1247,'2026-06-02 18:56:49',12),
(135,'AJU/2026/0135','approved',1247,12,'ajuste',NULL,'2026-06-02 18:48:37','2026-06-02 18:56:42','[{"product": "[ALAM-10022-1] Puerta de Piso S Autom\u00e1tico Panoramico 2 Panel (Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 209963, "inventory_quantity": 1.0}]','2026-06-02 18:48:37',1247,'2026-06-02 18:56:41',12),
(136,'AJU/2026/0136','approved',1247,12,'ajuste',NULL,'2026-06-02 18:49:04','2026-06-02 18:56:23','[{"product": "[ALAM-10021-2] Puerta de Cabina S Autom\u00e1tico Panoramico 2 Panel (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 209964, "inventory_quantity": 2.0}]','2026-06-02 18:49:04',1247,'2026-06-02 18:56:18',12),
(137,'AJU/2026/0137','approved',1247,12,'ajuste inv',NULL,'2026-06-02 19:02:36','2026-06-04 23:59:21','[{"product": "[ALAM-6024] Inserto Duro de Zapatas Para Rieles T89 y T90 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 14.0, "diff": 13.0, "lot": ""}]','[{"id": 209942, "inventory_quantity": 14.0}]','2026-06-02 19:02:36',1247,'2026-06-04 23:59:21',12),
(138,'AJU/2026/0138','approved',1247,12,'ajuste inventario',NULL,'2026-06-03 22:16:03','2026-06-04 23:59:00','[{"product": "[ALAM-7049-5] Cable de Acero (Traccion 13 mm 9x19S Nucleo acero)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 4000.0, "diff": 4000.0, "lot": ""}]','[{"id": 210007, "inventory_quantity": 4000.0}]','2026-06-03 22:16:03',1247,'2026-06-04 23:58:59',12),
(139,'AJU/2026/0139','rejected',1247,12,'ajuste OUT30278','error diego','2026-06-03 23:58:10','2026-06-04 23:58:48','[{"product": "[ALAM-7001] Cable 3 Polos Azul Cal 18", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -30.0, "qty_counted": 25.0, "diff": 55.0, "lot": ""}]','[{"id": 208402, "inventory_quantity": 25.0}]','2026-06-03 23:58:10',1247,'2026-06-04 23:58:48',12),
(140,'AJU/2026/0140','approved',1247,12,'Cable de Devolucion de Pemex Villahermosa',NULL,'2026-06-04 21:44:14','2026-06-04 23:57:49','[{"product": "[ALAM-7001] Cable 3 Polos Azul Cal 18", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -30.0, "qty_counted": 650.0, "diff": 680.0, "lot": ""}]','[{"id": 208402, "inventory_quantity": 650.0}]','2026-06-04 21:44:14',1247,'2026-06-04 23:57:48',12),
(141,'AJU/2026/0141','approved',1247,12,'ajuste',NULL,'2026-06-04 23:53:33','2026-06-04 23:57:21','[{"product": "[ALAM-1042] Caja de inspecci\u00f3n para Control Alamex Inteligente y 02 S (Tarjeta PWL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 209947, "inventory_quantity": 0.0}]','2026-06-04 23:53:33',1247,'2026-06-04 23:57:20',12),
(142,'AJU/2026/0142','approved',1247,12,'me ayudas con ingreso de 1 pz para validar out30307',NULL,'2026-06-05 17:47:48','2026-06-05 18:03:15','[{"product": "[ALAM-2027] Base de Goma para Bancada 90 x 4 mm", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3/RACK 13/ALM-3 13-C1", "qty_system": 5.0, "qty_counted": 6.0, "diff": 1.0, "lot": ""}]','[{"id": 206677, "inventory_quantity": 6.0}]','2026-06-05 17:47:48',1247,'2026-06-05 18:03:14',12),
(143,'AJU/2026/0143','rejected',1247,12,'Existenciapara validar el OUT28238','cambio SKU','2026-06-08 19:44:53','2026-06-11 17:55:46','[{"product": "Plataforma Hidr\u00e1ulica 4 Postes (2, N/A, Pintado, L\u00e1mina Antiderrapante, 2, 2 (180 Degrees), 380 V, Heavy Duty Button Panel with Stop, 200 mm. - 800 mm., 1550-1649 mm, 1550-1599 mm, Fondo, 2, 3,000 Kg.)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210099, "inventory_quantity": 1.0}]','2026-06-08 19:44:53',1247,'2026-06-11 17:55:46',12),
(144,'AJU/2026/0144','rejected',1247,12,'Existencia validada en el OUT28238','error sku','2026-06-08 19:46:26','2026-06-11 17:58:19','[{"product": "Plataforma Hidr\u00e1ulica 4 Postes (N/A, N/A, Acero Inoxidable Mate, L\u00e1mina Antiderrapante, 2, 1, 220 V. 3F, Thin Film-Transistor (FTF), No Pit, 1550-1649 mm, 1550-1599 mm, Izquierda, 1, 4,000 Kg.)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208973, "inventory_quantity": 0.0}]','2026-06-08 19:46:26',1247,'2026-06-11 17:58:19',12),
(145,'AJU/2026/0145','approved',1247,12,'para validar el OUT30359',NULL,'2026-06-09 22:49:23','2026-06-11 17:58:44','[{"product": "[ALAM-1189] Relevador con Base 14 Pins 24 V", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210136, "inventory_quantity": 1.0}]','2026-06-09 22:49:23',1247,'2026-06-11 17:58:44',12),
(146,'AJU/2026/0146','rejected',1247,12,'para validar OUT30352','quedo con transferencia','2026-06-09 22:56:25','2026-06-11 18:21:19','[{"product": "[ALAM-2223-2] Puntero para Cable de Avi\u00f3n (MACHO)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": -1.0, "qty_counted": 2.0, "diff": 3.0, "lot": ""}]','[{"id": 205748, "inventory_quantity": 2.0}]','2026-06-09 22:56:25',1247,'2026-06-11 18:21:19',12),
(147,'AJU/2026/0147','approved',1247,12,'para validar el OUT30348',NULL,'2026-06-09 23:16:54','2026-06-11 18:20:54','[{"product": "[ALAM-2190-1] Cam de Operador Grande (Pinza Dorada) (Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210138, "inventory_quantity": 1.0}]','2026-06-09 23:16:54',1247,'2026-06-11 18:20:53',12),
(148,'AJU/2026/0148','approved',1247,12,'realizar transfrerencia a GDL',NULL,'2026-06-10 20:10:46','2026-06-11 18:21:28','[{"product": "[ALAM-1042] Caja de inspecci\u00f3n para Control Alamex Inteligente y 02 S (Tarjeta PWL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210166, "inventory_quantity": 1.0}]','2026-06-10 20:10:46',1247,'2026-06-11 18:21:28',12),
(149,'AJU/2026/0149','approved',1247,12,'para realizar Transfe a GDL',NULL,'2026-06-10 20:17:31','2026-06-11 18:28:10','[{"product": "[01-COP-CCAI-0PB-03] COP Inteligente & Alam 02S (Azul, PB-3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210167, "inventory_quantity": 1.0}]','2026-06-10 20:17:31',1247,'2026-06-11 18:28:10',12),
(150,'AJU/2026/0150','approved',1247,12,'para validar el OUT 29592',NULL,'2026-06-11 14:51:30','2026-06-11 18:37:51','[{"product": "[01-TAR-LOP-INT-D7S-S/E] Tarjeta Interior LOP con Display 7 Seg. Sis. Enchufe Avox", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 210178, "inventory_quantity": 2.0}]','2026-06-11 14:51:30',1247,'2026-06-11 18:37:50',12),
(151,'AJU/2026/0151','approved',1247,12,'Para Validar el OUT30391 de SEINCO este variador se tomo de un control que desinstalo LAB de Rodher.',NULL,'2026-06-12 15:58:51','2026-06-15 23:46:46','[{"product": "[ALAM-1003-6] Variador Inteligente Alam (220V/7.5 Kw / 32 A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210224, "inventory_quantity": 1.0}]','2026-06-12 15:58:51',1247,'2026-06-15 23:46:45',12),
(152,'AJU/2026/0152','approved',1247,12,'Los roller no estan el sistema por que los habían regresado como merma, se les mostró a operaciones y ellos lo solicitaron',NULL,'2026-06-13 18:34:47','2026-06-15 23:46:01','[{"product": "[ALAM-2160] Roller Para Chasis MRL o Hidr\u00e1ulico (80 mm) Exc\u00e9ntrico", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 6.0, "diff": 6.0, "lot": ""}]','[{"id": 210258, "inventory_quantity": 6.0}]','2026-06-13 18:34:47',1247,'2026-06-15 23:46:00',12),
(153,'AJU/2026/0153','approved',1247,12,'Existencias por alta de producto existente sin SKU.',NULL,'2026-06-15 18:04:03','2026-06-29 18:34:28','[{"product": "[ALAM-2266] V\u00e1lvula de Alivio para Bomba 35Lt", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 12.0, "diff": 12.0, "lot": ""}]','[{"id": 210272, "inventory_quantity": 12.0}]','2026-06-15 18:04:03',1247,'2026-06-29 18:34:28',12),
(154,'AJU/2026/0154','approved',1247,12,'valida incorrectamente en el OUT26787 no se descargo de inv debido a que el almacén *stockdoppler',NULL,'2026-06-15 18:45:18','2026-06-30 19:24:02','[{"product": "[ALAM-4001-002] Bomba Hidr\u00e1ulica (144 L-11Kw-220/380 V-60Hz)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 6.0, "qty_counted": 5.0, "diff": -1.0, "lot": ""}]','[{"id": 206204, "inventory_quantity": 5.0}]','2026-06-15 18:45:18',1247,'2026-06-30 19:24:02',12),
(155,'AJU/2026/0155','approved',1247,12,'IN4468 se reciben 4 bombas con n/s 260679.01 al 260679.04 transf INT27258 error de sistema en almacen 2 4 cuando es 1 pz',NULL,'2026-06-15 18:48:38','2026-06-17 20:10:35','[{"product": "[ALAM-4001-007] Bomba Hidr\u00e1ulica (144L 9.2 Kw 220/380V 60 Hz)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 4.0, "qty_counted": 1.0, "diff": -3.0, "lot": "260679.01"}]','[{"id": 209639, "inventory_quantity": 1.0}]','2026-06-15 18:48:38',1247,'2026-06-17 20:10:35',12),
(156,'AJU/2026/0156','approved',1247,12,'Ajuste por conteo Ciclico',NULL,'2026-06-16 15:59:15','2026-06-30 19:23:51','[{"product": "[ALAM-1155-6] LOP Botonera De Piso Cuadrados -Naranja (2 Boton + Display Binario)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 40.0, "qty_counted": 58.0, "diff": 18.0, "lot": ""}]','[{"id": 207689, "inventory_quantity": 58.0}]','2026-06-16 15:59:15',1247,'2026-06-30 19:23:51',12),
(159,'AJU/2026/0159','approved',1247,12,'ajuste por conteo de inventario',NULL,'2026-06-16 16:02:12','2026-06-30 19:23:01','[{"product": "[ALAM-1142-003] COP Botonera de Cabina Bot\u00f3n Redondo (PB-3 (Display Blanco))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 6.0, "diff": 3.0, "lot": ""}]','[{"id": 203612, "inventory_quantity": 6.0}]','2026-06-16 16:02:12',1247,'2026-06-30 19:23:01',12),
(160,'AJU/2026/0160','rejected',1247,12,'ajuste x existencia en maleta','deeb estar devolucion de merema como fue transferencia','2026-06-16 20:00:59','2026-06-17 20:08:28','[{"product": "[ALAM-1279] Tarjeta Principal ML65x", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 210324, "inventory_quantity": 2.0}]','2026-06-16 20:00:59',1247,'2026-06-17 20:08:28',12),
(161,'AJU/2026/0161','approved',1247,12,'ajuste por conteo de Inv',NULL,'2026-06-16 22:03:39','2026-06-17 20:07:50','[{"product": "[ALAM-1132-048] Bot\u00f3n Slim Cuadrado (Bajar)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 91.0, "qty_counted": 98.0, "diff": 7.0, "lot": ""}]','[{"id": 207296, "inventory_quantity": 98.0}]','2026-06-16 22:03:39',1247,'2026-06-17 20:07:50',12),
(162,'AJU/2026/0162','approved',1247,12,'ajuste por conteo en Inv',NULL,'2026-06-16 22:05:02','2026-06-17 20:07:29','[{"product": "[ALAM-1132-050] Bot\u00f3n Slim Cuadrado (Ciego)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 160.0, "qty_counted": 162.0, "diff": 2.0, "lot": ""}]','[{"id": 207299, "inventory_quantity": 162.0}]','2026-06-16 22:05:02',1247,'2026-06-17 20:07:29',12),
(163,'AJU/2026/0163','approved',1247,12,'ajuste por conteo en Inv',NULL,'2026-06-16 22:05:35','2026-06-30 19:22:52','[{"product": "[ALAM-1132-052] Bot\u00f3n Slim Cuadrado (Subir)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 559.0, "qty_counted": 554.0, "diff": -5.0, "lot": ""}]','[{"id": 207294, "inventory_quantity": 554.0}]','2026-06-16 22:05:35',1247,'2026-06-30 19:22:52',12),
(164,'AJU/2026/0164','approved',1247,12,'ajuste por conteo Inv',NULL,'2026-06-16 22:07:18','2026-06-17 20:06:29','[{"product": "[ALAM-1132-024] Bot\u00f3n Slim Cuadrado (7)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 57.0, "qty_counted": 60.0, "diff": 3.0, "lot": ""}]','[{"id": 207253, "inventory_quantity": 60.0}]','2026-06-16 22:07:18',1247,'2026-06-17 20:06:29',12),
(165,'AJU/2026/0165','approved',1247,12,'ajuste por conteo de Inve',NULL,'2026-06-16 22:07:50','2026-06-17 20:06:22','[{"product": "[ALAM-1132-023] Bot\u00f3n Slim Cuadrado (6)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 70.0, "qty_counted": 72.0, "diff": 2.0, "lot": ""}]','[{"id": 207252, "inventory_quantity": 72.0}]','2026-06-16 22:07:50',1247,'2026-06-17 20:06:22',12),
(166,'AJU/2026/0166','approved',1247,12,'Ajuste de +1 pieza por devolución de Miramintes 3004',NULL,'2026-06-16 22:36:29','2026-06-17 20:06:13','[{"product": "[TAR-ANU-ESP-MCTC] Tarjeta Anunciador ( MCTC-COB-A1 )", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 9.0, "qty_counted": 10.0, "diff": 1.0, "lot": ""}]','[{"id": 206560, "inventory_quantity": 10.0}]','2026-06-16 22:36:29',1247,'2026-06-17 20:06:13',12),
(167,'AJU/2026/0167','approved',1247,12,'ajuste por devolucion de miramoetes 3004',NULL,'2026-06-16 22:38:40','2026-06-17 20:05:51','[{"product": "[ALAM-1096] Intercomunicador Chino", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 10.0, "qty_counted": 11.0, "diff": 1.0, "lot": ""}]','[{"id": 207553, "inventory_quantity": 11.0}]','2026-06-16 22:38:40',1247,'2026-06-17 20:05:51',12),
(168,'AJU/2026/0168','approved',1247,12,'Para validar el OUT 30491 con este ajuste se caba la existencia.',NULL,'2026-06-17 19:34:59','2026-06-17 20:05:15','[{"product": "[ALAM-6024] Inserto Duro de Zapatas Para Rieles T89 y T90 (Duro)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 2.0, "qty_counted": 5.0, "diff": 3.0, "lot": ""}]','[{"id": 209942, "inventory_quantity": 5.0}]','2026-06-17 19:34:59',1247,'2026-06-17 20:05:14',12),
(170,'AJU/2026/0170','approved',1247,12,'botones retirados de una PB1 para validar el Out30451',NULL,'2026-06-18 19:09:03','2026-06-30 19:22:10','[{"product": "[ALAM-1130-023] Bot\u00f3n Redondo Blanco (S1)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 19.0, "qty_counted": 21.0, "diff": 2.0, "lot": ""}]','[{"id": 206729, "inventory_quantity": 21.0}]','2026-06-18 19:09:03',1247,'2026-06-30 19:22:09',12),
(171,'AJU/2026/0171','approved',1247,12,'botones retirados de una PB1 para validar el Out30451',NULL,'2026-06-18 19:09:34','2026-06-30 19:22:00','[{"product": "[ALAM-1130-013] Bot\u00f3n Redondo Blanco (Bajar)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 8.0, "qty_counted": 33.0, "diff": 25.0, "lot": ""}]','[{"id": 209238, "inventory_quantity": 33.0}]','2026-06-18 19:09:34',1247,'2026-06-30 19:22:00',12),
(172,'AJU/2026/0172','rejected',1247,12,'botones retirados de una PB1 para validar el Out30451','no esta correcto','2026-06-18 19:10:11','2026-08-17 19:44:38','[{"product": "[ALAM-1130-045] Bot\u00f3n Redondo Blanco (1)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 1.0, "diff": -2.0, "lot": ""}]','[{"id": 209231, "inventory_quantity": 1.0}]','2026-06-18 19:10:11',1247,'2026-08-17 19:44:38',12),
(173,'AJU/2026/0173','rejected',1247,12,'Para Validar el OUT24573','error','2026-06-22 16:36:11','2026-06-29 18:32:39','[{"product": "[akabani 2] Elevador MRL-G (Acero Inoxidable Mate, PVC, ASC (Est\u00e1ndar), 900x2100 mm, Autom\u00e1tico, Est\u00e1ndar, 800 Kg, 2:1, 1, 1 m/s, 220 V / 2F, 1 m, Matriz de Puntos, S\u00ed, No, Derecha, 0, 3100-3299 mm, 0 - 5000 mm., 850-999 mm, S\u00ed, S\u00ed, S\u00ed, S\u00ed, S\u00ed, 0-5,000 mm, 1000-1549 mm., 1000-1549 mm., Si, Matriz de Puntos, 5 Niveles, 2, 1, 1, Orbed, Acero Inoxidable Mate 304, Acero Inoxidable Mate 304, Left Side, 2, SI, Horizontal display)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210465, "inventory_quantity": 1.0}]','2026-06-22 16:36:10',1247,'2026-06-29 18:32:39',12),
(174,'AJU/2026/0174','rejected',1247,12,'Se envia chapa a Bolaños sin OUT.','error cantidad','2026-06-22 19:22:33','2026-08-17 21:19:10','[{"product": "[ALAM-2197-2] Chapa Puerta Manual Grande (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 2.0, "diff": -1.0, "lot": ""}]','[{"id": 210454, "inventory_quantity": 2.0}]','2026-06-22 19:22:33',1247,'2026-08-17 21:19:10',12),
(175,'AJU/2026/0175','approved',1247,12,'Se envia chapa a Bolaños sin OUT.',NULL,'2026-06-22 19:23:56','2026-06-29 18:32:02','[{"product": "[ALAM-2197-2] Chapa Puerta Manual Grande (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 1.0, "diff": -2.0, "lot": ""}]','[{"id": 210454, "inventory_quantity": 1.0}]','2026-06-22 19:23:55',1247,'2026-06-29 18:32:01',12),
(176,'AJU/2026/0176','approved',1247,12,'Resistencia desmontada de un control',NULL,'2026-06-23 16:20:49','2026-06-29 18:29:32','[{"product": "[ALAM-1191-013] Resistencia De Aluminio (15 Ohms - 1.5 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 2.0, "diff": 1.0, "lot": ""}]','[{"id": 208905, "inventory_quantity": 2.0}]','2026-06-23 16:20:49',1247,'2026-06-29 18:29:31',12),
(177,'AJU/2026/0177','approved',1247,12,'ajuste por cambio de tarjeta de - 1 pza de E3 a +1 pza de F3',NULL,'2026-06-26 16:58:37','2026-06-30 19:20:44','[{"product": "[ALAM-1254] Tarjeta Encoder E3 - Yaskawa", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 209532, "inventory_quantity": 0.0}]','2026-06-26 16:58:37',1247,'2026-06-30 19:20:43',12),
(178,'AJU/2026/0178','approved',1247,12,'ajuste +1',NULL,'2026-06-26 17:01:14','2026-06-29 18:13:16','[{"product": "[ALAM-1255] Tarjeta Encoder F3 - Yaskawa", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 4.0, "diff": 1.0, "lot": ""}]','[{"id": 197222, "inventory_quantity": 4.0}]','2026-06-26 17:01:14',1247,'2026-06-29 18:13:15',12),
(180,'AJU/2026/0180','approved',1247,12,'por conteo de inventario',NULL,'2026-07-02 18:39:07','2026-07-08 21:39:52','[{"product": "[ALAM-14017] Taquete de Arp\u00f3n  11.9 mm (15/32)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 99.0, "qty_counted": 931.0, "diff": 832.0, "lot": ""}]','[{"id": 186352, "inventory_quantity": 931.0}]','2026-07-02 18:39:07',1247,'2026-07-08 21:39:51',12),
(181,'AJU/2026/0181','approved',1247,12,'Me ayudas con ajuste para validar el OUT 30640 de envio de GDL, la bonina se retiro de una maquina',NULL,'2026-07-02 19:50:44','2026-07-08 21:39:33','[{"product": "[ALAM-2045] Bobina de Freno 110 V-MP/SID 6,8K 95 Ohms  ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210835, "inventory_quantity": 1.0}]','2026-07-02 19:50:44',1247,'2026-07-08 21:39:32',12),
(182,'AJU/2026/0182','approved',1247,12,'ajuste al Inv para validar el OUT30687',NULL,'2026-07-03 20:53:46','2026-07-09 22:40:53','[{"product": "[ALAM-5004-1] Motor De Operador PN Sin Engrane", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 210864, "inventory_quantity": 2.0}]','2026-07-03 20:53:46',1247,'2026-07-09 22:40:53',12),
(183,'AJU/2026/0183','approved',1247,12,'se levanto ticket para revisar por que no se puede validar ya que el pick si fue validado',NULL,'2026-07-04 16:56:13','2026-07-08 21:37:35','[{"product": "[06-CHA-HID-320] Kit Chasis Hidr\u00e1ulico 450 Kg DBG : 70 cm", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 210874, "inventory_quantity": 1.0}]','2026-07-04 16:56:13',1247,'2026-07-08 21:37:35',12),
(184,'AJU/2026/0184','approved',1247,12,'se levanto ticket para revisar por que no se puede validar ya que el pick si fue validado',NULL,'2026-07-04 16:56:57','2026-07-08 21:37:01','[{"product": "[CAB-PRO-ALAM-06] Cabinas Para Proyectos (450 Kg)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 2.0, "diff": 1.0, "lot": ""}]','[{"id": 209320, "inventory_quantity": 2.0}]','2026-07-04 16:56:57',1247,'2026-07-08 21:37:01',12),
(185,'AJU/2026/0185','approved',1247,12,'ajuste para vaidar el OUT 30643',NULL,'2026-07-04 17:00:55','2026-07-08 21:36:43','[{"product": "[ALAM-1042] Caja de inspecci\u00f3n para Control Alamex Inteligente y 02 S (Tarjeta PWL)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 210875, "inventory_quantity": 2.0}]','2026-07-04 17:00:55',1247,'2026-07-08 21:36:43',12),
(186,'AJU/2026/0186','approved',1247,12,'ajuste por conteo de Inv',NULL,'2026-07-06 18:46:23','2026-07-08 21:36:07','[{"product": "[ALAM-14015] Taquete 12.7 mm (1/2) Plateado", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": -1.0, "qty_counted": 3200.0, "diff": 3201.0, "lot": ""}]','[{"id": 206110, "inventory_quantity": 3200.0}]','2026-07-06 18:46:22',1247,'2026-07-08 21:36:07',12),
(187,'AJU/2026/0187','approved',1247,12,'Ajuste por conteo de Inv',NULL,'2026-07-08 20:55:07','2026-07-08 21:35:46','[{"product": "[ALAM-1226] Tarjeta 7 Segmentos 02 SDC11", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 19.0, "diff": 19.0, "lot": ""}]','[{"id": 210987, "inventory_quantity": 19.0}]','2026-07-08 20:55:07',1247,'2026-07-08 21:35:46',12),
(188,'AJU/2026/0188','approved',1247,12,'PARA CREACION DE PICK Y GENERAR OUT PARA SALIDA',NULL,'2026-07-09 21:08:38','2026-07-09 22:40:36','[{"product": "[ALAM-15006-015] Cabina Sedena 450 Kg", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 211074, "inventory_quantity": 1.0}]','2026-07-09 21:08:38',1247,'2026-07-09 22:40:35',12),
(190,'AJU/2026/0190','approved',27323,12,'Ajuste de cantidad en menos porque sacó de ubicación falso https://workdrive.zoho.com/folder/my5e98e24c28678394906be1fac84fab95ffd',NULL,'2026-07-17 19:00:03','2026-07-30 00:10:08','[{"product": "[ALAM-6050-001] Piston Hidr\u00e1ulico (100x5x2300 mm)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210899, "inventory_quantity": 0.0}]','2026-07-17 19:00:03',27323,'2026-07-30 00:10:07',12),
(191,'AJU/2026/0191','approved',27323,12,'Ajuste de cantidad porque antes se sacó de ubicación falso (stock doppler) en menos https://workdrive.zoho.com/folder/my5e98e24c28678394906be1fac84fab95ffd',NULL,'2026-07-17 19:10:25','2026-07-29 22:15:16','[{"product": "[ALAM-6050-001] Piston Hidr\u00e1ulico (100x5x2300 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": "260678.04"}]','[{"id": 209643, "inventory_quantity": 0.0}]','2026-07-17 19:10:25',27323,'2026-07-29 22:15:16',12),
(192,'AJU/2026/0192','approved',27323,12,'En el ultimó conteo cíclico, encontró 1  e ya transfirió a showroom, los 2 no existen por eso este ajuste

https://workdrive.zoho.com/folder/fc91v6409328f15f74f9baf31b844613d1bcb',NULL,'2026-07-17 19:15:11','2026-07-29 22:14:53','[{"product": "[ALAM-6050-011] Piston Hidr\u00e1ulico (Resd 70x50x1800 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 206550, "inventory_quantity": 0.0}]','2026-07-17 19:15:11',27323,'2026-07-29 22:14:53',12),
(193,'AJU/2026/0193','approved',27323,12,'En total son 22 en sistema y 14 fisicamente ... Hay 6 en GDL , 1 fue y su OUT no esta validado OUT/30655.
el problema queda con 1 pza que tiene el sistema extra, esta pza pienso fue un error cuando modificó una vez los 75/50-3300 y transfirió sus cantidades al producto 70X50X3950 

https://workdrive.zoho.com/folder/9xuqi6847b4894b9340ec9546135437d74b1a',NULL,'2026-07-17 19:36:40','2026-07-29 22:14:44','[{"product": "[ALAM-6050-014] Piston Hidr\u00e1ulico (70X50X3950 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 15.0, "qty_counted": 14.0, "diff": -1.0, "lot": ""}]','[{"id": 206540, "inventory_quantity": 14.0}]','2026-07-17 19:36:40',27323,'2026-07-29 22:14:43',12),
(194,'AJU/2026/0194','approved',1247,12,'ajuste por conteo',NULL,'2026-07-22 17:07:40','2026-07-29 22:14:34','[{"product": "[ALAM-2108] Escalera para Fosa ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 16.0, "diff": 16.0, "lot": ""}]','[{"id": 211463, "inventory_quantity": 16.0}]','2026-07-22 17:07:40',1247,'2026-07-29 22:14:34',12),
(195,'AJU/2026/0195','approved',1247,12,'Ajuste por conteo',NULL,'2026-07-24 16:48:31','2026-07-29 22:14:25','[{"product": "[ALAM-2162] Rondana Plana Galvanizada M12 - 1.75\"", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 8.0, "qty_counted": 500.0, "diff": 492.0, "lot": ""}]','[{"id": 206109, "inventory_quantity": 500.0}]','2026-07-24 16:48:31',1247,'2026-07-29 22:14:25',12),
(196,'AJU/2026/0196','approved',1247,12,'Ajuste por conteo',NULL,'2026-07-24 16:48:58','2026-07-29 22:11:20','[{"product": "[ALAM-2164] Rondana de Presi\u00f3n Galvanizada M12 - 1.75\"", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": -8.0, "qty_counted": 500.0, "diff": 508.0, "lot": ""}]','[{"id": 209307, "inventory_quantity": 500.0}]','2026-07-24 16:48:58',1247,'2026-07-29 22:11:20',12),
(197,'AJU/2026/0197','approved',1247,12,'Entrada por retorno del Lab se ingresa a almacen 3',NULL,'2026-07-24 17:38:49','2026-07-29 22:10:50','[{"product": "[ARElD-TFT-7\"] Display TFT De 7 \" Horizontal ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 4.0, "qty_counted": 5.0, "diff": 1.0, "lot": ""}]','[{"id": 206427, "inventory_quantity": 5.0}]','2026-07-24 17:38:49',1247,'2026-07-29 22:10:49',12),
(198,'AJU/2026/0198','approved',27323,12,'Conteo Cíclico 
Las evidencias:

https://workdrive.zoho.com/folder/pufb1a51047e24531405592aa7707a1f8d69b',NULL,'2026-07-24 22:21:14','2026-07-30 00:08:24','[{"product": "[ALAM-8016-2] Im\u00e1n Control Alam (30 cm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 338.0, "qty_counted": 299.0, "diff": -39.0, "lot": ""}]','[{"id": 207557, "inventory_quantity": 299.0}]','2026-07-24 22:21:14',27323,'2026-07-30 00:08:24',12),
(199,'AJU/2026/0199','approved',27323,12,'Conteo Cíclico, Se vio que solo hay un OUT/30655 no esta validado pero su pick validado por eso debe reservar 3 pzas en ALM1 para validar el OUT en el futuro',NULL,'2026-07-24 22:23:37','2026-07-30 00:08:02','[{"product": "[ALAM-8016-2] Im\u00e1n Control Alam (30 cm)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 12.0, "qty_counted": 3.0, "diff": -9.0, "lot": ""}]','[{"id": 208370, "inventory_quantity": 3.0}]','2026-07-24 22:23:37',27323,'2026-07-30 00:08:02',12),
(200,'AJU/2026/0200','approved',27323,12,'Conteo Cíclico

durante el conteo se encontró 7 pzas para usar en LAB pruebas

Las evdienciashttps://workdrive.zoho.com/folder/pufb1a51047e24531405592aa7707a1f8d69b',NULL,'2026-07-24 22:48:18','2026-07-30 00:07:59','[{"product": "[ALAM-8016-2] Im\u00e1n Control Alam (30 cm)", "location": "Stock Laboratorio", "qty_system": 0.0, "qty_counted": 7.0, "diff": 7.0, "lot": ""}]','[{"id": 211536, "inventory_quantity": 7.0}]','2026-07-24 22:48:17',27323,'2026-07-30 00:07:59',12),
(201,'AJU/2026/0201','approved',27323,12,'Conteo cíclico número CC000024

https://workdrive.zoho.com/folder/gx3mq2b4331f4deba409cbb3cff112c63a37e

no hay algo para poner en ALM1 depende al presente',NULL,'2026-07-27 22:30:50','2026-07-30 00:10:41','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 44.0, "qty_counted": 0.0, "diff": -44.0, "lot": ""}]','[{"id": 208548, "inventory_quantity": 0.0}]','2026-07-27 22:30:50',27323,'2026-07-30 00:10:40',12),
(202,'AJU/2026/0202','approved',27323,12,'Conteo Cíclico número CC000024

https://workdrive.zoho.com/folder/gx3mq2b4331f4deba409cbb3cff112c63a37e

para borrar los cantidades en menos',NULL,'2026-07-27 22:32:09','2026-07-29 22:09:54','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -60.0, "qty_counted": 0.0, "diff": 60.0, "lot": ""}]','[{"id": 211086, "inventory_quantity": 0.0}]','2026-07-27 22:32:09',27323,'2026-07-29 22:09:54',12),
(203,'AJU/2026/0203','approved',27323,12,'Conteo cíclico debe tener 10 pzas en ALM3 porque hay 4 por OUT/30655 (entregamos pero no podemos validar) + 6 por OUT/29356

debende el conteo cíclico número CC000024

https://workdrive.zoho.com/folder/gx3mq2b4331f4deba409cbb3cff112c63a37e',NULL,'2026-07-27 22:33:57','2026-07-29 22:08:36','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 10.0, "diff": 10.0, "lot": ""}]','[{"id": 211570, "inventory_quantity": 10.0}]','2026-07-27 22:33:57',27323,'2026-07-29 22:08:36',12),
(204,'AJU/2026/0204','approved',27323,12,'Conteo cíclico número CC000024

https://workdrive.zoho.com/folder/gx3mq2b4331f4deba409cbb3cff112c63a37e

encontró en LAB 12 pzas para pruebas y uso interno',NULL,'2026-07-27 22:37:20','2026-07-29 22:07:52','[{"product": "[ALAM-8016-3] Im\u00e1n Control Alam (Redondo)", "location": "Stock Laboratorio", "qty_system": 0.0, "qty_counted": 12.0, "diff": 12.0, "lot": ""}]','[{"id": 211572, "inventory_quantity": 12.0}]','2026-07-27 22:37:20',27323,'2026-07-29 22:07:51',12),
(205,'AJU/2026/0205','approved',27323,12,'Conteo Cíclico las evidencias: https://workdrive.zoho.com/folder/wcryv2db07e7d338e44fe880800d1c6899431',NULL,'2026-07-29 16:57:25','2026-07-29 22:07:26','[{"product": "[ALAM-8016-1] Im\u00e1n Control Alam (10 cm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 8597.0, "qty_counted": 9671.0, "diff": 1074.0, "lot": ""}]','[{"id": 207559, "inventory_quantity": 9671.0}]','2026-07-29 16:57:25',27323,'2026-07-29 22:07:26',12),
(206,'AJU/2026/0206','approved',27323,12,'Conteo Cíclico

Evidencias:
https://workdrive.zoho.com/folder/wcryv2db07e7d338e44fe880800d1c6899431',NULL,'2026-07-29 17:00:19','2026-07-29 22:06:26','[{"product": "[ALAM-8016-1] Im\u00e1n Control Alam (10 cm)", "location": "Stock Laboratorio", "qty_system": 0.0, "qty_counted": 4.0, "diff": 4.0, "lot": ""}]','[{"id": 211614, "inventory_quantity": 4.0}]','2026-07-29 17:00:19',27323,'2026-07-29 22:06:26',12),
(208,'AJU/2026/0208','approved',1247,12,'Variador el cual se regreso de Peten y se mando a Revisión a Pilar Mexicana',NULL,'2026-08-04 20:28:12','2026-09-07 20:40:10','[{"product": "[ALAM-1181-4] Variador Yaskawa L1000E (380/15hp/23A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 211749, "inventory_quantity": 1.0}]','2026-08-04 20:28:12',1247,'2026-09-07 20:40:09',12),
(211,'AJU/2026/0211','rejected',1247,12,'para validar el OUT 31141','no esta correcto','2026-08-11 18:29:54','2026-08-17 19:44:20','[{"product": "[ALAM-2017] Base Para Zapata de Tracci\u00f3n con Inserto ALAM19 (16 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 2.0, "qty_counted": 4.0, "diff": 2.0, "lot": ""}]','[{"id": 203261, "inventory_quantity": 4.0}]','2026-08-11 18:29:54',1247,'2026-08-17 19:44:20',12),
(217,'AJU/2026/0217','approved',1247,12,'para validar el OUT31304',NULL,'2026-08-14 19:45:49','2026-09-08 18:03:47','[{"product": "[ALAM-2041] Bloque de Contacto NC", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212024, "inventory_quantity": 1.0}]','2026-08-14 19:45:49',1247,'2026-09-08 18:03:47',12),
(218,'AJU/2026/0218','approved',1247,12,'las entradas de esta variador durante el año fueron de dos piezas las cuales salieron sin embargo Lab rehabilito 1 pz es por ello que necesito el ingreso de 1 mas para validar el OUT31304',NULL,'2026-08-14 19:51:17','2026-09-08 18:03:40','[{"product": "[ALAM-1003-2] Variador Inteligente Alam (220v/11kw/45A)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212026, "inventory_quantity": 1.0}]','2026-08-14 19:51:17',1247,'2026-09-08 18:03:40',12),
(219,'AJU/2026/0219','approved',27323,12,'ajuste para más cantidades, horita tenemos 6 pzas en ALM y debemos tener 4 pzas para validar el OUT (OUT/31141
) y su PICK que fueron al cliente para validarlos

Las evidencias: https://workdrive.zoho.com/folder/98tetef187409aafc411da09e1a783db2b8da',NULL,'2026-08-17 15:53:05','2026-08-17 19:45:19','[{"product": "[ALAM-2017] Base Para Zapata de Tracci\u00f3n con Inserto ALAM19 (16 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 2.0, "qty_counted": 10.0, "diff": 8.0, "lot": ""}]','[{"id": 203261, "inventory_quantity": 10.0}]','2026-08-17 15:53:05',27323,'2026-08-17 19:45:19',12),
(220,'AJU/2026/0220','approved',27323,12,'Conteo Cíclico, se encontró 16 pzas en total en ALM3 y no hay algo pendinte para validar en sistema, por fa cancelá ajuste número 172 y valida este.

Las evidencias:
https://workdrive.zoho.com/folder/98tetf6b973d1e9344d9abbca9b9ecdbf91bd',NULL,'2026-08-17 17:52:34','2026-08-17 19:45:32','[{"product": "[ALAM-1130-045] Bot\u00f3n Redondo Blanco (1)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 19.0, "qty_counted": 16.0, "diff": -3.0, "lot": ""}]','[{"id": 209231, "inventory_quantity": 16.0}]','2026-08-17 17:52:34',27323,'2026-08-17 19:45:32',12),
(221,'AJU/2026/0221','approved',27323,12,'Conteo Cíclico hay 2 pzas en ALM3 en lugar de 3 por eso el ajuste menos 1

Las evidencias:
https://workdrive.zoho.com/folder/98tet1c782e36d4cf44c78f4b6a9a0e8d409a',NULL,'2026-08-17 19:49:23','2026-08-17 21:19:31','[{"product": "[ALAM-2197-1] Chapa Puerta Manual Grande (Derecha)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 2.0, "diff": -1.0, "lot": ""}]','[{"id": 205987, "inventory_quantity": 2.0}]','2026-08-17 19:49:23',27323,'2026-08-17 21:19:31',12),
(222,'AJU/2026/0222','approved',27323,12,'Conteo Cíclico',NULL,'2026-08-24 21:26:52','2026-08-24 23:15:54','[{"product": "[ALAM-1191-009] Resistencia De Aluminio (10 Ohms - 3.5 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212206, "inventory_quantity": 1.0}]','2026-08-24 21:26:52',27323,'2026-08-24 23:15:54',12),
(223,'AJU/2026/0223','approved',27323,12,'Corregir las cantidades en menos',NULL,'2026-08-24 21:30:05','2026-08-24 23:16:15','[{"product": "[ALAM-1191-012] Resistencia De Aluminio (12.6 Ohms - 3 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -2.0, "qty_counted": 0.0, "diff": 2.0, "lot": ""}]','[{"id": 208491, "inventory_quantity": 0.0}]','2026-08-24 21:30:05',27323,'2026-08-24 23:16:15',12),
(224,'AJU/2026/0224','approved',27323,12,'porque hay cantidades en menos y pedimos ajuste AJU/2026/0223 horita quitamos los 2 de aqui y todo bien',NULL,'2026-08-24 21:32:53','2026-08-24 23:18:39','[{"product": "[ALAM-1191-012] Resistencia De Aluminio (12.6 Ohms - 3 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 8.0, "qty_counted": 6.0, "diff": -2.0, "lot": ""}]','[{"id": 207914, "inventory_quantity": 6.0}]','2026-08-24 21:32:52',27323,'2026-08-24 23:18:39',12),
(225,'AJU/2026/0225','approved',27323,12,'Conteo Cíclico',NULL,'2026-08-24 22:23:34','2026-08-24 23:16:37','[{"product": "[ALAM-1191-018] Resistencia De Aluminio (19 Ohms - 3 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 54.0, "qty_counted": 55.0, "diff": 1.0, "lot": ""}]','[{"id": 207900, "inventory_quantity": 55.0}]','2026-08-24 22:23:34',27323,'2026-08-24 23:16:37',12),
(226,'AJU/2026/0226','approved',27323,12,'Conteo Cíclico',NULL,'2026-08-24 22:43:54','2026-08-24 23:18:22','[{"product": "[ALAM-1191-026] Resistencia De Aluminio (50 Ohms - 1.5 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 61.0, "qty_counted": 64.0, "diff": 3.0, "lot": ""}]','[{"id": 208895, "inventory_quantity": 64.0}]','2026-08-24 22:43:54',27323,'2026-08-24 23:18:22',12),
(227,'AJU/2026/0227','approved',27323,12,'este producto estaba archivado y repetido',NULL,'2026-08-24 22:50:15','2026-08-24 23:17:00','[{"product": "[ALAM-1191-001] Resistencia De Aluminio", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 211363, "inventory_quantity": 0.0}]','2026-08-24 22:50:15',27323,'2026-08-24 23:17:00',12),
(228,'AJU/2026/0228','approved',27323,12,'este producto estaba archivado y repetido  sus cantidades van agregar al otro mismo producto con diferente SKU',NULL,'2026-08-24 22:52:00','2026-08-24 23:17:37','[{"product": "[ALAM-1191-001] Resistencia De Aluminio", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 65.0, "qty_counted": 0.0, "diff": -65.0, "lot": ""}]','[{"id": 194255, "inventory_quantity": 0.0}]','2026-08-24 22:52:00',27323,'2026-08-24 23:17:37',12),
(229,'AJU/2026/0229','approved',27323,12,'más cantidades del otro SKU que estaba archivado',NULL,'2026-08-24 22:52:53','2026-08-24 23:17:26','[{"product": "[ALAM-1191-021] Resistencia De Aluminio (32 Ohms - 3 KW)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 67.0, "qty_counted": 134.0, "diff": 67.0, "lot": ""}]','[{"id": 208898, "inventory_quantity": 134.0}]','2026-08-24 22:52:53',27323,'2026-08-24 23:17:26',12),
(230,'AJU/2026/0230','approved',27323,12,'Conteo Cíclico

Las evidencias:

https://workdrive.zoho.com/folder/rjdzm6ec9eca784a041c8b6f420a685fca31b',NULL,'2026-08-25 16:07:20','2026-08-25 17:14:12','[{"product": "[ALAM-5003-2] Motor con Engrane de Operador H (Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 49.0, "qty_counted": 46.0, "diff": -3.0, "lot": ""}]','[{"id": 205950, "inventory_quantity": 46.0}]','2026-08-25 16:07:20',27323,'2026-08-25 17:14:12',12),
(231,'AJU/2026/0231','approved',27323,12,'Conteo cíclico voy cambiar su ubicación y considerar en ALM3',NULL,'2026-08-25 16:39:00','2026-08-25 17:13:54','[{"product": "[ALAM-6005] Amortiguador ALAM 01", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 209263, "inventory_quantity": 0.0}]','2026-08-25 16:39:00',27323,'2026-08-25 17:13:54',12),
(232,'AJU/2026/0232','approved',27323,12,'Conteo Cíclico encontró 1 pza más la otra pza porque cancelar de ALM2 y considerar aquí con ALM3

Las evidencias: https://workdrive.zoho.com/folder/rjdzmbeddea39c7634953bcefc7e6dafb7933',NULL,'2026-08-25 16:41:08','2026-08-25 17:13:35','[{"product": "[ALAM-6005] Amortiguador ALAM 01", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 200.0, "qty_counted": 202.0, "diff": 2.0, "lot": ""}]','[{"id": 211003, "inventory_quantity": 202.0}]','2026-08-25 16:41:08',27323,'2026-08-25 17:13:35',12),
(233,'AJU/2026/0233','approved',27323,12,'Quieremos separar las cantidades a dos productos ALAM01 y ALAM03 poreso este debe ser 0',NULL,'2026-08-25 17:39:14','2026-08-25 20:31:42','[{"product": "[ALAM-6005] Amortiguador ALAM de Foso", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 202.0, "qty_counted": 0.0, "diff": -202.0, "lot": ""}]','[{"id": 211003, "inventory_quantity": 0.0}]','2026-08-25 17:39:14',27323,'2026-08-25 20:31:42',12),
(234,'AJU/2026/0234','approved',27323,12,'Se creó nuevo variante para separar 2 prdouctos

Las evidencias: https://workdrive.zoho.com/folder/rjdzma7e0192b567c4f438392c37d3af63f48',NULL,'2026-08-25 17:49:40','2026-08-25 20:31:17','[{"product": "[ALAM-6005-02] Amortiguador ALAM de Foso (ALAM-03)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 152.0, "diff": 152.0, "lot": ""}]','[{"id": 212229, "inventory_quantity": 152.0}]','2026-08-25 17:49:40',27323,'2026-08-25 20:31:17',12),
(235,'AJU/2026/0235','approved',27323,12,'Se creó nuevo variante para separar los 2 productos 
Las evidencias https://workdrive.zoho.com/folder/rjdzm44689eb8e1ea4a58a8e961731c3a1a47',NULL,'2026-08-25 17:51:15','2026-08-25 20:31:01','[{"product": "[ALAM-6005-01] Amortiguador ALAM de Foso (ALAM-01)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 50.0, "diff": 50.0, "lot": ""}]','[{"id": 212230, "inventory_quantity": 50.0}]','2026-08-25 17:51:15',27323,'2026-08-25 20:31:01',12),
(236,'AJU/2026/0236','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/7clk2e330d0c7de8c4242847269b6056eb7dc',NULL,'2026-08-26 19:33:21','2026-08-26 21:46:31','[{"product": "[ALAM-2236-2] Zapata Hidr\u00e1ulica Con Inserto Flexible (16 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 118.0, "qty_counted": 114.0, "diff": -4.0, "lot": ""}]','[{"id": 205945, "inventory_quantity": 114.0}]','2026-08-26 19:33:21',27323,'2026-08-26 21:46:31',12),
(237,'AJU/2026/0237','approved',27323,12,'Conteo Cíclico 

Las evidencias:
https://workdrive.zoho.com/folder/7clk2dd8c7ad056104f14ad11df1eda7ceb13',NULL,'2026-08-26 19:34:13','2026-08-26 21:46:12','[{"product": "[ALAM-2236-1] Zapata Hidr\u00e1ulica Con Inserto Flexible (9 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 142.0, "qty_counted": 141.0, "diff": -1.0, "lot": ""}]','[{"id": 205944, "inventory_quantity": 141.0}]','2026-08-26 19:34:13',27323,'2026-08-26 21:46:12',12),
(238,'AJU/2026/0238','approved',27323,12,'Para corregir las cantidades en menos',NULL,'2026-08-26 19:34:45','2026-08-26 21:45:48','[{"product": "[ALAM-2236-2] Zapata Hidr\u00e1ulica Con Inserto Flexible (16 mm)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210537, "inventory_quantity": 0.0}]','2026-08-26 19:34:45',27323,'2026-08-26 21:45:48',12),
(239,'AJU/2026/0239','approved',27323,12,'Contro Cíclico hay más porque hay cargadores pero otro modelo son regresos de obras o otra cosa - 163 ALM3 y 1 ALM1

Las evidencias:
https://workdrive.zoho.com/folder/7clk21402410bd17c431c81b54f48aee6ac06',NULL,'2026-08-26 21:38:00','2026-08-26 21:45:32','[{"product": "[ALAM-2072] Cargador De Cable Viajero Plano", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 157.0, "qty_counted": 163.0, "diff": 6.0, "lot": ""}]','[{"id": 209536, "inventory_quantity": 163.0}]','2026-08-26 21:38:00',27323,'2026-08-26 21:45:32',12),
(240,'AJU/2026/0240','approved',27323,12,'Corregir las cantidades en menos

Las evidencias:

https://workdrive.zoho.com/folder/weyble0b01f87abdc4abc9765b7f9325d0512',NULL,'2026-08-27 17:28:52','2026-08-27 20:51:11','[{"product": "[ALAM-1220] Switch Sobre Paso Modelo Mitsubishi", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -2.0, "qty_counted": 0.0, "diff": 2.0, "lot": ""}]','[{"id": 210579, "inventory_quantity": 0.0}]','2026-08-27 17:28:52',27323,'2026-08-27 20:51:10',12),
(241,'AJU/2026/0241','approved',27323,12,'Corregir las cantidades en menos

Las evidencias:

https://workdrive.zoho.com/folder/weyble0b01f87abdc4abc9765b7f9325d0512',NULL,'2026-08-27 17:29:04','2026-08-27 20:50:16','[{"product": "[ALAM-1220] Switch Sobre Paso Modelo Mitsubishi", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -4.0, "qty_counted": 0.0, "diff": 4.0, "lot": ""}]','[{"id": 206659, "inventory_quantity": 0.0}]','2026-08-27 17:29:04',27323,'2026-08-27 20:50:16',12),
(242,'AJU/2026/0242','approved',27323,12,'Conteo Cíclico ademas hay cantidades que sacó de otro ubicaciones en menos y corregimos aqui y allí

Las evidencias:

https://workdrive.zoho.com/folder/weyble0b01f87abdc4abc9765b7f9325d0512',NULL,'2026-08-27 17:30:17','2026-08-27 20:49:54','[{"product": "[ALAM-1220] Switch Sobre Paso Modelo Mitsubishi", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 122.0, "qty_counted": 111.0, "diff": -11.0, "lot": ""}]','[{"id": 194285, "inventory_quantity": 111.0}]','2026-08-27 17:30:17',27323,'2026-08-27 20:49:53',12),
(243,'AJU/2026/0243','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/t0rc36884467d61ed4eb3b83426b950f1d0d5',NULL,'2026-08-27 20:45:12','2026-09-02 18:35:39','[{"product": "[ALAM-1268] Tarjeta Operador De Cabina ALAM-KM10", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 74.0, "qty_counted": 71.0, "diff": -3.0, "lot": ""}]','[{"id": 208936, "inventory_quantity": 71.0}]','2026-08-27 20:45:12',27323,'2026-09-02 18:35:39',12),
(244,'AJU/2026/0244','approved',27323,12,'Para corregir su ubicaciones y va agreagar a ALM3 en lugar stock doppler

las evidencias:
https://workdrive.zoho.com/folder/t0rc36884467d61ed4eb3b83426b950f1d0d5',NULL,'2026-08-28 18:19:40','2026-09-02 18:35:46','[{"product": "[ALAM-1219] Switch Sobre Paso Llanta Grande ", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 3.0, "qty_counted": 0.0, "diff": -3.0, "lot": ""}]','[{"id": 210583, "inventory_quantity": 0.0}]','2026-08-28 18:19:40',27323,'2026-09-02 18:35:45',12),
(245,'AJU/2026/0245','approved',27323,12,'Conteo Cíclico

Las evdencias:
https://workdrive.zoho.com/folder/ikyn8b5b003a6e6e342869a8c8d883c74b5ee',NULL,'2026-08-28 18:20:18','2026-09-02 18:35:54','[{"product": "[ALAM-1219] Switch Sobre Paso Llanta Grande ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 121.0, "qty_counted": 122.0, "diff": 1.0, "lot": ""}]','[{"id": 205951, "inventory_quantity": 122.0}]','2026-08-28 18:20:18',27323,'2026-09-02 18:35:54',12),
(246,'AJU/2026/0246','approved',27323,12,'Estaba en merma, armó para entregar con el NWH/OUT/31479
quitó los postes de NWH/INT/27817',NULL,'2026-08-28 19:30:16','2026-09-02 18:36:06','[{"product": "[LL80 21 H2 INOX] Puerta de Piso H Autom\u00e1tico Inoxidable (800 x 2100 mm, Izquierda)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212300, "inventory_quantity": 1.0}]','2026-08-28 19:30:16',27323,'2026-09-02 18:36:05',12),
(247,'AJU/2026/0247','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:19:53','2026-09-02 18:36:12','[{"product": "[ALAM-1138-005] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 0)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 138.0, "qty_counted": 137.0, "diff": -1.0, "lot": ""}]','[{"id": 202536, "inventory_quantity": 137.0}]','2026-08-31 21:19:53',27323,'2026-09-02 18:36:11',12),
(248,'AJU/2026/0248','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:21:04','2026-09-02 18:36:17','[{"product": "[ALAM-1138-006] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 1)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208154, "inventory_quantity": 0.0}]','2026-08-31 21:21:04',27323,'2026-09-02 18:36:17',12),
(249,'AJU/2026/0249','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:21:16','2026-09-02 18:36:25','[{"product": "[ALAM-1138-006] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 1)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208113, "inventory_quantity": 0.0}]','2026-08-31 21:21:15',27323,'2026-09-02 18:36:25',12),
(250,'AJU/2026/0250','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:22:17','2026-09-02 18:36:30','[{"product": "[ALAM-1138-007] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 2)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208155, "inventory_quantity": 0.0}]','2026-08-31 21:22:17',27323,'2026-09-02 18:36:29',12),
(251,'AJU/2026/0251','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:23:26','2026-09-02 18:36:50','[{"product": "[ALAM-1138-007] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 2)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208155, "inventory_quantity": 0.0}]','2026-08-31 21:23:26',27323,'2026-09-02 18:36:49',12),
(252,'AJU/2026/0252','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:26:19','2026-09-02 18:36:54','[{"product": "[ALAM-1138-008] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 29.0, "qty_counted": 27.0, "diff": -2.0, "lot": ""}]','[{"id": 202539, "inventory_quantity": 27.0}]','2026-08-31 21:26:19',27323,'2026-09-02 18:36:53',12),
(253,'AJU/2026/0253','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:26:40','2026-09-02 18:37:01','[{"product": "[ALAM-1138-008] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 3)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208115, "inventory_quantity": 0.0}]','2026-08-31 21:26:40',27323,'2026-09-02 18:37:01',12),
(254,'AJU/2026/0254','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:29:33','2026-09-02 18:37:09','[{"product": "[ALAM-1138-009] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 23.0, "qty_counted": 25.0, "diff": 2.0, "lot": ""}]','[{"id": 202540, "inventory_quantity": 25.0}]','2026-08-31 21:29:33',27323,'2026-09-02 18:37:08',12),
(255,'AJU/2026/0255','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:29:52','2026-09-02 18:37:14','[{"product": "[ALAM-1138-009] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 4)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208116, "inventory_quantity": 0.0}]','2026-08-31 21:29:52',27323,'2026-09-02 18:37:13',12),
(256,'AJU/2026/0256','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:30:56','2026-09-02 18:37:24','[{"product": "[ALAM-1138-009] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 4)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208157, "inventory_quantity": 0.0}]','2026-08-31 21:30:56',27323,'2026-09-02 18:37:24',12),
(257,'AJU/2026/0257','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:32:20','2026-09-02 18:40:02','[{"product": "[ALAM-1138-011] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 6)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 28.0, "qty_counted": 31.0, "diff": 3.0, "lot": ""}]','[{"id": 202542, "inventory_quantity": 31.0}]','2026-08-31 21:32:20',27323,'2026-09-02 18:40:02',12),
(258,'AJU/2026/0258','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:32:50','2026-09-02 18:40:10','[{"product": "[ALAM-1138-011] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 6)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208118, "inventory_quantity": 0.0}]','2026-08-31 21:32:50',27323,'2026-09-02 18:40:09',12),
(259,'AJU/2026/0259','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:33:01','2026-09-02 18:40:18','[{"product": "[ALAM-1138-011] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 6)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208158, "inventory_quantity": 0.0}]','2026-08-31 21:33:01',27323,'2026-09-02 18:40:17',12),
(260,'AJU/2026/0260','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:34:15','2026-09-02 18:40:24','[{"product": "[ALAM-1138-012] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 7)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 18.0, "qty_counted": 21.0, "diff": 3.0, "lot": ""}]','[{"id": 202543, "inventory_quantity": 21.0}]','2026-08-31 21:34:15',27323,'2026-09-02 18:40:24',12),
(261,'AJU/2026/0261','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:35:10','2026-09-02 18:40:31','[{"product": "[ALAM-1138-012] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 7)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208119, "inventory_quantity": 0.0}]','2026-08-31 21:35:10',27323,'2026-09-02 18:40:31',12),
(262,'AJU/2026/0262','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:35:18','2026-09-02 18:40:37','[{"product": "[ALAM-1138-012] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 7)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208159, "inventory_quantity": 0.0}]','2026-08-31 21:35:18',27323,'2026-09-02 18:40:37',12),
(263,'AJU/2026/0263','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:36:04','2026-09-02 18:40:43','[{"product": "[ALAM-1138-013] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 8)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 61.0, "qty_counted": 42.0, "diff": -19.0, "lot": ""}]','[{"id": 207869, "inventory_quantity": 42.0}]','2026-08-31 21:36:04',27323,'2026-09-02 18:40:43',12),
(264,'AJU/2026/0264','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:36:46','2026-09-02 18:40:50','[{"product": "[ALAM-1138-013] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 8)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208120, "inventory_quantity": 0.0}]','2026-08-31 21:36:45',27323,'2026-09-02 18:40:50',12),
(265,'AJU/2026/0265','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:36:54','2026-09-02 18:40:57','[{"product": "[ALAM-1138-013] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 8)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208160, "inventory_quantity": 0.0}]','2026-08-31 21:36:54',27323,'2026-09-02 18:40:56',12),
(266,'AJU/2026/0266','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:37:54','2026-09-02 18:41:03','[{"product": "[ALAM-1138-014] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 9)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 73.0, "qty_counted": 75.0, "diff": 2.0, "lot": ""}]','[{"id": 207141, "inventory_quantity": 75.0}]','2026-08-31 21:37:54',27323,'2026-09-02 18:41:03',12),
(267,'AJU/2026/0267','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:38:27','2026-09-02 18:41:08','[{"product": "[ALAM-1138-014] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 9)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208121, "inventory_quantity": 0.0}]','2026-08-31 21:38:27',27323,'2026-09-02 18:41:08',12),
(268,'AJU/2026/0268','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:38:33','2026-09-02 18:41:14','[{"product": "[ALAM-1138-014] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 9)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208161, "inventory_quantity": 0.0}]','2026-08-31 21:38:33',27323,'2026-09-02 18:41:14',12),
(269,'AJU/2026/0269','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:48:20','2026-09-02 18:41:21','[{"product": "[ALAM-1138-019] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, S)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 90.0, "qty_counted": 70.0, "diff": -20.0, "lot": ""}]','[{"id": 202578, "inventory_quantity": 70.0}]','2026-08-31 21:48:20',27323,'2026-09-02 18:41:21',12),
(270,'AJU/2026/0270','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:49:18','2026-09-02 18:41:27','[{"product": "[ALAM-1138-020] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 10)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 97.0, "qty_counted": 99.0, "diff": 2.0, "lot": ""}]','[{"id": 207140, "inventory_quantity": 99.0}]','2026-08-31 21:49:17',27323,'2026-09-02 18:41:26',12),
(271,'AJU/2026/0271','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:49:38','2026-09-02 18:41:32','[{"product": "[ALAM-1138-020] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 10)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208122, "inventory_quantity": 0.0}]','2026-08-31 21:49:38',27323,'2026-09-02 18:41:31',12),
(272,'AJU/2026/0272','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:49:47','2026-09-02 18:41:49','[{"product": "[ALAM-1138-020] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 10)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208162, "inventory_quantity": 0.0}]','2026-08-31 21:49:47',27323,'2026-09-02 18:41:49',12),
(273,'AJU/2026/0273','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:51:54','2026-09-02 18:42:08','[{"product": "[ALAM-1138-021] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 11)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 108.0, "qty_counted": 110.0, "diff": 2.0, "lot": ""}]','[{"id": 207139, "inventory_quantity": 110.0}]','2026-08-31 21:51:54',27323,'2026-09-02 18:42:08',12),
(274,'AJU/2026/0274','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:52:10','2026-09-02 18:42:14','[{"product": "[ALAM-1138-021] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 11)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208129, "inventory_quantity": 0.0}]','2026-08-31 21:52:09',27323,'2026-09-02 18:42:14',12),
(275,'AJU/2026/0275','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:52:19','2026-09-02 18:42:19','[{"product": "[ALAM-1138-021] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 11)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208169, "inventory_quantity": 0.0}]','2026-08-31 21:52:19',27323,'2026-09-02 18:42:19',12),
(276,'AJU/2026/0276','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:53:08','2026-09-02 18:42:28','[{"product": "[ALAM-1138-022] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 12)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 89.0, "qty_counted": 91.0, "diff": 2.0, "lot": ""}]','[{"id": 207138, "inventory_quantity": 91.0}]','2026-08-31 21:53:08',27323,'2026-09-02 18:42:28',12),
(277,'AJU/2026/0277','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:53:17','2026-09-02 18:41:37','[{"product": "[ALAM-1138-022] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 12)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208123, "inventory_quantity": 0.0}]','2026-08-31 21:53:17',27323,'2026-09-02 18:41:37',12),
(278,'AJU/2026/0278','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:53:26','2026-09-02 18:42:34','[{"product": "[ALAM-1138-022] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 12)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208163, "inventory_quantity": 0.0}]','2026-08-31 21:53:26',27323,'2026-09-02 18:42:33',12),
(279,'AJU/2026/0279','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:55:16','2026-09-02 18:42:40','[{"product": "[ALAM-1138-024] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 14)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 35.0, "qty_counted": 37.0, "diff": 2.0, "lot": ""}]','[{"id": 207136, "inventory_quantity": 37.0}]','2026-08-31 21:55:16',27323,'2026-09-02 18:42:39',12),
(280,'AJU/2026/0280','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:55:22','2026-09-02 18:42:44','[{"product": "[ALAM-1138-024] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 14)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208124, "inventory_quantity": 0.0}]','2026-08-31 21:55:22',27323,'2026-09-02 18:42:44',12),
(281,'AJU/2026/0281','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 21:55:33','2026-09-02 18:43:02','[{"product": "[ALAM-1138-024] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 14)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208164, "inventory_quantity": 0.0}]','2026-08-31 21:55:33',27323,'2026-09-02 18:43:01',12),
(282,'AJU/2026/0282','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:07:45','2026-09-02 18:43:07','[{"product": "[ALAM-1138-025] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 15)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 39.0, "qty_counted": 41.0, "diff": 2.0, "lot": ""}]','[{"id": 207135, "inventory_quantity": 41.0}]','2026-08-31 22:07:45',27323,'2026-09-02 18:43:06',12),
(283,'AJU/2026/0283','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:07:54','2026-09-02 18:43:12','[{"product": "[ALAM-1138-025] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 15)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208125, "inventory_quantity": 0.0}]','2026-08-31 22:07:54',27323,'2026-09-02 18:43:12',12),
(284,'AJU/2026/0284','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:08:02','2026-09-02 18:41:44','[{"product": "[ALAM-1138-025] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 15)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208165, "inventory_quantity": 0.0}]','2026-08-31 22:08:02',27323,'2026-09-02 18:41:44',12),
(285,'AJU/2026/0285','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:09:08','2026-09-02 18:34:44','[{"product": "[ALAM-1138-026] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 16)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 21.0, "qty_counted": 23.0, "diff": 2.0, "lot": ""}]','[{"id": 207134, "inventory_quantity": 23.0}]','2026-08-31 22:09:08',27323,'2026-09-02 18:34:44',12),
(286,'AJU/2026/0286','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:09:22','2026-09-02 18:34:40','[{"product": "[ALAM-1138-026] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 16)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208126, "inventory_quantity": 0.0}]','2026-08-31 22:09:22',27323,'2026-09-02 18:34:39',12),
(287,'AJU/2026/0287','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:09:31','2026-09-02 18:34:21','[{"product": "[ALAM-1138-026] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 16)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208166, "inventory_quantity": 0.0}]','2026-08-31 22:09:31',27323,'2026-09-02 18:34:21',12),
(288,'AJU/2026/0288','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:56:51','2026-09-02 18:34:14','[{"product": "[ALAM-1138-030] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 20)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 18.0, "qty_counted": 17.0, "diff": -1.0, "lot": ""}]','[{"id": 207118, "inventory_quantity": 17.0}]','2026-08-31 22:56:51',27323,'2026-09-02 18:34:13',12),
(289,'AJU/2026/0289','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:57:27','2026-09-02 18:34:07','[{"product": "[ALAM-1138-035] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 25)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 13.0, "qty_counted": 0.0, "diff": -13.0, "lot": ""}]','[{"id": 207113, "inventory_quantity": 0.0}]','2026-08-31 22:57:27',27323,'2026-09-02 18:34:06',12),
(290,'AJU/2026/0290','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:58:24','2026-09-02 18:33:52','[{"product": "[ALAM-1138-044] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, Cerrar)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208153, "inventory_quantity": 0.0}]','2026-08-31 22:58:24',27323,'2026-09-02 18:33:52',12),
(291,'AJU/2026/0291','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:58:31','2026-09-02 18:33:46','[{"product": "[ALAM-1138-044] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, Cerrar)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208112, "inventory_quantity": 0.0}]','2026-08-31 22:58:31',27323,'2026-09-02 18:33:46',12),
(292,'AJU/2026/0292','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 22:59:17','2026-09-02 18:33:33','[{"product": "[ALAM-1138-048] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, E4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 51.0, "qty_counted": 52.0, "diff": 1.0, "lot": ""}]','[{"id": 202577, "inventory_quantity": 52.0}]','2026-08-31 22:59:17',27323,'2026-09-02 18:33:33',12),
(293,'AJU/2026/0293','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 23:04:41','2026-09-02 18:33:27','[{"product": "[ALAM-1138-049] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, PB)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208111, "inventory_quantity": 0.0}]','2026-08-31 23:04:41',27323,'2026-09-02 18:33:27',12),
(294,'AJU/2026/0294','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 23:05:58','2026-09-02 18:33:18','[{"product": "[ALAM-1138-049] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, PB)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 19.0, "qty_counted": 17.0, "diff": -2.0, "lot": ""}]','[{"id": 202584, "inventory_quantity": 17.0}]','2026-08-31 23:05:57',27323,'2026-09-02 18:33:18',12),
(295,'AJU/2026/0295','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 23:06:43','2026-09-02 18:33:10','[{"product": "[ALAM-1138-059] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, Ciego)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 1.0, "diff": -2.0, "lot": ""}]','[{"id": 204964, "inventory_quantity": 1.0}]','2026-08-31 23:06:43',27323,'2026-09-02 18:33:10',12),
(296,'AJU/2026/0296','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 23:07:19','2026-09-02 18:33:02','[{"product": "[ALAM-1138-064] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, P1)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208167, "inventory_quantity": 0.0}]','2026-08-31 23:07:19',27323,'2026-09-02 18:33:02',12),
(297,'AJU/2026/0297','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-08-31 23:07:49','2026-09-02 18:32:57','[{"product": "[ALAM-1138-065] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, P2)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 208168, "inventory_quantity": 0.0}]','2026-08-31 23:07:49',27323,'2026-09-02 18:32:57',12),
(298,'AJU/2026/0298','approved',1054,12,'Buen día, se solicita aprobación de ajuste de inventario de RH para que se pueda validar la asignación de unas botas de seguridad.',NULL,'2026-08-31 23:26:46','2026-09-02 18:32:39','[{"product": "[BOT-SEG-RH-26] Botas de Seguridad (26)", "location": "Physical Locations/WHTL/\u00c1reas/Recursos Humanos", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212326, "inventory_quantity": 1.0}]','2026-08-31 23:26:46',1054,'2026-09-02 18:32:38',12),
(299,'AJU/2026/0299','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-09-01 15:09:59','2026-09-02 18:32:26','[{"product": "[ALAM-1138-010] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 5)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208117, "inventory_quantity": 0.0}]','2026-09-01 15:09:59',27323,'2026-09-02 18:32:25',12),
(300,'AJU/2026/0300','approved',27323,12,'Conteo Ciclico

Las evidencias:
https://workdrive.zoho.com/folder/jbfghbb95460dea714289b77573f88437e52a',NULL,'2026-09-01 15:10:14','2026-09-02 18:32:08','[{"product": "[ALAM-1138-010] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 5)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 2.0, "diff": -2.0, "lot": ""}]','[{"id": 203508, "inventory_quantity": 2.0}]','2026-09-01 15:10:14',27323,'2026-09-02 18:32:07',12),
(301,'AJU/2026/0301','approved',27323,12,'Esta ajuste porque antes yo pedí cancelar el ajuste pero no se canceló y aprobó 

 Las evidencias:
https://workdrive.zoho.com/folder/c25ld9fa888fec7b449a7ad2c90c968e39512',NULL,'2026-09-03 16:05:58','2026-09-05 18:59:36','[{"product": "[ALAM-1138-030] Bot\u00f3n con Rosca Redondo con Braille 25 mm de Di\u00e1metro (Azul, 20)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 17.0, "qty_counted": 18.0, "diff": 1.0, "lot": ""}]','[{"id": 207118, "inventory_quantity": 18.0}]','2026-09-03 16:05:58',27323,'2026-09-05 18:59:35',12),
(302,'AJU/2026/0302','approved',27323,12,'Hay 2 usadas sin cajas

las evdiencias:
https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:21:29','2026-09-05 18:59:06','[{"product": "[ALAM-1126] Variador ME320LN - 220V (5.5 Kw)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 2.0, "diff": 1.0, "lot": "0103A3284P900002"}]','[{"id": 203897, "inventory_quantity": 2.0}]','2026-09-03 16:21:29',27323,'2026-09-05 18:59:05',12),
(303,'AJU/2026/0303','approved',27323,12,'Exsite dentro un control 

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:23:51','2026-09-05 18:58:58','[{"product": "[01-VAR-ME320LN-220-7.5] Variador ME320LN - 220V (7.5 Kw)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212381, "inventory_quantity": 1.0}]','2026-09-03 16:23:51',27323,'2026-09-05 18:58:58',12),
(304,'AJU/2026/0304','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:27:59','2026-09-05 18:58:49','[{"product": "[01-VAR-ALA-620] Variador Alam 620-220 V 11Kw  7.5 Hp", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212382, "inventory_quantity": 2.0}]','2026-09-03 16:27:59',27323,'2026-09-05 18:58:49',12),
(305,'AJU/2026/0305','approved',27323,12,'Para validar los OUTS OUT/31304 y OUT/31354


https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:43:23','2026-09-05 18:58:38','[{"product": "[ALAM-1003-2] Variador Inteligente Alam (220v/11kw/45A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212390, "inventory_quantity": 2.0}]','2026-09-03 16:43:23',27323,'2026-09-05 18:58:38',12),
(306,'AJU/2026/0306','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:45:10','2026-09-05 18:58:26','[{"product": "[ALAM-1003-6] Variador Inteligente Alam (220V/7.5 Kw / 32 A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212391, "inventory_quantity": 1.0}]','2026-09-03 16:45:10',27323,'2026-09-05 18:58:25',12),
(307,'AJU/2026/0307','approved',27323,12,'Conteo Ciclico

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:50:56','2026-09-05 18:58:08','[{"product": "[ALAM-1001-1] Variador ALAM Drive con Tarjeta de Encoder 1024 ((220/11Kw/45A))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212392, "inventory_quantity": 2.0}]','2026-09-03 16:50:56',27323,'2026-09-05 18:58:07',12),
(308,'AJU/2026/0308','approved',27323,12,'2 en ALM3 y 1 para validar el OUT/31169

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:52:01','2026-09-05 18:58:00','[{"product": "[ALAM-1002-9] Variador ALAMEX  (Black Model) (1024, 22 kw)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 3.0, "diff": 3.0, "lot": ""}]','[{"id": 212393, "inventory_quantity": 3.0}]','2026-09-03 16:52:01',27323,'2026-09-05 18:57:59',12),
(309,'AJU/2026/0309','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 16:57:24','2026-09-04 20:20:30','[{"product": "[ALAM-1181-3] Variador Yaskawa L1000E (220v/15Hp/41A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 4.0, "diff": 1.0, "lot": ""}]','[{"id": 211982, "inventory_quantity": 4.0}]','2026-09-03 16:57:24',27323,'2026-09-04 20:20:29',12),
(310,'AJU/2026/0310','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/c25ldf84fb5b705fc448e87a1ad32eb8c9d69',NULL,'2026-09-03 17:12:53','2026-09-04 20:20:08','[{"product": "[ALAM-1181-7] Variador Yaskawa L1000E (380V/25hp/39A)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208422, "inventory_quantity": 0.0}]','2026-09-03 17:12:53',27323,'2026-09-04 20:20:08',12),
(311,'AJU/2026/0311','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:26:28','2026-09-03 23:58:01','[{"product": "[ALAM-1142-005] COP Botonera de Cabina Bot\u00f3n Redondo (PB-5 (Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 2.0, "diff": -1.0, "lot": ""}]','[{"id": 203614, "inventory_quantity": 2.0}]','2026-09-03 18:26:28',27323,'2026-09-03 23:58:00',12),
(312,'AJU/2026/0312','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:27:41','2026-09-03 23:58:12','[{"product": "[ALAM-1142-004] COP Botonera de Cabina Bot\u00f3n Redondo (PB-4 (Display Blanco)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 211052, "inventory_quantity": 0.0}]','2026-09-03 18:27:41',27323,'2026-09-03 23:58:11',12),
(313,'AJU/2026/0313','approved',27323,12,'Conteo cíclico

https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:29:01','2026-09-03 23:58:18','[{"product": "[ALAM-1142-003] COP Botonera de Cabina Bot\u00f3n Redondo (PB-3 (Display Blanco))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 4.0, "qty_counted": 3.0, "diff": -1.0, "lot": ""}]','[{"id": 203612, "inventory_quantity": 3.0}]','2026-09-03 18:29:01',27323,'2026-09-03 23:58:17',12),
(314,'AJU/2026/0314','approved',27323,12,'Corregir las cantidades que estan en meno

https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:30:38','2026-09-04 00:00:03','[{"product": "[ALAM-1142-002] COP Botonera de Cabina Bot\u00f3n Redondo (PB-2 (Display Blanco))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210037, "inventory_quantity": 0.0}]','2026-09-03 18:30:38',27323,'2026-09-04 00:00:03',12),
(315,'AJU/2026/0315','approved',27323,12,'Porque corrigió las cantidades en menos con otro ajuste y este horita menos 1 (antes sacaron de otro ubicacion en meno en lugar este)

 https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:32:08','2026-09-04 00:00:08','[{"product": "[ALAM-1142-002] COP Botonera de Cabina Bot\u00f3n Redondo (PB-2 (Display Blanco))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 2.0, "qty_counted": 1.0, "diff": -1.0, "lot": ""}]','[{"id": 203611, "inventory_quantity": 1.0}]','2026-09-03 18:32:08',27323,'2026-09-04 00:00:08',12),
(316,'AJU/2026/0316','approved',27323,12,'Corregir las cantidades que eran en menos

https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:33:50','2026-09-03 23:57:46','[{"product": "[ALAM-1142-001] COP Botonera de Cabina Bot\u00f3n Redondo (PB-1 (Display Blanco))", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 208493, "inventory_quantity": 0.0}]','2026-09-03 18:33:50',27323,'2026-09-03 23:57:44',12),
(317,'AJU/2026/0317','approved',27323,12,'Corregir las cantidades que eran en menos

https://workdrive.zoho.com/folder/c25lda17d9079b0154f57966b0167aedda12d',NULL,'2026-09-03 18:34:34','2026-09-04 00:00:12','[{"product": "[ALAM-1142-001] COP Botonera de Cabina Bot\u00f3n Redondo (PB-1 (Display Blanco))", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210625, "inventory_quantity": 0.0}]','2026-09-03 18:34:34',27323,'2026-09-04 00:00:12',12),
(318,'AJU/2026/0318','approved',27323,12,'Conteo cíclico

https://workdrive.zoho.com/folder/th9cf850036dcad564c5d85ed6b513e548424',NULL,'2026-09-03 18:52:18','2026-09-04 00:00:20','[{"product": "[ALAM-2057] B\u00e1scula Para Cabina ALAMR100 OVERLOAD WDS", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 29.0, "qty_counted": 30.0, "diff": 1.0, "lot": ""}]','[{"id": 195110, "inventory_quantity": 30.0}]','2026-09-03 18:52:18',27323,'2026-09-04 00:00:19',12),
(319,'AJU/2026/0319','approved',27323,12,'Para borrar las 0 cantidades

https://workdrive.zoho.com/folder/1vm0i025476f66aad4771a9d99c2d40d3cf05',NULL,'2026-09-04 16:21:32','2026-09-04 20:20:04','[{"product": "[ALAM-2234-1] Solenoide Para Apila Autos (110 Voltios)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 211339, "inventory_quantity": 0.0}]','2026-09-04 16:21:32',27323,'2026-09-04 20:20:04',12),
(320,'AJU/2026/0320','approved',27323,12,'Conteo Cíclico

https://workdrive.zoho.com/folder/1vm0i025476f66aad4771a9d99c2d40d3cf05',NULL,'2026-09-04 16:22:57','2026-09-04 20:19:55','[{"product": "[ALAM-2234-3] Solenoide Para Apila Autos (24 Voltios)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 204313, "inventory_quantity": 0.0}]','2026-09-04 16:22:57',27323,'2026-09-04 20:19:54',12),
(321,'AJU/2026/0321','approved',27323,12,'Cponteo Cíclico

https://workdrive.zoho.com/folder/1vm0i025476f66aad4771a9d99c2d40d3cf05',NULL,'2026-09-04 16:23:47','2026-09-04 20:19:49','[{"product": "[ALAM-2234-3] Solenoide Para Apila Autos (24 Voltios)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 47.0, "qty_counted": 45.0, "diff": -2.0, "lot": ""}]','[{"id": 186298, "inventory_quantity": 45.0}]','2026-09-04 16:23:47',27323,'2026-09-04 20:19:48',12),
(322,'AJU/2026/0322','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmr48511f9efc76476b8b65443166922122',NULL,'2026-09-07 17:10:46','2026-09-07 17:13:24','[{"product": "[ALAM-1143-6] COP Botonera de Cabina Sistema de Enchufe Bot\u00f3n Redondo Display 7 Segmentos (0-8)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 207827, "inventory_quantity": 0.0}]','2026-09-07 17:10:46',27323,'2026-09-07 17:13:23',12),
(323,'AJU/2026/0323','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmr48511f9efc76476b8b65443166922122',NULL,'2026-09-07 17:12:03','2026-09-07 17:13:35','[{"product": "[ALAM-1143-9] COP Botonera de Cabina Sistema de Enchufe Bot\u00f3n Redondo Display 7 Segmentos (0-13)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212463, "inventory_quantity": 1.0}]','2026-09-07 17:12:03',27323,'2026-09-07 17:13:34',12),
(324,'AJU/2026/0324','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:01:31','2026-09-07 20:42:09','[{"product": "[01-COP-CCAI-0PB-03] COP Inteligente & Alam 02S (Azul, PB-3)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210174, "inventory_quantity": 0.0}]','2026-09-07 19:01:31',27323,'2026-09-07 20:42:09',12),
(325,'AJU/2026/0325','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:02:17','2026-09-07 20:42:04','[{"product": "[01-COP-CCAI-0PB-03] COP Inteligente & Alam 02S (Azul, PB-3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 210167, "inventory_quantity": 0.0}]','2026-09-07 19:02:17',27323,'2026-09-07 20:42:03',12),
(326,'AJU/2026/0326','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:04:42','2026-09-07 20:41:57','[{"product": "[01-COP-CCAI-0PB-03] COP Inteligente & Alam 02S (Azul, PB-3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212472, "inventory_quantity": 1.0}]','2026-09-07 19:04:42',27323,'2026-09-07 20:41:57',12),
(327,'AJU/2026/0327','approved',27323,12,'1 pza debe estar en ALM1 poruqe el pick para el out 30663 es validado y los otros son conteo cíclico

1 pza debe estar en ALM1 poruqe el pick para el out 30663 es validado y los otros son conteo cíclico',NULL,'2026-09-07 19:10:10','2026-09-07 20:41:52','[{"product": "[ALAM-1144-002] COP Inteligente & Alam 02S (Rojo, PB-1)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 9.0, "qty_counted": 13.0, "diff": 4.0, "lot": ""}]','[{"id": 197669, "inventory_quantity": 13.0}]','2026-09-07 19:10:10',27323,'2026-09-07 20:41:52',12),
(328,'AJU/2026/0328','approved',27323,12,'Hay 6 en ALM3 y 1 pza para OUT/29225 , 1 pza para OUT/30644

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:18:59','2026-09-07 20:41:48','[{"product": "[ALAM-1144-003] COP Inteligente & Alam 02S (Rojo, PB-2)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 7.0, "qty_counted": 8.0, "diff": 1.0, "lot": ""}]','[{"id": 197671, "inventory_quantity": 8.0}]','2026-09-07 19:18:59',27323,'2026-09-07 20:41:48',12),
(329,'AJU/2026/0329','approved',27323,12,'Corregir las cantidades en menos

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:20:41','2026-09-07 20:41:42','[{"product": "[ALAM-1144-004] COP Inteligente & Alam 02S (Rojo, PB-3)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210928, "inventory_quantity": 0.0}]','2026-09-07 19:20:41',27323,'2026-09-07 20:41:42',12),
(330,'AJU/2026/0330','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:21:19','2026-09-07 20:41:37','[{"product": "[ALAM-1144-004] COP Inteligente & Alam 02S (Rojo, PB-3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 6.0, "qty_counted": 8.0, "diff": 2.0, "lot": ""}]','[{"id": 197673, "inventory_quantity": 8.0}]','2026-09-07 19:21:19',27323,'2026-09-07 20:41:36',12),
(331,'AJU/2026/0331','approved',27323,12,'corregir ubicaciones
Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:28:39','2026-09-07 20:41:32','[{"product": "[ALAM-1144-005] COP Inteligente & Alam 02S (Rojo, PB-4)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208700, "inventory_quantity": 0.0}]','2026-09-07 19:28:39',27323,'2026-09-07 20:41:31',12),
(332,'AJU/2026/0332','approved',27323,12,'Corregir ubicaciones

Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:29:18','2026-09-07 20:41:28','[{"product": "[ALAM-1144-005] COP Inteligente & Alam 02S (Rojo, PB-4)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210700, "inventory_quantity": 0.0}]','2026-09-07 19:29:18',27323,'2026-09-07 20:41:28',12),
(333,'AJU/2026/0333','approved',27323,12,'Corregir ubicaciones

Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:33:29','2026-09-07 20:41:24','[{"product": "[ALAM-1144-005] COP Inteligente & Alam 02S (Rojo, PB-4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 208687, "inventory_quantity": 0.0}]','2026-09-07 19:33:29',27323,'2026-09-07 20:41:24',12),
(334,'AJU/2026/0334','approved',27323,12,'Corregir ubicaciones 

Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:34:15','2026-09-07 20:41:20','[{"product": "[ALAM-1144-005] COP Inteligente & Alam 02S (Rojo, PB-4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 208687, "inventory_quantity": 0.0}]','2026-09-07 19:34:15',27323,'2026-09-07 20:41:19',12),
(335,'AJU/2026/0335','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:51:23','2026-09-07 20:41:14','[{"product": "[ALAM-1144-005] COP Inteligente & Alam 02S (Rojo, PB-4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 4.0, "qty_counted": 6.0, "diff": 2.0, "lot": ""}]','[{"id": 197675, "inventory_quantity": 6.0}]','2026-09-07 19:51:23',27323,'2026-09-07 20:41:14',12),
(336,'AJU/2026/0336','approved',27323,12,'Hay 4 en ALM3 y 1 para OUT/31144 Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:52:45','2026-09-07 20:41:10','[{"product": "[ALAM-1144-007] COP Inteligente & Alam 02S (Rojo, PB-7)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 5.0, "diff": 2.0, "lot": ""}]','[{"id": 197682, "inventory_quantity": 5.0}]','2026-09-07 19:52:45',27323,'2026-09-07 20:41:09',12),
(337,'AJU/2026/0337','approved',27323,12,'Corregir las cantidades que estan en menos

Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:54:00','2026-09-07 20:41:06','[{"product": "[ALAM-1144-009] COP Inteligente & Alam 02S (Rojo, PB-8)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 206692, "inventory_quantity": 0.0}]','2026-09-07 19:54:00',27323,'2026-09-07 20:41:06',12),
(338,'AJU/2026/0338','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:54:52','2026-09-07 20:40:59','[{"product": "[ALAM-1144-009] COP Inteligente & Alam 02S (Rojo, PB-8)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 6.0, "qty_counted": 4.0, "diff": -2.0, "lot": ""}]','[{"id": 197684, "inventory_quantity": 4.0}]','2026-09-07 19:54:52',27323,'2026-09-07 20:40:59',12),
(339,'AJU/2026/0339','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 19:55:38','2026-09-07 20:40:53','[{"product": "[ALAM-1144-010] COP Inteligente & Alam 02S (Azul, PB-9)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 10.0, "qty_counted": 11.0, "diff": 1.0, "lot": ""}]','[{"id": 197730, "inventory_quantity": 11.0}]','2026-09-07 19:55:38',27323,'2026-09-07 20:40:53',12),
(340,'AJU/2026/0340','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 20:00:14','2026-09-07 20:40:46','[{"product": "[ALAM-1144-014] COP Inteligente & Alam 02S (Azul, PB-11)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 5.0, "qty_counted": 8.0, "diff": 3.0, "lot": ""}]','[{"id": 197756, "inventory_quantity": 8.0}]','2026-09-07 20:00:14',27323,'2026-09-07 20:40:46',12),
(341,'AJU/2026/0341','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 20:13:33','2026-09-07 20:40:38','[{"product": "[ALAM-1144-016] COP Inteligente & Alam 02S (Azul, PB-12)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 5.0, "qty_counted": 6.0, "diff": 1.0, "lot": ""}]','[{"id": 197758, "inventory_quantity": 6.0}]','2026-09-07 20:13:33',27323,'2026-09-07 20:40:38',12),
(342,'AJU/2026/0342','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/shpmre23a14dcbcd34f8285aae317870f81f1',NULL,'2026-09-07 20:14:24','2026-09-07 20:40:34','[{"product": "[ALAM-1144-018] COP Inteligente & Alam 02S (Azul, PB-14)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 1.0, "qty_counted": 2.0, "diff": 1.0, "lot": ""}]','[{"id": 202270, "inventory_quantity": 2.0}]','2026-09-07 20:14:24',27323,'2026-09-07 20:40:33',12),
(343,'AJU/2026/0343','approved',27323,12,'Porque había pzas en el suelo que regresaron de ALM1 a ALM3 cuando cambiamos su lugar y juntamos todo en ALM3

https://workdrive.zoho.com/folder/vmy5i398f703c4c1146c589b3175d72e9ffc4',NULL,'2026-09-07 20:54:18','2026-09-08 18:03:37','[{"product": "[ALAM-1219] Switch Sobre Paso Llanta Grande ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 122.0, "qty_counted": 127.0, "diff": 5.0, "lot": ""}]','[{"id": 205951, "inventory_quantity": 127.0}]','2026-09-07 20:54:18',27323,'2026-09-08 18:03:36',12),
(344,'AJU/2026/0344','approved',27323,12,'Porque había pzas en el suelo que regresaron de ALM1 a ALM3 cuando cambiamos su lugar y juntamos todo en ALM3

https://workdrive.zoho.com/folder/vmy5ic2d94cf51dcd4cd89de64f6cb3e18fb1',NULL,'2026-09-07 21:03:50','2026-09-08 18:03:33','[{"product": "[ALAM-1220] Switch Sobre Paso Modelo Mitsubishi", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 111.0, "qty_counted": 117.0, "diff": 6.0, "lot": ""}]','[{"id": 194285, "inventory_quantity": 117.0}]','2026-09-07 21:03:50',27323,'2026-09-08 18:03:33',12),
(345,'AJU/2026/0345','approved',27323,12,'Corregir ubicaciones

https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:16:23','2026-09-08 18:03:15','[{"product": "[ALAM-1158-2] LOP Botonera de Piso Redondos - Blancos (1 Boton Bajada + Display Blanco)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 4.0, "qty_counted": 0.0, "diff": -4.0, "lot": ""}]','[{"id": 211053, "inventory_quantity": 0.0}]','2026-09-07 22:16:23',27323,'2026-09-08 18:03:14',12),
(346,'AJU/2026/0346','approved',27323,12,'Corregir las cantidades en menos

https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:17:42','2026-09-08 18:03:11','[{"product": "[ALAM-1158-1] LOP Botonera de Piso Redondos - Blancos (2 botones + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -2.0, "qty_counted": 0.0, "diff": 2.0, "lot": ""}]','[{"id": 210627, "inventory_quantity": 0.0}]','2026-09-07 22:17:42',27323,'2026-09-08 18:03:10',12),
(347,'AJU/2026/0347','approved',27323,12,'Corregir cantidades en menos

https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:30:15','2026-09-08 18:02:57','[{"product": "[ALAM-1158-2] LOP Botonera de Piso Redondos - Blancos (1 Boton Bajada + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210155, "inventory_quantity": 0.0}]','2026-09-07 22:30:15',27323,'2026-09-08 18:02:56',12),
(348,'AJU/2026/0348','approved',27323,12,'Corregir las cantidades en menos

https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:31:09','2026-09-08 16:47:48','[{"product": "[ALAM-1158-3] LOP Botonera de Piso Redondos - Blancos (1 Boton Bajada Blanco Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210629, "inventory_quantity": 0.0}]','2026-09-07 22:31:09',27323,'2026-09-08 16:47:47',12),
(349,'AJU/2026/0349','approved',27323,12,'Corregir las cantidades en menos

https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:32:48','2026-09-08 16:47:43','[{"product": "[ALAM-1158-4] LOP Botonera de Piso Redondos - Blancos (1 Boton subida + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210153, "inventory_quantity": 0.0}]','2026-09-07 22:32:48',27323,'2026-09-08 16:47:42',12),
(350,'AJU/2026/0350','approved',27323,12,'Corregir las cantidades en menos

https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:33:37','2026-09-08 16:47:35','[{"product": "[ALAM-1158-1] LOP Botonera de Piso Redondos - Blancos (2 botones + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 207633, "inventory_quantity": 0.0}]','2026-09-07 22:33:36',27323,'2026-09-08 16:47:35',12),
(351,'AJU/2026/0351','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:35:55','2026-09-08 16:47:26','[{"product": "[ALAM-1158-1] LOP Botonera de Piso Redondos - Blancos (2 botones + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 105.0, "qty_counted": 104.0, "diff": -1.0, "lot": ""}]','[{"id": 206274, "inventory_quantity": 104.0}]','2026-09-07 22:35:55',27323,'2026-09-08 16:47:26',12),
(352,'AJU/2026/0352','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:44:19','2026-09-08 16:46:48','[{"product": "[ALAM-1158-2] LOP Botonera de Piso Redondos - Blancos (1 Boton Bajada + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 69.0, "qty_counted": 68.0, "diff": -1.0, "lot": ""}]','[{"id": 206294, "inventory_quantity": 68.0}]','2026-09-07 22:44:19',27323,'2026-09-08 16:46:48',12),
(353,'AJU/2026/0353','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:45:56','2026-09-08 16:46:43','[{"product": "[ALAM-1158-3] LOP Botonera de Piso Redondos - Blancos (1 Boton Bajada Blanco Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 327.0, "qty_counted": 329.0, "diff": 2.0, "lot": ""}]','[{"id": 206298, "inventory_quantity": 329.0}]','2026-09-07 22:45:56',27323,'2026-09-08 16:46:42',12),
(354,'AJU/2026/0354','approved',27323,12,'https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:47:08','2026-09-08 16:46:33','[{"product": "[ALAM-1158-4] LOP Botonera de Piso Redondos - Blancos (1 Boton subida + Display Blanco)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 121.0, "qty_counted": 123.0, "diff": 2.0, "lot": ""}]','[{"id": 211040, "inventory_quantity": 123.0}]','2026-09-07 22:47:08',27323,'2026-09-08 16:46:33',12),
(355,'AJU/2026/0355','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:47:56','2026-09-08 16:46:05','[{"product": "[ALAM-1158-5] LOP Botonera de Piso Redondos - Blancos (1 Botone Subida Blanco Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 125.0, "qty_counted": 123.0, "diff": -2.0, "lot": ""}]','[{"id": 206299, "inventory_quantity": 123.0}]','2026-09-07 22:47:56',27323,'2026-09-08 16:46:05',12),
(356,'AJU/2026/0356','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/vmy5if824d66bd63b4fbf83ff3984bcff6dac',NULL,'2026-09-07 22:49:25','2026-09-08 16:44:21','[{"product": "[ALAM-1158-6] LOP Botonera de Piso Redondos - Blancos (2 Botones Blanco Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 179.0, "qty_counted": 177.0, "diff": -2.0, "lot": ""}]','[{"id": 206300, "inventory_quantity": 177.0}]','2026-09-07 22:49:25',27323,'2026-09-08 16:44:21',12),
(357,'AJU/2026/0357','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-07 23:55:52','2026-09-08 16:44:07','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208720, "inventory_quantity": 0.0}]','2026-09-07 23:55:52',27323,'2026-09-08 16:44:07',12),
(358,'AJU/2026/0358','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-07 23:56:43','2026-09-08 16:43:57','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208724, "inventory_quantity": 0.0}]','2026-09-07 23:56:43',27323,'2026-09-08 16:43:56',12),
(359,'AJU/2026/0359','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-07 23:57:13','2026-09-08 16:43:51','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208707, "inventory_quantity": 0.0}]','2026-09-07 23:57:13',27323,'2026-09-08 16:43:50',12),
(360,'AJU/2026/0360','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-07 23:57:35','2026-09-08 16:43:41','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 208698, "inventory_quantity": 0.0}]','2026-09-07 23:57:35',27323,'2026-09-08 16:43:41',12),
(361,'AJU/2026/0361','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-07 23:58:39','2026-09-08 16:43:34','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 5.0, "qty_counted": 0.0, "diff": -5.0, "lot": ""}]','[{"id": 207797, "inventory_quantity": 0.0}]','2026-09-07 23:58:39',27323,'2026-09-08 16:43:34',12),
(362,'AJU/2026/0362','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-07 23:59:20','2026-09-08 16:43:27','[{"product": "[ALAM-1155-2] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Subida + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 210152, "inventory_quantity": 0.0}]','2026-09-07 23:59:20',27323,'2026-09-08 16:43:26',12),
(363,'AJU/2026/0363','approved',27323,12,'Corregir ubicaciones

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:15:08','2026-09-08 16:43:22','[{"product": "[ALAM-1155-6] LOP Botonera De Piso Cuadrados -Naranja (2 Boton + Display Binario)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 208701, "inventory_quantity": 0.0}]','2026-09-08 15:15:08',27323,'2026-09-08 16:43:22',12),
(364,'AJU/2026/0364','approved',27323,12,'Corregir las cantidades que son en menos

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:17:17','2026-09-08 16:43:09','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -6.0, "qty_counted": 0.0, "diff": 6.0, "lot": ""}]','[{"id": 210160, "inventory_quantity": 0.0}]','2026-09-08 15:17:17',27323,'2026-09-08 16:43:09',12),
(365,'AJU/2026/0365','approved',27323,12,'Corregir las cantidades que son en menos

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:18:05','2026-09-08 18:04:55','[{"product": "[ALAM-1155-2] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Subida + Display Binario)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210944, "inventory_quantity": 0.0}]','2026-09-08 15:18:05',27323,'2026-09-08 18:04:55',12),
(366,'AJU/2026/0366','approved',27323,12,'Corregir las cantidades que son en menos

Las evidencia:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:25:14','2026-09-08 16:37:56','[{"product": "[ALAM-1155-6] LOP Botonera De Piso Cuadrados -Naranja (2 Boton + Display Binario)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210930, "inventory_quantity": 0.0}]','2026-09-08 15:25:14',27323,'2026-09-08 16:37:55',12),
(367,'AJU/2026/0367','approved',27323,12,'Conteo Cíclico y corregir las cantidades que son en menos

Las evidencias:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:35:40','2026-09-08 18:04:41','[{"product": "[ALAM-1155-1] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Bajada + Display Binario)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 71.0, "qty_counted": 93.0, "diff": 22.0, "lot": ""}]','[{"id": 207687, "inventory_quantity": 93.0}]','2026-09-08 15:35:40',27323,'2026-09-08 18:04:40',12),
(368,'AJU/2026/0368','approved',27323,12,'Conteo Cíclico y corregir las cantidades que son en menos

Las evidencias:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:37:50','2026-09-08 16:37:27','[{"product": "[ALAM-1155-2] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Subida + Display Binario)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 92.0, "qty_counted": 70.0, "diff": -22.0, "lot": ""}]','[{"id": 210973, "inventory_quantity": 70.0}]','2026-09-08 15:37:50',27323,'2026-09-08 16:37:27',12),
(369,'AJU/2026/0369','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/vmy5i4e34df337e8f4f3fbb2df83ea211b8e2',NULL,'2026-09-08 15:40:28','2026-09-08 16:37:15','[{"product": "[ALAM-1155-5] LOP Botonera De Piso Cuadrados -Naranja (1 Boton Subida Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 95.0, "qty_counted": 94.0, "diff": -1.0, "lot": ""}]','[{"id": 209229, "inventory_quantity": 94.0}]','2026-09-08 15:40:28',27323,'2026-09-08 16:37:14',12),
(370,'AJU/2026/0370','approved',27323,12,'Corregir las cantidades en menos.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:25:56','2026-09-08 21:16:49','[{"product": "[ALAM-2220-2] Lop Serial Control Inteligente & 02-S (1 boton Bajada + Display Rojo)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210907, "inventory_quantity": 0.0}]','2026-09-08 19:25:56',27323,'2026-09-08 21:16:48',12),
(371,'AJU/2026/0371','approved',27323,12,'Corregir las cantidades que son en negativo.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:27:26','2026-09-08 21:16:54','[{"product": "[ALAM-2220-3] Lop Serial Control Inteligente & 02-S (1 boton Subida + Display Rojo)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210906, "inventory_quantity": 0.0}]','2026-09-08 19:27:26',27323,'2026-09-08 21:16:53',12),
(372,'AJU/2026/0372','approved',27323,12,'Corregir las cantidades que son en negativo.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:28:05','2026-09-08 21:17:08','[{"product": "[ALAM-2220-2] Lop Serial Control Inteligente & 02-S (1 boton Bajada + Display Rojo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 206687, "inventory_quantity": 0.0}]','2026-09-08 19:28:05',27323,'2026-09-08 21:17:07',12),
(373,'AJU/2026/0373','approved',27323,12,'Corregir las cantidades que son en negativo.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:28:34','2026-09-08 21:17:21','[{"product": "[ALAM-2220-3] Lop Serial Control Inteligente & 02-S (1 boton Subida + Display Rojo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 206688, "inventory_quantity": 0.0}]','2026-09-08 19:28:34',27323,'2026-09-08 21:17:21',12),
(374,'AJU/2026/0374','approved',27323,12,'Conteo cíclico.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:31:30','2026-09-08 21:17:38','[{"product": "[ALAM-2220-1] Lop Serial Control Inteligente & 02-S (2 botones + Dispaly Rojo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 243.0, "qty_counted": 230.0, "diff": -13.0, "lot": ""}]','[{"id": 207060, "inventory_quantity": 230.0}]','2026-09-08 19:31:30',27323,'2026-09-08 21:17:38',12),
(376,'AJU/2026/0376','approved',27323,12,'Conteo cíclico.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:34:17','2026-09-08 19:39:38','[{"product": "[ALAM-2220-3] Lop Serial Control Inteligente & 02-S (1 boton Subida + Display Rojo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 166.0, "qty_counted": 164.0, "diff": -2.0, "lot": ""}]','[{"id": 207062, "inventory_quantity": 164.0}]','2026-09-08 19:34:17',27323,'2026-09-08 19:39:37',12),
(377,'AJU/2026/0377','approved',27323,12,'Conteo cíclico.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:37:55','2026-09-08 21:18:44','[{"product": "[01-LOPS-CAI-SD-S1] Lop Serial Control Inteligente & 02-S (1 Boton Subida Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212500, "inventory_quantity": 1.0}]','2026-09-08 19:37:55',27323,'2026-09-08 21:18:44',12),
(378,'AJU/2026/0378','approved',27323,12,'Conteo cíclico.

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 19:43:07','2026-09-08 21:18:55','[{"product": "[01-LOPS-CAI-SD-B1] Lop Serial Control Inteligente & 02-S (1 Boton Bajada Sin Display)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212501, "inventory_quantity": 1.0}]','2026-09-08 19:43:07',27323,'2026-09-08 21:18:55',12),
(379,'AJU/2026/0379','approved',27323,12,'Conteo ciclico 

Las evidencias:

https://workdrive.zoho.com/folder/ns80403f05fe579d74e1c9d7ed7e8a7255693',NULL,'2026-09-08 21:28:01','2026-09-09 00:10:29','[{"product": "[ALAM-2220-2] Lop Serial Control Inteligente & 02-S (1 boton Bajada + Display Rojo)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 168.0, "qty_counted": 161.0, "diff": -7.0, "lot": ""}]','[{"id": 207061, "inventory_quantity": 161.0}]','2026-09-08 21:28:01',27323,'2026-09-09 00:10:28',12),
(380,'AJU/2026/0380','approved',27323,12,'Corregir cantidades que son en negativo

Las evidencias:
https://workdrive.zoho.com/folder/cf7mo5bfbec50d0404b0cbd8a9da22a560045',NULL,'2026-09-08 21:49:59','2026-09-09 20:40:43','[{"product": "[ALAM-2056] B\u00e1scula Debajo de la Cabina 1730 Kg 2 activos + 2 pasivo", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 208376, "inventory_quantity": 0.0}]','2026-09-08 21:49:59',27323,'2026-09-09 20:40:42',12),
(381,'AJU/2026/0381','approved',27323,12,'Conteo cíclico y despues corregir las cantidades negativos

Las evidencias:
https://workdrive.zoho.com/folder/cf7mo5bfbec50d0404b0cbd8a9da22a560045',NULL,'2026-09-08 21:50:55','2026-09-09 00:10:58','[{"product": "[ALAM-2056] B\u00e1scula Debajo de la Cabina 1730 Kg 2 activos + 2 pasivo", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 9.0, "qty_counted": 8.0, "diff": -1.0, "lot": ""}]','[{"id": 205941, "inventory_quantity": 8.0}]','2026-09-08 21:50:55',27323,'2026-09-09 00:10:58',12),
(382,'AJU/2026/0382','rejected',27323,12,'solo necesitamos 4 pzas para validar el OUY/30875

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840','error','2026-09-10 20:55:26','2026-09-11 18:14:17','[{"product": "[ALAM-2146 - archivado] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 5.0, "qty_counted": 4.0, "diff": -1.0, "lot": ""}]','[{"id": 201177, "inventory_quantity": 4.0}]','2026-09-10 20:55:26',27323,'2026-09-11 18:14:17',12),
(383,'AJU/2026/0383','rejected',27323,12,'Corregir las cantidades en negativo

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840','error','2026-09-10 20:58:02','2026-09-11 18:14:34','[{"product": "[ALAM-2146 - archivado] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210592, "inventory_quantity": 0.0}]','2026-09-10 20:58:02',27323,'2026-09-11 18:14:34',12),
(384,'AJU/2026/0384','rejected',27323,12,'Corregir las cantidades en negativo

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840','error','2026-09-10 20:58:22','2026-09-11 18:14:48','[{"product": "[ALAM-2146 - archivado] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -7.0, "qty_counted": 0.0, "diff": 7.0, "lot": ""}]','[{"id": 205006, "inventory_quantity": 0.0}]','2026-09-10 20:58:22',27323,'2026-09-11 18:14:48',12),
(385,'AJU/2026/0385','approved',27323,12,'estas cantidades transfirio al otro producto

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-10 20:59:17','2026-09-11 18:16:17','[{"product": "[ALAM-2146 - archivado] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 461.0, "qty_counted": 0.0, "diff": -461.0, "lot": ""}]','[{"id": 199655, "inventory_quantity": 0.0}]','2026-09-10 20:59:17',27323,'2026-09-11 18:16:17',12),
(386,'AJU/2026/0386','approved',27323,12,'Corregir cantidades en negativo

Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 16:18:58','2026-09-11 18:16:05','[{"product": "[ALAM-6130] Inserto Duro Para Zapata Riel T50 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210540, "inventory_quantity": 0.0}]','2026-09-11 16:18:58',27323,'2026-09-11 18:16:05',12),
(387,'AJU/2026/0387','approved',27323,12,'Conteo cíclico

Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 16:20:34','2026-09-11 18:15:49','[{"product": "[ALAM-6130] Inserto Duro Para Zapata Riel T50 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 444.0, "qty_counted": 438.0, "diff": -6.0, "lot": ""}]','[{"id": 206316, "inventory_quantity": 438.0}]','2026-09-11 16:20:34',27323,'2026-09-11 18:15:49',12),
(388,'AJU/2026/0388','approved',27323,12,'Corregir las cantidades negativos

Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 16:27:26','2026-09-11 18:15:34','[{"product": "[ALAM-6023] Inserto Duro de Zapatas Para Riel T70 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210544, "inventory_quantity": 0.0}]','2026-09-11 16:27:26',27323,'2026-09-11 18:15:33',12),
(389,'AJU/2026/0389','approved',27323,12,'Conteo cíclico 

Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 16:33:17','2026-09-11 18:15:25','[{"product": "[ALAM-6023] Inserto Duro de Zapatas Para Riel T70 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 494.0, "qty_counted": 499.0, "diff": 5.0, "lot": ""}]','[{"id": 203973, "inventory_quantity": 499.0}]','2026-09-11 16:33:17',27323,'2026-09-11 18:15:24',12),
(390,'AJU/2026/0390','approved',27323,12,'Corregir las cantidades negativas

Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 18:04:18','2026-09-11 18:15:07','[{"product": "[ALAM-6024] Inserto Duro de Zapatas Para Rieles T89 y T90 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210542, "inventory_quantity": 0.0}]','2026-09-11 18:04:18',27323,'2026-09-11 18:15:07',12),
(391,'AJU/2026/0391','approved',27323,12,'Corregir ubicaciones

Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 18:04:47','2026-09-11 18:15:02','[{"product": "[ALAM-6024] Inserto Duro de Zapatas Para Rieles T89 y T90 (Duro)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 209942, "inventory_quantity": 0.0}]','2026-09-11 18:04:47',27323,'2026-09-11 18:15:01',12),
(392,'AJU/2026/0392','approved',27323,12,'Conteo cíclico y corregir las cantidades negativas con ubicaciones falso


Las evidencias:
https://workdrive.zoho.com/folder/aofp7ecbfecb0303142eda9a3a2ce726f7477',NULL,'2026-09-11 18:06:03','2026-09-11 18:14:57','[{"product": "[ALAM-6024] Inserto Duro de Zapatas Para Rieles T89 y T90 (Duro)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 270.0, "qty_counted": 269.0, "diff": -1.0, "lot": ""}]','[{"id": 211694, "inventory_quantity": 269.0}]','2026-09-11 18:06:03',27323,'2026-09-11 18:14:56',12),
(393,'AJU/2026/0393','approved',27323,12,'Corregir las cantidades negativas

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-11 21:37:05','2026-09-12 00:24:23','[{"product": "[ALAM-2025] Base de Goma Para Cabina (Tipo L)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210566, "inventory_quantity": 0.0}]','2026-09-11 21:37:05',27323,'2026-09-12 00:24:22',12),
(394,'AJU/2026/0394','approved',27323,12,'Conteo cíclico

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-11 21:38:13','2026-09-12 00:24:54','[{"product": "[ALAM-2025] Base de Goma Para Cabina (Tipo L)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 32.0, "qty_counted": 40.0, "diff": 8.0, "lot": ""}]','[{"id": 206680, "inventory_quantity": 40.0}]','2026-09-11 21:38:13',27323,'2026-09-12 00:24:54',12),
(395,'AJU/2026/0395','approved',27323,12,'Corregir las cantidades negativas

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-11 23:21:14','2026-09-12 00:24:40','[{"product": "[ALAM-2113] Goma Doble Tornillo Para Cabina ", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210572, "inventory_quantity": 0.0}]','2026-09-11 23:21:14',27323,'2026-09-12 00:24:40',12),
(396,'AJU/2026/0396','approved',27323,12,'Conteo cíclico 

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-11 23:24:00','2026-09-12 00:25:00','[{"product": "[ALAM-2113] Goma Doble Tornillo Para Cabina ", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 69.0, "qty_counted": 77.0, "diff": 8.0, "lot": ""}]','[{"id": 207064, "inventory_quantity": 77.0}]','2026-09-11 23:24:00',27323,'2026-09-12 00:25:00',12),
(397,'AJU/2026/0397','approved',27323,12,'Corregir las cantidades negativas

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 17:30:24','2026-09-14 19:34:58','[{"product": "[ALAM-2114] Goma Rectangular 10cm x 6.2cm x 2.5cm", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210570, "inventory_quantity": 0.0}]','2026-09-12 17:30:24',27323,'2026-09-14 19:34:58',12),
(398,'AJU/2026/0398','approved',27323,12,'Conteo cíclico y corregir las cantidades negativas

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 17:31:13','2026-09-14 19:34:54','[{"product": "[ALAM-2114] Goma Rectangular 10cm x 6.2cm x 2.5cm", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 2.0, "qty_counted": 1.0, "diff": -1.0, "lot": ""}]','[{"id": 206674, "inventory_quantity": 1.0}]','2026-09-12 17:31:13',27323,'2026-09-14 19:34:53',12),
(399,'AJU/2026/0399','approved',27323,12,'Corregir las cantidades negativas

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 18:13:59','2026-09-14 19:34:48','[{"product": "[ALAM-2112] Goma Cuadrada 8X87.5*11.5*9.5X8cm (12x8x10)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210568, "inventory_quantity": 0.0}]','2026-09-12 18:13:59',27323,'2026-09-14 19:34:48',12),
(400,'AJU/2026/0400','approved',27323,12,'Corregir las cantidades negativas
aqui hacemos menos 1 porque sacabó de otro ubicacion em negativo 


Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 18:15:13','2026-09-14 19:34:43','[{"product": "[ALAM-2112] Goma Cuadrada 8X87.5*11.5*9.5X8cm (12x8x10)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 120.0, "qty_counted": 119.0, "diff": -1.0, "lot": ""}]','[{"id": 206673, "inventory_quantity": 119.0}]','2026-09-12 18:15:13',27323,'2026-09-14 19:34:43',12),
(401,'AJU/2026/0401','approved',27323,12,'Va transferir las cantidades a otro variante que tiene el correcto info 70x70x23',NULL,'2026-09-12 18:26:07','2026-09-14 19:34:31','[{"product": "[ALAM-2021-1] Base de Goma Cuadrada (50x50x50 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 237.0, "qty_counted": 0.0, "diff": -237.0, "lot": ""}]','[{"id": 206678, "inventory_quantity": 0.0}]','2026-09-12 18:26:07',27323,'2026-09-14 19:34:30',12),
(402,'AJU/2026/0402','approved',27323,12,'Va transferir las cantidades a otro variante se llama 70x70x23

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 18:28:19','2026-09-14 19:34:25','[{"product": "[ALAM-2021-2] Base de Goma Cuadrada (70x70x70 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 202.0, "qty_counted": 0.0, "diff": -202.0, "lot": ""}]','[{"id": 206679, "inventory_quantity": 0.0}]','2026-09-12 18:28:19',27323,'2026-09-14 19:34:25',12),
(403,'AJU/2026/0403','approved',27323,12,'Creó este variante porque no existe antes y su cantidades eran con el variante 70x70x70

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 18:30:20','2026-09-14 19:34:17','[{"product": "[ALAM-2021-6] Base de Goma Cuadrada (70x70x23 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 190.0, "diff": 190.0, "lot": ""}]','[{"id": 212573, "inventory_quantity": 190.0}]','2026-09-12 18:30:20',27323,'2026-09-14 19:34:17',12),
(404,'AJU/2026/0404','approved',27323,12,'Creó este variante nuevamente porque no era existe y las cantidades con otro vaiante se llama 50x50x50

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 18:31:39','2026-09-14 19:33:55','[{"product": "[ALAM-2021-7] Base de Goma Cuadrada (50x50x23 mm)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 237.0, "diff": 237.0, "lot": ""}]','[{"id": 212574, "inventory_quantity": 237.0}]','2026-09-12 18:31:39',27323,'2026-09-14 19:33:54',12),
(405,'AJU/2026/0405','approved',27323,12,'Este producto ha modificado para incluye las cantidades que existen en inventario fisicamente

Las evidencias:
https://workdrive.zoho.com/folder/b9qzj5b7d92b2442345c28800315829117d3e',NULL,'2026-09-12 18:41:04','2026-09-14 19:33:47','[{"product": "[ALAM-2115] Goma Doble Tornillo Para Cabina Grande 10 mm", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 4.0, "diff": 4.0, "lot": ""}]','[{"id": 212575, "inventory_quantity": 4.0}]','2026-09-12 18:41:04',27323,'2026-09-14 19:33:46',12),
(406,'AJU/2026/0406','approved',27323,12,'en justo hay 803 pzas pero creó otro variantes va considerar allí

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:13:24','2026-09-14 19:33:37','[{"product": "[02-REC-ACE-0001] Recolector De Aceite C\u00edrculo", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": "17-06-2024"}]','[{"id": 141520, "inventory_quantity": 0.0}]','2026-09-12 19:13:23',27323,'2026-09-14 19:33:36',12),
(407,'AJU/2026/0407','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:15:23','2026-09-14 19:33:24','[{"product": "Recolector De Aceite C\u00edrculo (Blanco - 4 Lados)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 6.0, "diff": 6.0, "lot": ""}]','[{"id": 212576, "inventory_quantity": 6.0}]','2026-09-12 19:15:23',27323,'2026-09-14 19:33:23',12),
(408,'AJU/2026/0408','approved',27323,12,'Conteo cíclico 

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:16:29','2026-09-14 19:33:01','[{"product": "Recolector De Aceite C\u00edrculo (Gris - 4 Lados)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212577, "inventory_quantity": 2.0}]','2026-09-12 19:16:29',27323,'2026-09-14 19:33:00',12),
(409,'AJU/2026/0409','approved',27323,12,'Conteo cíclico
4 pzas para poder validar NWH/OUT/30875 porque su pick validado

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:25:16','2026-09-14 19:32:55','[{"product": "[ALAM-2146] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 5.0, "qty_counted": 4.0, "diff": -1.0, "lot": ""}]','[{"id": 201177, "inventory_quantity": 4.0}]','2026-09-12 19:25:16',27323,'2026-09-14 19:32:54',12),
(410,'AJU/2026/0410','approved',27323,12,'Corregir cantidades  negativos

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:26:11','2026-09-14 19:32:38','[{"product": "[ALAM-2146] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": -1.0, "qty_counted": 0.0, "diff": 1.0, "lot": ""}]','[{"id": 210592, "inventory_quantity": 0.0}]','2026-09-12 19:26:11',27323,'2026-09-14 19:32:37',12),
(411,'AJU/2026/0411','approved',27323,12,'Corregir cantidades  negativos

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:26:19','2026-09-14 19:32:34','[{"product": "[ALAM-2146] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": -7.0, "qty_counted": 0.0, "diff": 7.0, "lot": ""}]','[{"id": 205006, "inventory_quantity": 0.0}]','2026-09-12 19:26:19',27323,'2026-09-14 19:32:33',12),
(412,'AJU/2026/0412','approved',27323,12,'Conteo cíclico

Las evidencias:
https://workdrive.zoho.com/folder/rzv8i18c4d8e75d2348bea4d170e34a40e840',NULL,'2026-09-12 19:27:46','2026-09-14 19:32:27','[{"product": "[ALAM-2146] Recolector de Aceite Cuadrado", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 400.0, "diff": 400.0, "lot": ""}]','[{"id": 212578, "inventory_quantity": 400.0}]','2026-09-12 19:27:46',27323,'2026-09-14 19:32:26',12),
(413,'AJU/2026/0413','approved',27323,12,'Corregir ubicacion

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:22:46','2026-09-14 19:32:22','[{"product": "[ALAM-1130-013] Bot\u00f3n Redondo Blanco (Bajar)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 8.0, "qty_counted": 0.0, "diff": -8.0, "lot": ""}]','[{"id": 205197, "inventory_quantity": 0.0}]','2026-09-12 20:22:46',27323,'2026-09-14 19:32:21',12),
(414,'AJU/2026/0414','approved',27323,12,'Corregir ubicacion

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:23:28','2026-09-14 19:32:17','[{"product": "[ALAM-1130-041] Bot\u00f3n Redondo Blanco (6)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 205999, "inventory_quantity": 0.0}]','2026-09-12 20:23:28',27323,'2026-09-14 19:32:16',12),
(415,'AJU/2026/0415','approved',27323,12,'Corregir ubicacion

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:23:59','2026-09-14 19:31:55','[{"product": "[ALAM-1130-042] Bot\u00f3n Redondo Blanco (7)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 206000, "inventory_quantity": 0.0}]','2026-09-12 20:23:59',27323,'2026-09-14 19:31:55',12),
(416,'AJU/2026/0416','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:25:07','2026-09-14 19:31:28','[{"product": "[ALAM-1130-001] Bot\u00f3n Redondo Blanco (10)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 25.0, "qty_counted": 27.0, "diff": 2.0, "lot": ""}]','[{"id": 206704, "inventory_quantity": 27.0}]','2026-09-12 20:25:07',27323,'2026-09-14 19:31:28',12),
(417,'AJU/2026/0417','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:25:36','2026-09-14 19:31:16','[{"product": "[ALAM-1130-002] Bot\u00f3n Redondo Blanco (11)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 11.0, "qty_counted": 13.0, "diff": 2.0, "lot": ""}]','[{"id": 206705, "inventory_quantity": 13.0}]','2026-09-12 20:25:36',27323,'2026-09-14 19:31:16',12),
(418,'AJU/2026/0418','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:25:58','2026-09-14 19:31:07','[{"product": "[ALAM-1130-003] Bot\u00f3n Redondo Blanco (12)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 16.0, "qty_counted": 17.0, "diff": 1.0, "lot": ""}]','[{"id": 206706, "inventory_quantity": 17.0}]','2026-09-12 20:25:58',27323,'2026-09-14 19:31:07',12),
(419,'AJU/2026/0419','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:26:48','2026-09-14 19:30:55','[{"product": "[ALAM-1130-010] Bot\u00f3n Redondo Blanco (Abrir)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 21.0, "qty_counted": 23.0, "diff": 2.0, "lot": ""}]','[{"id": 206718, "inventory_quantity": 23.0}]','2026-09-12 20:26:48',27323,'2026-09-14 19:30:55',12),
(420,'AJU/2026/0420','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:27:38','2026-09-14 19:30:23','[{"product": "[ALAM-1130-011] Bot\u00f3n Redondo Blanco (Cerrar)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 35.0, "qty_counted": 37.0, "diff": 2.0, "lot": ""}]','[{"id": 206719, "inventory_quantity": 37.0}]','2026-09-12 20:27:38',27323,'2026-09-14 19:30:23',12),
(421,'AJU/2026/0421','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:28:00','2026-09-14 19:30:09','[{"product": "[ALAM-1130-012] Bot\u00f3n Redondo Blanco (Subir)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 25.0, "qty_counted": 22.0, "diff": -3.0, "lot": ""}]','[{"id": 206720, "inventory_quantity": 22.0}]','2026-09-12 20:28:00',27323,'2026-09-14 19:30:08',12),
(422,'AJU/2026/0422','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:29:15','2026-09-14 19:29:48','[{"product": "[ALAM-1130-013] Bot\u00f3n Redondo Blanco (Bajar)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 27.0, "qty_counted": 20.0, "diff": -7.0, "lot": ""}]','[{"id": 209238, "inventory_quantity": 20.0}]','2026-09-12 20:29:15',27323,'2026-09-14 19:29:47',12),
(423,'AJU/2026/0423','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:29:58','2026-09-14 19:29:37','[{"product": "[ALAM-1130-014] Bot\u00f3n Redondo Blanco (PB)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 46.0, "qty_counted": 61.0, "diff": 15.0, "lot": ""}]','[{"id": 206722, "inventory_quantity": 61.0}]','2026-09-12 20:29:58',27323,'2026-09-14 19:29:37',12),
(424,'AJU/2026/0424','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:30:31','2026-09-14 19:29:28','[{"product": "[ALAM-1130-016] Bot\u00f3n Redondo Blanco (PH)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 27.0, "qty_counted": 23.0, "diff": -4.0, "lot": ""}]','[{"id": 206723, "inventory_quantity": 23.0}]','2026-09-12 20:30:31',27323,'2026-09-14 19:29:27',12),
(425,'AJU/2026/0425','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:31:07','2026-09-14 19:28:06','[{"product": "[ALAM-1130-017] Bot\u00f3n Redondo Blanco (Ventilador)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 19.0, "qty_counted": 18.0, "diff": -1.0, "lot": ""}]','[{"id": 206724, "inventory_quantity": 18.0}]','2026-09-12 20:31:07',27323,'2026-09-14 19:28:05',12),
(426,'AJU/2026/0426','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:31:49','2026-09-14 19:35:21','[{"product": "[ALAM-1130-021] Bot\u00f3n Redondo Blanco (3)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 19.0, "qty_counted": 23.0, "diff": 4.0, "lot": ""}]','[{"id": 209233, "inventory_quantity": 23.0}]','2026-09-12 20:31:49',27323,'2026-09-14 19:35:21',12),
(427,'AJU/2026/0427','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:32:08','2026-09-14 19:27:55','[{"product": "[ALAM-1130-022] Bot\u00f3n Redondo Blanco (S)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 45.0, "qty_counted": 44.0, "diff": -1.0, "lot": ""}]','[{"id": 206728, "inventory_quantity": 44.0}]','2026-09-12 20:32:08',27323,'2026-09-14 19:27:54',12),
(428,'AJU/2026/0428','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:32:27','2026-09-14 19:20:12','[{"product": "[ALAM-1130-023] Bot\u00f3n Redondo Blanco (S1)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 19.0, "qty_counted": 18.0, "diff": -1.0, "lot": ""}]','[{"id": 206729, "inventory_quantity": 18.0}]','2026-09-12 20:32:27',27323,'2026-09-14 19:20:12',12),
(429,'AJU/2026/0429','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:33:18','2026-09-14 19:20:07','[{"product": "[ALAM-1130-032] Bot\u00f3n Redondo Blanco (4)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 33.0, "qty_counted": 36.0, "diff": 3.0, "lot": ""}]','[{"id": 206698, "inventory_quantity": 36.0}]','2026-09-12 20:33:18',27323,'2026-09-14 19:20:07',12),
(430,'AJU/2026/0430','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:34:36','2026-09-14 19:19:57','[{"product": "[ALAM-1130-040] Bot\u00f3n Redondo Blanco (5)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 32.0, "qty_counted": 35.0, "diff": 3.0, "lot": ""}]','[{"id": 206699, "inventory_quantity": 35.0}]','2026-09-12 20:34:36',27323,'2026-09-14 19:19:57',12),
(431,'AJU/2026/0431','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:35:13','2026-09-14 19:19:49','[{"product": "[ALAM-1130-041] Bot\u00f3n Redondo Blanco (6)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 43.0, "qty_counted": 48.0, "diff": 5.0, "lot": ""}]','[{"id": 206700, "inventory_quantity": 48.0}]','2026-09-12 20:35:13',27323,'2026-09-14 19:19:49',12),
(432,'AJU/2026/0432','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:35:47','2026-09-14 19:19:43','[{"product": "[ALAM-1130-042] Bot\u00f3n Redondo Blanco (7)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 5.0, "qty_counted": 8.0, "diff": 3.0, "lot": ""}]','[{"id": 206701, "inventory_quantity": 8.0}]','2026-09-12 20:35:47',27323,'2026-09-14 19:19:43',12),
(433,'AJU/2026/0433','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:36:27','2026-09-14 19:19:39','[{"product": "[ALAM-1130-043] Bot\u00f3n Redondo Blanco (8)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 27.0, "qty_counted": 28.0, "diff": 1.0, "lot": ""}]','[{"id": 206702, "inventory_quantity": 28.0}]','2026-09-12 20:36:27',27323,'2026-09-14 19:19:38',12),
(434,'AJU/2026/0434','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:37:04','2026-09-14 19:19:22','[{"product": "[ALAM-1130-044] Bot\u00f3n Redondo Blanco (9)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 23.0, "qty_counted": 25.0, "diff": 2.0, "lot": ""}]','[{"id": 206703, "inventory_quantity": 25.0}]','2026-09-12 20:37:04',27323,'2026-09-14 19:19:22',12),
(435,'AJU/2026/0435','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:37:29','2026-09-14 19:19:13','[{"product": "[ALAM-1130-045] Bot\u00f3n Redondo Blanco (1)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 16.0, "qty_counted": 17.0, "diff": 1.0, "lot": ""}]','[{"id": 209231, "inventory_quantity": 17.0}]','2026-09-12 20:37:29',27323,'2026-09-14 19:19:13',12),
(436,'AJU/2026/0436','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:38:03','2026-09-14 19:19:03','[{"product": "[ALAM-1130-046] Bot\u00f3n Redondo Blanco (2)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 20.0, "qty_counted": 26.0, "diff": 6.0, "lot": ""}]','[{"id": 209232, "inventory_quantity": 26.0}]','2026-09-12 20:38:03',27323,'2026-09-14 19:19:03',12),
(437,'AJU/2026/0437','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:40:15','2026-09-14 19:18:38','[{"product": "[ALAM-1130-050] Bot\u00f3n Redondo Blanco (28)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212579, "inventory_quantity": 2.0}]','2026-09-12 20:40:15',27323,'2026-09-14 19:18:37',12),
(438,'AJU/2026/0438','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:40:52','2026-09-14 19:18:33','[{"product": "[ALAM-1130-051] Bot\u00f3n Redondo Blanco (29)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212580, "inventory_quantity": 2.0}]','2026-09-12 20:40:52',27323,'2026-09-14 19:18:32',12),
(439,'AJU/2026/0439','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:41:25','2026-09-14 19:18:23','[{"product": "[ALAM-1130-052] Bot\u00f3n Redondo Blanco (30)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212581, "inventory_quantity": 2.0}]','2026-09-12 20:41:25',27323,'2026-09-14 19:18:23',12),
(440,'AJU/2026/0440','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:42:07','2026-09-14 19:18:19','[{"product": "[ALAM-1130-053] Bot\u00f3n Redondo Blanco (31)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212582, "inventory_quantity": 2.0}]','2026-09-12 20:42:07',27323,'2026-09-14 19:18:19',12),
(441,'AJU/2026/0441','approved',27323,12,'Conteo ciclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 20:42:49','2026-09-14 19:18:11','[{"product": "[ALAM-1130-054] Bot\u00f3n Redondo Blanco (J)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 2.0, "diff": 2.0, "lot": ""}]','[{"id": 212583, "inventory_quantity": 2.0}]','2026-09-12 20:42:49',27323,'2026-09-14 19:18:11',12),
(442,'AJU/2026/0442','approved',27323,12,'Corregir ubicacion

Las evidencias:
https://workdrive.zoho.com/folder/n82bd129e0876d54143a0bcfd3b59ca4f0072',NULL,'2026-09-12 21:10:11','2026-09-14 19:18:05','[{"product": "[ALAM-2214-1] Fuente Chica (24 Volt Entrada 100 a 240 Volt) (4.5 A.)", "location": "Physical Locations/WHTL/Almac\u00e9n 1", "qty_system": 1.0, "qty_counted": 0.0, "diff": -1.0, "lot": ""}]','[{"id": 209422, "inventory_quantity": 0.0}]','2026-09-12 21:10:11',27323,'2026-09-14 19:18:05',12),
(443,'AJU/2026/0443','approved',27323,12,'Corregir ubicacion

Las evidencias:
https://workdrive.zoho.com/folder/n82bd129e0876d54143a0bcfd3b59ca4f0072',NULL,'2026-09-12 21:10:36','2026-09-14 19:17:56','[{"product": "[ALAM-2214-1] Fuente Chica (24 Volt Entrada 100 a 240 Volt) (4.5 A.)", "location": "Physical Locations/WHTL/Stock Doppler", "qty_system": 2.0, "qty_counted": 0.0, "diff": -2.0, "lot": ""}]','[{"id": 212306, "inventory_quantity": 0.0}]','2026-09-12 21:10:36',27323,'2026-09-14 19:17:56',12),
(444,'AJU/2026/0444','approved',27323,12,'Corregir ubicacion

Las evidencias:
https://workdrive.zoho.com/folder/n82bd129e0876d54143a0bcfd3b59ca4f0072',NULL,'2026-09-12 21:11:00','2026-09-14 19:17:42','[{"product": "[ALAM-2214-1] Fuente Chica (24 Volt Entrada 100 a 240 Volt) (4.5 A.)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 2", "qty_system": 29.0, "qty_counted": 0.0, "diff": -29.0, "lot": ""}]','[{"id": 211006, "inventory_quantity": 0.0}]','2026-09-12 21:11:00',27323,'2026-09-14 19:17:42',12),
(445,'AJU/2026/0445','approved',27323,12,'Conteo cíclico y Corregir ubicaciones

Las evidencias:
https://workdrive.zoho.com/folder/n82bd129e0876d54143a0bcfd3b59ca4f0072',NULL,'2026-09-12 21:11:36','2026-09-14 19:17:28','[{"product": "[ALAM-2214-1] Fuente Chica (24 Volt Entrada 100 a 240 Volt) (4.5 A.)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 3.0, "qty_counted": 36.0, "diff": 33.0, "lot": ""}]','[{"id": 208921, "inventory_quantity": 36.0}]','2026-09-12 21:11:36',27323,'2026-09-14 19:17:28',12),
(446,'AJU/2026/0446','approved',27323,12,'Conteo Cíclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd129e0876d54143a0bcfd3b59ca4f0072',NULL,'2026-09-12 21:12:10','2026-09-14 19:17:15','[{"product": "[ALAM-2214-2] Fuente Chica (24 Volt Entrada 100 a 240 Volt) (6.5 A.)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 4.0, "qty_counted": 3.0, "diff": -1.0, "lot": ""}]','[{"id": 208922, "inventory_quantity": 3.0}]','2026-09-12 21:12:10',27323,'2026-09-14 19:17:15',12),
(447,'AJU/2026/0447','approved',27323,12,'Se creó nuevo variante con el conteo cíclico

Las evidencias:
https://workdrive.zoho.com/folder/n82bd129e0876d54143a0bcfd3b59ca4f0072',NULL,'2026-09-12 21:13:39','2026-09-14 19:17:03','[{"product": "[ALAM-2214-3] Fuente Chica (24 Volt Entrada 100 a 240 Volt) (5 A.)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 5.0, "diff": 5.0, "lot": ""}]','[{"id": 212584, "inventory_quantity": 5.0}]','2026-09-12 21:13:39',27323,'2026-09-14 19:17:02',12),
(448,'AJU/2026/0448','approved',27323,12,'Conteo cíclico

https://workdrive.zoho.com/folder/n82bd45985834406d420c9f671e50535ecc29',NULL,'2026-09-12 21:40:40','2026-09-14 19:16:54','[{"product": "[ALAM-1130-020] Bot\u00f3n Redondo Blanco (Ciego)", "location": "Physical Locations/WHTL/Stock Doppler/Almac\u00e9n 3", "qty_system": 0.0, "qty_counted": 1.0, "diff": 1.0, "lot": ""}]','[{"id": 212585, "inventory_quantity": 1.0}]','2026-09-12 21:40:40',27323,'2026-09-14 19:16:53',12)
ON CONFLICT (id) DO NOTHING;
SELECT setval('stock_adjustment_request_id_seq', (SELECT max(id) FROM stock_adjustment_request));
COMMIT;
