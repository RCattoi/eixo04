-- alternativa.dim_cliente definição

-- Drop table
-- DROP TABLE alternativa.dim_cliente;

CREATE TABLE alternativa.dim_cliente (
	sk_id_cliente serial primary key,
	id_cliente int4 NULL,
	nome varchar(100) NOT NULL,
	tipo_cliente varchar(20) NULL,
	cidade varchar(50) NULL,
	inicio_validade timestamp DEFAULT now() NOT NULL,
	fim_validade timestamp NULL,
	CONSTRAINT dim_cliente_tipo_cliente_check CHECK (((tipo_cliente)::text = ANY ((ARRAY['PJ'::character varying, 'PF'::character varying])::text[])))
);





-- alternativa.dim_frota definição

-- Drop table

-- DROP TABLE alternativa.dim_frota;

CREATE TABLE alternativa.dim_frota (
	sk_id_caminhao serial4 NOT NULL,
	id_caminhao int4 NULL,
	placa varchar(50) NULL,
	tipo_modelo varchar(50) NULL,
	capacidade int4 NULL,
	inicio_validade timestamp DEFAULT now() NOT NULL,
	fim_validade timestamp NULL,
	CONSTRAINT dim_frota_pkey PRIMARY KEY (sk_id_caminhao)
);


-- alternativa.dim_residuo definição

-- Drop table

-- DROP TABLE alternativa.dim_residuo;

CREATE TABLE alternativa.dim_residuo (
	sk_id_residuo serial4 NOT NULL,
	id_residuo int4 NULL,
	tipo_residuo varchar(50) NULL,
	tratamento varchar(50) NULL,
	inicio_validade timestamp DEFAULT now() NOT NULL,
	fim_validade timestamp NULL,
	CONSTRAINT dim_residuo_pkey PRIMARY KEY (sk_id_residuo)
);