-- Crear la tabla de hechos particionada
CREATE TABLE fact_user_usage (
    fact_id SERIAL,
    user_id INT NOT NULL,
    plan_name VARCHAR(50) NOT NULL,
    date_id DATE NOT NULL,
    total_minutes_used NUMERIC(10, 2) DEFAULT 0,
    total_messages_sent INT DEFAULT 0,
    total_mb_used NUMERIC(15, 2) DEFAULT 0,
    total_revenue NUMERIC(10, 2) DEFAULT 0,
    PRIMARY KEY (fact_id, date_id) -- Es necesario incluir la clave de partición en la PK
) PARTITION BY RANGE (date_id);

-- Crear las particiones específicas para Enero y Febrero de 2025
CREATE TABLE fact_user_usage_2025_01 PARTITION OF fact_user_usage
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE fact_user_usage_2025_02 PARTITION OF fact_user_usage
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');