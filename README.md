# Plataforma de Gestão de Pneus

Sistema completo de gestão de frota de pneus com funcionalidade de multi-tenancy, desenvolvido para integração com TagoIO.

## 🚀 Funcionalidades

### Gestão de Pneus
- ✅ Cadastro completo de pneus com especificações técnicas
- ✅ Controle de quilometragem e desgaste
- ✅ Histórico completo de eventos
- ✅ Sistema de permuta entre pneus
- ✅ Controle de recapagens

### Gestão de Veículos
- ✅ Cadastro de veículos da frota
- ✅ Controle de eixos e posições
- ✅ Rastreamento de pneus por veículo

### Sistema de Eventos
- ✅ Montagem/remoção de pneus
- ✅ Envio para recapagem
- ✅ Registro de quilometragem
- ✅ Rodízio e permuta
- ✅ Descarte de pneus

### Multi-tenancy
- ✅ Isolamento completo de dados por cliente
- ✅ Integração com tags da TagoIO
- ✅ Filtragem automática por cliente

## 🛠️ Tecnologias

### Backend
- **Python 3.x**
- **Flask** - Framework web
- **MySQL** - Banco de dados
- **Flask-CORS** - Cross-origin requests

### Frontend
- **HTML5/CSS3/JavaScript**
- **Tailwind CSS** - Framework CSS
- **TagoIO Widget** - Integração com dashboard

## 📋 Pré-requisitos

- Python 3.7+
- MySQL 5.7+
- Navegador web moderno

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/plataforma-gestao-pneus.git
cd plataforma-gestao-pneus
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados
```sql
-- Execute os scripts SQL para criar as tabelas
-- Adicione o campo cliente_id nas tabelas existentes
ALTER TABLE tires ADD COLUMN cliente_id VARCHAR(255) NOT NULL DEFAULT 'default_client';
ALTER TABLE vehicles ADD COLUMN cliente_id VARCHAR(255) NOT NULL DEFAULT 'default_client';
ALTER TABLE tire_events ADD COLUMN cliente_id VARCHAR(255) NOT NULL DEFAULT 'default_client';
```

### 4. Configure as variáveis de ambiente
```bash
# Edite db/connection.py com suas credenciais do MySQL
host = "seu-host"
user = "seu-usuario"
password = "sua-senha"
database = "tire_management_db"
```

### 5. Execute a aplicação
```bash
python app.py
```

## 📖 Como Usar

### Configuração da TagoIO

1. **Crie um dashboard** na TagoIO
2. **Adicione a tag "Cliente"** ao dashboard
3. **Configure o widget** para usar o arquivo `index_client.html`
4. **Defina o valor da tag** para o cliente desejado

### Uso da Plataforma

1. **Acesse o dashboard** na TagoIO
2. **O sistema detectará automaticamente** o cliente pela tag
3. **Gerencie pneus, veículos e eventos** normalmente
4. **Todos os dados ficam isolados** por cliente

## 🔧 API Endpoints

### Pneus
- `GET /api/tires?cliente_id={id}` - Listar pneus
- `POST /api/tires?cliente_id={id}` - Criar pneu
- `PUT /api/tires/{id}?cliente_id={id}` - Atualizar pneu
- `DELETE /api/tires/{id}?cliente_id={id}` - Excluir pneu

### Veículos
- `GET /api/vehicles?cliente_id={id}` - Listar veículos
- `POST /api/vehicles?cliente_id={id}` - Criar veículo
- `PUT /api/vehicles/{id}?cliente_id={id}` - Atualizar veículo
- `DELETE /api/vehicles/{id}?cliente_id={id}` - Excluir veículo

### Eventos
- `GET /api/events?cliente_id={id}` - Listar eventos
- `POST /api/events?cliente_id={id}` - Criar evento
- `DELETE /api/events/{id}?cliente_id={id}` - Excluir evento

### Permuta
- `POST /api/swap-tires?cliente_id={id}` - Permutar pneus

## 🧪 Testes

Execute o script de teste para verificar a funcionalidade:

```bash
python test_multi_tenancy.py
```

## 📁 Estrutura do Projeto

```
plataforma-gestao-pneus/
├── app.py                          # Aplicação Flask principal
├── requirements.txt                # Dependências Python
├── index_client.html              # Interface frontend
├── controllers/                   # Controladores da API
│   ├── tire_controller.py
│   ├── vehicle_controller.py
│   └── event_controller.py
├── db/                           # Configuração do banco
│   └── connection.py
├── test_multi_tenancy.py         # Script de testes
├── CHANGELOG_MULTI_TENANCY.md    # Log de mudanças
└── README.md                     # Este arquivo
```

## 🔒 Segurança

- **Isolamento de dados** por cliente
- **Validação de cliente_id** em todas as operações
- **Prevenção de vazamento** de dados entre clientes
- **Sanitização de inputs** SQL

## 📊 Funcionalidades Avançadas

### Controle de Ciclo de Vida
- Pneu novo → Em Estoque → Em Uso → Recapagem → Em Uso → Descarte
- Rastreamento completo de cada transição

### Relatórios e KPIs
- Quilometragem por pneu
- Número de recapagens
- Status atual da frota
- Histórico de eventos

### Integração TagoIO
- Detecção automática de cliente
- Interface responsiva
- Notificações em tempo real

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato via email: suporte@exemplo.com

## 🎯 Roadmap

- [ ] Relatórios avançados
- [ ] Notificações push
- [ ] API de integração
- [ ] App mobile
- [ ] Dashboard de analytics

---

**Desenvolvido com ❤️ para gestão eficiente de frotas**
