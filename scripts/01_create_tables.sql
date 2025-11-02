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

-- alternativa.fato_servico definição

-- Drop table

-- DROP TABLE alternativa.fato_servico;

CREATE TABLE alternativa.fato_servico (
	id_servico text NOT NULL,
	id_cliente int4 NULL,
	id_caminhao int4 NULL,
	id_residuo int4 NULL,
	id_motorista int4 NULL,
	data_solicitacao date NULL,
	tempo_resposta_horas numeric(5, 2) NULL,
	tempo_permanencia_dias numeric(5, 2) NULL,
	peso_residuos_kg numeric NULL,
	km_percorridos int4 NULL,
	taxa_ocupacao_percent numeric(5, 2) NULL,
	CONSTRAINT fato_servico_pkey PRIMARY KEY (id_servico)
);


-- alternativa.dim_funcionario definição

-- Drop table

-- DROP TABLE alternativa.dim_funcionario;

CREATE TABLE alternativa.dim_funcionario (
	sk_id_funcionario serial4 NOT NULL,
	id_funcionario int4 NULL,
	nome varchar(50) NULL,
	cargo varchar(50) NULL,
	inicio_validade timestamp DEFAULT now() NOT NULL,
	fim_validade timestamp NULL,
	CONSTRAINT dim_funcionario_pkey PRIMARY KEY (sk_id_funcionario)
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