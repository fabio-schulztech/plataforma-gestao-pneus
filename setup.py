#!/usr/bin/env python3
"""
Script de configuração para a Plataforma de Gestão de Pneus
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ é necessário. Versão atual:", sys.version)
        return False
    print("✅ Python", sys.version.split()[0], "detectado")
    return True

def install_requirements():
    """Instala as dependências do requirements.txt"""
    try:
        print("📦 Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    try:
        print("🔌 Testando conexão com o banco de dados...")
        from db.connection import create_db_connection
        connection = create_db_connection()
        if connection and connection.is_connected():
            print("✅ Conexão com banco de dados estabelecida")
            connection.close()
            return True
        else:
            print("❌ Falha na conexão com banco de dados")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")
        return False

def create_database_tables():
    """Cria as tabelas necessárias no banco de dados"""
    try:
        print("🗄️ Criando tabelas no banco de dados...")
        from db.connection import create_db_connection
        connection = create_db_connection()
        
        if not connection:
            print("❌ Não foi possível conectar ao banco")
            return False
            
        cursor = connection.cursor()
        
        # Scripts SQL para criar as tabelas
        sql_scripts = [
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id VARCHAR(255) PRIMARY KEY,
                placa VARCHAR(20) NOT NULL,
                modelo VARCHAR(100),
                ano INT,
                eixos INT,
                cliente_id VARCHAR(255) NOT NULL DEFAULT 'default_client',
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tires (
                id VARCHAR(255) PRIMARY KEY,
                numeroFogo VARCHAR(50) NOT NULL,
                marca VARCHAR(100),
                modelo VARCHAR(100),
                tipoPneu VARCHAR(50),
                medida VARCHAR(50),
                capacidadeCarga VARCHAR(50),
                desenhoBanda VARCHAR(100),
                profundidadeSulcoInicial DECIMAL(5,2),
                custoAquisicao DECIMAL(10,2),
                dataAquisicao DATE,
                fornecedor VARCHAR(100),
                numeroNF VARCHAR(50),
                statusInicial VARCHAR(50),
                numeroRecapagens INT DEFAULT 0,
                quilometragemTotalPercorrida DECIMAL(10,2) DEFAULT 0,
                ultimaLeituraHodometroRegistrada DECIMAL(10,2) DEFAULT 0,
                profundidadeSulcoAtual DECIMAL(5,2),
                currentVehicleId VARCHAR(255),
                currentVehiclePlaca VARCHAR(20),
                currentAxle VARCHAR(50),
                currentPosition VARCHAR(50),
                cliente_id VARCHAR(255) NOT NULL DEFAULT 'default_client',
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (currentVehicleId) REFERENCES vehicles(id) ON DELETE SET NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tire_events (
                id VARCHAR(255) PRIMARY KEY,
                tireId VARCHAR(255) NOT NULL,
                tipo VARCHAR(100) NOT NULL,
                data DATE NOT NULL,
                observacoes TEXT,
                detalhes JSON,
                cliente_id VARCHAR(255) NOT NULL DEFAULT 'default_client',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tireId) REFERENCES tires(id) ON DELETE CASCADE
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_tires_cliente_id ON tires(cliente_id);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_vehicles_cliente_id ON vehicles(cliente_id);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_tire_events_cliente_id ON tire_events(cliente_id);
            """
        ]
        
        for script in sql_scripts:
            cursor.execute(script)
        
        connection.commit()
        print("✅ Tabelas criadas com sucesso")
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def run_tests():
    """Executa os testes da aplicação"""
    try:
        print("🧪 Executando testes...")
        result = subprocess.run([sys.executable, "test_multi_tenancy.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Testes executados com sucesso")
            print(result.stdout)
            return True
        else:
            print("❌ Alguns testes falharam")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def main():
    """Função principal do setup"""
    print("🚀 Configurando Plataforma de Gestão de Pneus")
    print("=" * 50)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependências
    if not install_requirements():
        sys.exit(1)
    
    # Testar conexão com banco
    if not test_database_connection():
        print("⚠️  Configure as credenciais do banco em db/connection.py")
        sys.exit(1)
    
    # Criar tabelas
    if not create_database_tables():
        sys.exit(1)
    
    # Executar testes
    if not run_tests():
        print("⚠️  Alguns testes falharam, mas a instalação foi concluída")
    
    print("\n" + "=" * 50)
    print("✅ Configuração concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure a tag 'Cliente' no dashboard da TagoIO")
    print("2. Execute: python app.py")
    print("3. Acesse: http://localhost:7766")
    print("\n📖 Consulte o README.md para mais informações")

if __name__ == "__main__":
    main()
