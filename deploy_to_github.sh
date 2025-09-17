#!/bin/bash

# Script para fazer deploy do projeto para o GitHub
# Execute: chmod +x deploy_to_github.sh && ./deploy_to_github.sh

echo "🚀 Iniciando deploy para GitHub..."

# Nome do repositório
REPO_NAME="plataforma-gestao-pneus"
GITHUB_USERNAME="seu-usuario"  # Substitua pelo seu username do GitHub

# Verificar se o Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não está instalado. Instale o Git primeiro."
    exit 1
fi

# Verificar se estamos em um repositório Git
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
fi

# Adicionar todos os arquivos
echo "📦 Adicionando arquivos ao Git..."
git add .

# Fazer commit inicial
echo "💾 Fazendo commit inicial..."
git commit -m "🎉 Initial commit: Plataforma de Gestão de Pneus

✨ Funcionalidades implementadas:
- Sistema completo de gestão de pneus
- Multi-tenancy com isolamento por cliente
- Integração com TagoIO
- API REST completa
- Interface web responsiva
- Controle de ciclo de vida dos pneus
- Sistema de eventos e histórico
- Permuta de pneus
- Relatórios e KPIs

🛠️ Tecnologias:
- Backend: Python Flask + MySQL
- Frontend: HTML5/CSS3/JavaScript + Tailwind CSS
- Integração: TagoIO Widget

📋 Próximos passos:
1. Configure o banco de dados
2. Execute: python setup.py
3. Configure a TagoIO
4. Execute: python app.py"

# Adicionar remote do GitHub (substitua pelo seu username)
echo "🔗 Configurando remote do GitHub..."
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# Verificar se o remote foi adicionado
if git remote -v | grep -q "origin"; then
    echo "✅ Remote origin configurado"
else
    echo "❌ Erro ao configurar remote. Verifique o nome do usuário e repositório."
    exit 1
fi

# Fazer push para o GitHub
echo "📤 Fazendo push para o GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deploy concluído com sucesso!"
    echo ""
    echo "📋 Informações do repositório:"
    echo "   URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "   Branch: main"
    echo ""
    echo "📖 Próximos passos:"
    echo "1. Acesse o repositório no GitHub"
    echo "2. Configure as secrets/secrets do repositório se necessário"
    echo "3. Configure o banco de dados em produção"
    echo "4. Execute: python setup.py"
    echo "5. Configure a TagoIO com o arquivo index_client.html"
    echo ""
    echo "🔧 Para futuras atualizações:"
    echo "   git add ."
    echo "   git commit -m 'Descrição da mudança'"
    echo "   git push origin main"
else
    echo "❌ Erro ao fazer push para o GitHub"
    echo "Verifique suas credenciais e permissões do repositório"
    exit 1
fi
