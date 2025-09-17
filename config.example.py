# Configuração de exemplo para a Plataforma de Gestão de Pneus
# Copie este arquivo para config.py e ajuste as configurações

# Configurações do Banco de Dados
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sua_senha_aqui',
    'database': 'tire_management_db',
    'port': 3306
}

# Configurações da Aplicação Flask
FLASK_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': 7766,
    'secret_key': 'sua_chave_secreta_aqui'
}

# Configurações da TagoIO
TAGOIO_CONFIG = {
    'profile_token': 'seu_token_aqui',
    'base_url': 'https://api.tago.io'
}

# Configurações de CORS
CORS_CONFIG = {
    'origins': ['*'],  # Em produção, especifique os domínios permitidos
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization']
}

# Configurações de Log
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'app.log'
}
