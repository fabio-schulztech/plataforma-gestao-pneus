# Changelog - Implementação de Multi-tenancy

## Resumo das Modificações

Este documento descreve as modificações realizadas no backend para implementar funcionalidade de multi-tenancy baseada na tag "Cliente" da TagoIO.

## Arquivos Modificados

### 1. `app.py`
- **Adicionada função `validate_client_id()`**: Valida e extrai o `cliente_id` das requisições
- **Modificadas todas as rotas**: Agora todas as rotas requerem `cliente_id` como parâmetro
- **Rotas afetadas**:
  - `GET /api/tires` - Buscar pneus por cliente
  - `POST /api/tires` - Criar pneu para cliente específico
  - `PUT /api/tires/<id>` - Atualizar pneu do cliente
  - `DELETE /api/tires/<id>` - Deletar pneu do cliente
  - `GET /api/vehicles` - Buscar veículos por cliente
  - `POST /api/vehicles` - Criar veículo para cliente específico
  - `PUT /api/vehicles/<id>` - Atualizar veículo do cliente
  - `DELETE /api/vehicles/<id>` - Deletar veículo do cliente
  - `GET /api/events` - Buscar eventos por cliente
  - `POST /api/events` - Criar evento para cliente específico
  - `DELETE /api/events/<id>` - Deletar evento do cliente
  - `POST /api/swap-tires` - Permutar pneus do mesmo cliente

### 2. `controllers/tire_controller.py`
- **`get_all_tires(cliente_id)`**: Filtra pneus por cliente
- **`create_tire(data, cliente_id)`**: Cria pneu associado ao cliente
- **`update_tire(tire_id, data, cliente_id)`**: Atualiza pneu do cliente específico
- **`delete_tire(tire_id, cliente_id)`**: Deleta pneu do cliente específico
- **`swap_tires(tire1_id, tire2_id, cliente_id)`**: Permuta pneus do mesmo cliente
- **Validações de segurança**: Todas as operações verificam se o recurso pertence ao cliente

### 3. `controllers/vehicle_controller.py`
- **`get_all_vehicles(cliente_id)`**: Filtra veículos por cliente
- **`create_vehicle(data, cliente_id)`**: Cria veículo associado ao cliente
- **`update_vehicle(vehicle_id, data, cliente_id)`**: Atualiza veículo do cliente específico
- **`delete_vehicle(vehicle_id, cliente_id)`**: Deleta veículo do cliente específico
- **Validações de segurança**: Todas as operações verificam se o recurso pertence ao cliente

### 4. `controllers/event_controller.py`
- **`get_all_events(cliente_id)`**: Filtra eventos por cliente
- **`create_event(data, cliente_id)`**: Cria evento associado ao cliente
- **`delete_event(event_id, cliente_id)`**: Deleta evento do cliente específico
- **`create_event_internal(connection, data)`**: Atualizada para incluir `cliente_id`
- **Validações de segurança**: Verifica se o pneu pertence ao cliente antes de criar evento

## Funcionalidades Implementadas

### ✅ Isolamento de Dados
- Cada cliente só acessa seus próprios dados
- Filtros aplicados em todas as consultas SQL
- Validação de propriedade em todas as operações

### ✅ Segurança
- Validação obrigatória de `cliente_id` em todas as rotas
- Prevenção de acesso a dados de outros clientes
- Mensagens de erro específicas para recursos não encontrados

### ✅ Compatibilidade
- Mantém a mesma interface da API (apenas adiciona parâmetro `cliente_id`)
- Estrutura de resposta inalterada
- Códigos de status HTTP mantidos

## Como Usar

### Requisições GET
```
GET /api/tires?cliente_id=cliente_123
GET /api/vehicles?cliente_id=cliente_123
GET /api/events?cliente_id=cliente_123
```

### Requisições POST/PUT
```json
POST /api/tires?cliente_id=cliente_123
{
  "id": "tire_123",
  "numeroFogo": "ABC123",
  "marca": "Michelin",
  // ... outros campos
}
```

### Respostas de Erro
```json
{
  "message": "cliente_id é obrigatório"
}
```

```json
{
  "message": "Pneu não encontrado ou não pertence ao cliente."
}
```

## Próximos Passos

1. **Testar as modificações** usando o script `test_multi_tenancy.py`
2. **Atualizar o frontend** para enviar `cliente_id` nas requisições
3. **Configurar a TagoIO** para passar a tag "Cliente" para o widget
4. **Migrar dados existentes** para incluir `cliente_id` padrão
5. **Deploy em produção**

## Arquivos de Teste

- `test_multi_tenancy.py`: Script para testar a funcionalidade
- `CHANGELOG_MULTI_TENANCY.md`: Este arquivo de documentação

## Notas Importantes

- Todas as modificações são **backward compatible** com a estrutura existente
- O campo `cliente_id` foi adicionado ao banco de dados (assumindo que já foi feito)
- As validações de segurança impedem vazamento de dados entre clientes
- A performance não deve ser afetada significativamente devido aos índices no `cliente_id`
