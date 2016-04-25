
CREATE SEQUENCE public.gestion_pago_id_gestionpago_seq;

CREATE TABLE public.gestion_pago (
                id_gestionpago INTEGER NOT NULL DEFAULT nextval('public.gestion_pago_id_gestionpago_seq'),
                numero_tarjeta INTEGER NOT NULL,
                fecha_caducidad VARCHAR(5) NOT NULL,
                cvc INTEGER NOT NULL,
                saldo NUMERIC NOT NULL,
                CONSTRAINT id_gestionpago PRIMARY KEY (id_gestionpago)
);


ALTER SEQUENCE public.gestion_pago_id_gestionpago_seq OWNED BY public.gestion_pago.id_gestionpago;

CREATE SEQUENCE public.tipo_eventos_id_tipoevento_seq;

CREATE TABLE public.tipo_eventos (
                id_tipoevento INTEGER NOT NULL DEFAULT nextval('public.tipo_eventos_id_tipoevento_seq'),
                nombre_tipoevento VARCHAR(25) NOT NULL,
                CONSTRAINT id_tipoevento PRIMARY KEY (id_tipoevento)
);


ALTER SEQUENCE public.tipo_eventos_id_tipoevento_seq OWNED BY public.tipo_eventos.id_tipoevento;

CREATE SEQUENCE public.eventos_id_evento_seq;

CREATE TABLE public.eventos (
                id_evento INTEGER NOT NULL DEFAULT nextval('public.eventos_id_evento_seq'),
                nombre VARCHAR(50) NOT NULL,
                imagen VARCHAR(75),
                descripcion VARCHAR(250) NOT NULL,
                precio NUMERIC NOT NULL,
                consultas INTEGER DEFAULT 0 NOT NULL,
                estado VARCHAR(25) NOT NULL,
                tipo_evento INTEGER NOT NULL,
                CONSTRAINT id_evento PRIMARY KEY (id_evento)
);


ALTER SEQUENCE public.eventos_id_evento_seq OWNED BY public.eventos.id_evento;

CREATE SEQUENCE public.sesiones_id_sesion_seq;

CREATE TABLE public.sesiones (
                id_sesion INTEGER NOT NULL DEFAULT nextval('public.sesiones_id_sesion_seq'),
                ciudad VARCHAR(25) NOT NULL,
                lugar VARCHAR(25) NOT NULL,
                sesion TIMESTAMP NOT NULL,
                capacidad INTEGER NOT NULL,
                entradas_vendidas INTEGER DEFAULT 0 NOT NULL,
                id_evento INTEGER NOT NULL,
                CONSTRAINT id_sesion PRIMARY KEY (id_sesion)
);


ALTER SEQUENCE public.sesiones_id_sesion_seq OWNED BY public.sesiones.id_sesion;

CREATE SEQUENCE public.entradas_id_entrada_seq;

CREATE TABLE public.entradas (
                id_entrada INTEGER NOT NULL DEFAULT nextval('public.entradas_id_entrada_seq'),
                fecha_compra TIMESTAMP NOT NULL,
                nombre VARCHAR(25) NOT NULL,
                apellido VARCHAR(25) NOT NULL,
                dni VARCHAR(10) NOT NULL,
                telefono VARCHAR(25) NOT NULL,
                edad INTEGER NOT NULL,
                email VARCHAR(50) NOT NULL,
                id_sesion INTEGER NOT NULL,
                CONSTRAINT id_entrada PRIMARY KEY (id_entrada)
);


ALTER SEQUENCE public.entradas_id_entrada_seq OWNED BY public.entradas.id_entrada;

ALTER TABLE public.eventos ADD CONSTRAINT tipo_eventos_eventos_fk
FOREIGN KEY (tipo_evento)
REFERENCES public.tipo_eventos (id_tipoevento)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.sesiones ADD CONSTRAINT eventos_sesiones_fk
FOREIGN KEY (id_evento)
REFERENCES public.eventos (id_evento)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.entradas ADD CONSTRAINT sesiones_entradas_fk
FOREIGN KEY (id_sesion)
REFERENCES public.sesiones (id_sesion)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
