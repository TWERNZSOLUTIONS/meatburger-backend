-- =============================
-- 🧩 Atualização da tabela site_settings
-- =============================

-- Se a tabela não existir, cria
CREATE TABLE IF NOT EXISTS site_settings (
    id SERIAL PRIMARY KEY,
    open_time TIME NULL,
    close_time TIME NULL,
    working_days JSON DEFAULT '[]',
    is_open BOOLEAN DEFAULT TRUE,
    notice_message VARCHAR NULL,
    instagram_link VARCHAR NULL,
    whatsapp_link VARCHAR NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ajustes de colunas existentes (para sincronizar sem recriar a tabela)
ALTER TABLE site_settings
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

-- Garante que colunas novas existam
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='site_settings' AND column_name='working_days') THEN
        ALTER TABLE site_settings ADD COLUMN working_days JSON DEFAULT '[]';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='site_settings' AND column_name='instagram_link') THEN
        ALTER TABLE site_settings ADD COLUMN instagram_link VARCHAR;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='site_settings' AND column_name='whatsapp_link') THEN
        ALTER TABLE site_settings ADD COLUMN whatsapp_link VARCHAR;
    END IF;
END $$;


-- =============================
-- 🧩 Atualização da tabela products
-- =============================

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    image_url VARCHAR,
    category VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE products
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='products' AND column_name='category') THEN
        ALTER TABLE products ADD COLUMN category VARCHAR;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='products' AND column_name='is_active') THEN
        ALTER TABLE products ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
    END IF;
END $$;
