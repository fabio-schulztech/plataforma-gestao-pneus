
# Guia de Deploy - Plataforma de Gestão de Pneus

## 🚀 Deploy para GitHub

### Opção 1: Script Automático (Recomendado)

1. **Configure o script de deploy:**
   ```bash
   # Edite o arquivo deploy_to_github.sh
   # Substitua "seu-usuario" pelo seu username do GitHub
   GITHUB_USERNAME="seu-usuario"
   ```

2. **Execute o script:**
   ```bash
   chmod +x deploy_to_github.sh
   ./deploy_to_github.sh
   ```

### Opção 2: Deploy Manual

1. **Crie o repositório no GitHub:**
   - Acesse https://github.com/new
   - Nome: `plataforma-gestao-pneus`
   - Descrição: `Sistema completo de gestão de frota de pneus com multi-tenancy`
   - Público ou Privado (sua escolha)
   - **NÃO** inicialize com README, .gitignore ou LICENSE

2. **Inicialize o Git localmente:**
   ```bash
   git init
   git add .
   git commit -m "🎉 Initial commit: Plataforma de Gestão de Pneus"
   ```

3. **Conecte com o GitHub:**
   ```bash
   git remote add origin https://github.com/SEU-USUARIO/plataforma-gestao-pneus.git
   git branch -M main
   git push -u origin main
   ```

## 🔧 Configuração Pós-Deploy

### 1. Configurar o Banco de Dados

1. **Crie o banco de dados MySQL:**
   ```sql
   CREATE DATABASE tire_management_db;
   ```

2. **Configure as credenciais:**
   - Edite `db/connection.py`
   - Ajuste host, user, password e database

3. **Execute o setup:**
   ```bash
   python setup.py
   ```

### 2. Configurar a TagoIO

1. **Acesse sua conta TagoIO**
2. **Crie um novo dashboard**
3. **Adicione a tag "Cliente"** com o valor desejado
4. **Configure o widget customizado:**
   - URL: `https://seu-dominio.com/index_client.html`
   - Ou hospede o arquivo na TagoIO

### 3. Deploy em Produção

#### Opção A: Servidor Próprio

1. **Configure o servidor:**
   ```bash
   # Instale dependências
   pip install -r requirements.txt
   
   # Configure o banco
   python setup.py
   
   # Execute com Gunicorn
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:7766 app:app
   ```

2. **Configure proxy reverso (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name seu-dominio.com;
       
       location / {
           proxy_pass http://127.0.0.1:7766;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

#### Opção B: Heroku

1. **Instale Heroku CLI**
2. **Crie Procfile:**
   ```
   web: gunicorn app:app
   ```
3. **Deploy:**
   ```bash
   heroku create plataforma-gestao-pneus
   git push heroku main
   ```

#### Opção C: Docker

1. **Crie Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 7766
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7766", "app:app"]
   ```

2. **Build e execute:**
   ```bash
   docker build -t plataforma-gestao-pneus .
   docker run -p 7766:7766 plataforma-gestao-pneus
   ```

## 📋 Checklist de Deploy

### Antes do Deploy
- [ ] Testes passando (`python test_multi_tenancy.py`)
- [ ] Configurações de banco ajustadas
- [ ] Arquivos sensíveis no .gitignore
- [ ] README.md atualizado
- [ ] Documentação completa

### Após o Deploy
- [ ] Repositório criado no GitHub
- [ ] Código enviado com sucesso
- [ ] Banco de dados configurado
- [ ] TagoIO configurada
- [ ] Testes em produção
- [ ] Monitoramento ativo

## 🔒 Segurança

### Configurações Importantes

1. **Variáveis de Ambiente:**
   ```bash
   export DATABASE_PASSWORD="senha_segura"
   export FLASK_SECRET_KEY="chave_secreta_forte"
   ```

2. **Firewall:**
   - Abra apenas a porta 7766
   - Configure HTTPS se possível

3. **Banco de Dados:**
   - Use senhas fortes
   - Configure backup automático
   - Monitore logs de acesso

## 📊 Monitoramento

### Logs da Aplicação
```bash
# Ver logs em tempo real
tail -f app.log

# Ver logs do sistema
journalctl -u plataforma-gestao-pneus -f
```

### Métricas Importantes
- Uptime da aplicação
- Tempo de resposta da API
- Uso de memória e CPU
- Conexões com banco de dados
- Erros 4xx e 5xx

## 🆘 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco:**
   - Verifique credenciais em `db/connection.py`
   - Teste conexão: `python -c "from db.connection import create_db_connection; print(create_db_connection())"`

2. **Erro 500 na API:**
   - Verifique logs da aplicação
   - Teste endpoints individualmente
   - Verifique se o banco está acessível

3. **TagoIO não carrega:**
   - Verifique se a tag "Cliente" está configurada
   - Teste o arquivo `index_client.html` localmente
   - Verifique CORS no backend

4. **Performance lenta:**
   - Verifique índices do banco
   - Monitore uso de memória
   - Considere cache para consultas frequentes

## 📞 Suporte

Para problemas de deploy:
- Abra uma issue no GitHub
- Consulte os logs da aplicação
- Verifique a documentação da TagoIO
- Entre em contato com o suporte técnico

---

**Boa sorte com seu deploy! 🚀**
