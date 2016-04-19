
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
                fecha DATE NOT NULL,
                lugar VARCHAR(25) NOT NULL,
                descripcion VARCHAR(250) NOT NULL,
                precio NUMERIC NOT NULL,
                capacidad INTEGER NOT NULL,
                entradas_vendidas INTEGER NOT NULL,
                consultas INTEGER NOT NULL,
                estado VARCHAR(25) NOT NULL,
                tipo_evento INTEGER NOT NULL,
                CONSTRAINT id_evento PRIMARY KEY (id_evento)
);


ALTER SEQUENCE public.eventos_id_evento_seq OWNED BY public.eventos.id_evento;

CREATE SEQUENCE public.horarios_id_horario_seq;

CREATE TABLE public.horarios (
                id_horario INTEGER NOT NULL DEFAULT nextval('public.horarios_id_horario_seq'),
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                id_evento INTEGER NOT NULL,
                CONSTRAINT id_horario PRIMARY KEY (id_horario)
);


ALTER SEQUENCE public.horarios_id_horario_seq OWNED BY public.horarios.id_horario;

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
                id_evento INTEGER NOT NULL,
                CONSTRAINT id_entrada PRIMARY KEY (id_entrada)
);


ALTER SEQUENCE public.entradas_id_entrada_seq OWNED BY public.entradas.id_entrada;

ALTER TABLE public.eventos ADD CONSTRAINT tipo_eventos_eventos_fk
FOREIGN KEY (tipo_evento)
REFERENCES public.tipo_eventos (id_tipoevento)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.entradas ADD CONSTRAINT eventos_entradas_fk
FOREIGN KEY (id_evento)
REFERENCES public.eventos (id_evento)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.horarios ADD CONSTRAINT eventos_horarios_fk
FOREIGN KEY (id_evento)
REFERENCES public.eventos (id_evento)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
