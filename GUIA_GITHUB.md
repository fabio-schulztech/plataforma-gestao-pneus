# 🚀 Guia para Criar Repositório no GitHub

## Passo a Passo Completo

### 1. **Criar Repositório no GitHub**

1. **Acesse o GitHub:**
   - Vá para https://github.com
   - Faça login na sua conta

2. **Criar novo repositório:**
   - Clique no botão **"New"** ou **"+"** no canto superior direito
   - Ou acesse diretamente: https://github.com/new

3. **Configurar o repositório:**
   ```
   Repository name: plataforma-gestao-pneus
   Description: Sistema completo de gestão de frota de pneus com multi-tenancy
   Visibility: Public (ou Private, sua escolha)
   ✅ Initialize this repository with: NENHUM (deixe vazio)
   ```

4. **Clique em "Create repository"**

### 2. **Conectar Repositório Local ao GitHub**

Execute os comandos abaixo no terminal (já estamos no diretório correto):

```bash
# Adicionar remote do GitHub (substitua SEU-USUARIO pelo seu username)
git remote add origin https://github.com/SEU-USUARIO/plataforma-gestao-pneus.git

# Verificar se foi adicionado corretamente
git remote -v

# Fazer push para o GitHub
git branch -M main
git push -u origin main
```

### 3. **Verificar se Funcionou**

1. **Acesse seu repositório:**
   - Vá para https://github.com/SEU-USUARIO/plataforma-gestao-pneus

2. **Verifique se todos os arquivos estão lá:**
   - README.md
   - app.py
   - controllers/
   - index_client.html
   - etc.

### 4. **Configurações Adicionais (Opcional)**

#### **Configurar GitHub Pages (para hospedar o frontend):**
1. Vá em **Settings** do repositório
2. Role até **Pages**
3. Em **Source**, selecione **Deploy from a branch**
4. Selecione **main** branch
5. Clique **Save**

#### **Configurar Secrets (para variáveis sensíveis):**
1. Vá em **Settings** do repositório
2. Role até **Secrets and variables** > **Actions**
3. Adicione secrets como:
   - `DATABASE_PASSWORD`
   - `FLASK_SECRET_KEY`
   - `TAGOIO_TOKEN`

## 🔧 Comandos Rápidos

Se você quiser executar tudo de uma vez:

```bash
# Substitua SEU-USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU-USUARIO/plataforma-gestao-pneus.git
git branch -M main
git push -u origin main
```

## 📋 Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Nome: `plataforma-gestao-pneus`
- [ ] Descrição adicionada
- [ ] Repositório conectado localmente
- [ ] Push realizado com sucesso
- [ ] Todos os arquivos visíveis no GitHub
- [ ] README.md exibindo corretamente

## 🎯 Próximos Passos

Após criar o repositório:

1. **Configure o banco de dados:**
   ```bash
   python setup.py
   ```

2. **Teste a aplicação:**
   ```bash
   python app.py
   ```

3. **Configure a TagoIO:**
   - Use o arquivo `index_client.html`
   - Configure a tag "Cliente"

4. **Para futuras atualizações:**
   ```bash
   git add .
   git commit -m "Descrição da mudança"
   git push origin main
   ```

## 🆘 Problemas Comuns

### **Erro: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/SEU-USUARIO/plataforma-gestao-pneus.git
```

### **Erro: "Authentication failed"**
- Verifique se você está logado no GitHub
- Use token de acesso pessoal se necessário

### **Erro: "Repository not found"**
- Verifique se o nome do repositório está correto
- Verifique se você tem permissão para acessar o repositório

---

**Boa sorte! 🚀**
