-- =====================================================
-- MODELO DE BI BASEADO EM INDICADORES EMPRESARIAIS
-- =====================================================

-- =========================
-- TABELAS DIMENSÃO
-- =========================

CREATE TABLE dim_tempo (
    id_tempo SERIAL PRIMARY KEY,
    mes VARCHAR(7) NOT NULL, -- Ex: '2024-01'
    ano INT NOT NULL,
    trimestre INT CHECK (trimestre BETWEEN 1 AND 4)
);

COMMENT ON TABLE dim_tempo IS 'Dimensão temporal - meses, anos e trimestres.';


CREATE TABLE dim_cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo_cliente VARCHAR(20) CHECK (tipo_cliente IN ('PJ', 'PF')),
    cidade VARCHAR(50),
    segmento VARCHAR(50)
);

COMMENT ON TABLE dim_cliente IS 'Dimensão de clientes - identifica o perfil e tipo de cliente.';


CREATE TABLE dim_funcionario (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    setor VARCHAR(50)
);

COMMENT ON TABLE dim_funcionario IS 'Dimensão de funcionários - identifica colaboradores envolvidos nas operações.';


CREATE TABLE dim_frota (
    id_frota SERIAL PRIMARY KEY,
    placa VARCHAR(10) UNIQUE NOT NULL,
    tipo_veiculo VARCHAR(50),
    capacidade_m3 DECIMAL(10,2)
);

COMMENT ON TABLE dim_frota IS 'Dimensão de frota - dados sobre veículos utilizados nas coletas.';


CREATE TABLE dim_residuo (
    id_residuo SERIAL PRIMARY KEY,
    tipo_residuo VARCHAR(50),
    categoria VARCHAR(50),
    tratamento VARCHAR(50)
);

COMMENT ON TABLE dim_residuo IS 'Dimensão de resíduos - tipos e categorias de resíduos coletados.';


-- =========================
-- TABELA FATO
-- =========================

CREATE TABLE fato_indicadores (
    id_indicador SERIAL PRIMARY KEY,
    id_tempo INT REFERENCES dim_tempo(id_tempo),
    id_cliente INT REFERENCES dim_cliente(id_cliente),
    id_funcionario INT REFERENCES dim_funcionario(id_funcionario),
    id_frota INT REFERENCES dim_frota(id_frota),
    id_residuo INT REFERENCES dim_residuo(id_residuo),

    tempo_medio_coleta_h DECIMAL(10,2),
    custo_medio_viagem DECIMAL(12,2),
    taxa_ocupacao_cacambas DECIMAL(5,2),
    volume_total_entulho_m3 DECIMAL(12,2),
    receita_mensal DECIMAL(14,2),
    lucro_liquido DECIMAL(14,2)
);

COMMENT ON TABLE fato_indicadores IS 'Tabela fato contendo métricas mensais de desempenho operacional e financeiro.';


-- =========================
-- ÍNDICES PARA PERFORMANCE
-- =========================

CREATE INDEX idx_fato_tempo ON fato_indicadores(id_tempo);
CREATE INDEX idx_fato_cliente ON fato_indicadores(id_cliente);
CREATE INDEX idx_fato_funcionario ON fato_indicadores(id_funcionario);
CREATE INDEX idx_fato_frota ON fato_indicadores(id_frota);
CREATE INDEX idx_fato_residuo ON fato_indicadores(id_residuo);