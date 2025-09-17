#!/usr/bin/env python3
"""
Script de teste para verificar a funcionalidade de multi-tenancy
"""

import requests
import json

# Configuração
BASE_URL = "https://api.schulztech.com.br/pneus/api"
CLIENTE_A = "cliente_teste_a"
CLIENTE_B = "cliente_teste_b"

def test_client_isolation():
    """Testa se os clientes estão isolados"""
    print("🧪 Testando isolamento entre clientes...")
    
    # Teste 1: Buscar pneus do cliente A
    print("1. Buscando pneus do cliente A...")
    try:
        response_a = requests.get(f"{BASE_URL}/tires?cliente_id={CLIENTE_A}")
        print(f"   Status: {response_a.status_code}")
        if response_a.status_code == 200:
            tires_a = response_a.json()
            print(f"   Pneus encontrados: {len(tires_a)}")
        else:
            print(f"   Erro: {response_a.text}")
    except Exception as e:
        print(f"   Erro na requisição: {e}")
    
    # Teste 2: Buscar pneus do cliente B
    print("2. Buscando pneus do cliente B...")
    try:
        response_b = requests.get(f"{BASE_URL}/tires?cliente_id={CLIENTE_B}")
        print(f"   Status: {response_b.status_code}")
        if response_b.status_code == 200:
            tires_b = response_b.json()
            print(f"   Pneus encontrados: {len(tires_b)}")
        else:
            print(f"   Erro: {response_b.text}")
    except Exception as e:
        print(f"   Erro na requisição: {e}")
    
    # Teste 3: Tentar acessar sem cliente_id
    print("3. Testando requisição sem cliente_id...")
    try:
        response_no_client = requests.get(f"{BASE_URL}/tires")
        print(f"   Status: {response_no_client.status_code}")
        if response_no_client.status_code == 400:
            print("   ✅ Validação funcionando - cliente_id obrigatório")
        else:
            print(f"   ❌ Erro: Deveria retornar 400, mas retornou {response_no_client.status_code}")
    except Exception as e:
        print(f"   Erro na requisição: {e}")

def test_create_tire():
    """Testa criação de pneu com cliente_id"""
    print("\n🧪 Testando criação de pneu...")
    
    import time
    unique_id = f"test_tire_{int(time.time())}"
    
    tire_data = {
        "id": unique_id,
        "numeroFogo": f"TEST{int(time.time())}",
        "marca": "Teste",
        "modelo": "Teste Model",
        "medida": "295/80R22.5",
        "custoAquisicao": 1000.00,
        "dataAquisicao": "2024-01-01",
        "fornecedor": "Fornecedor Teste",
        "statusInicial": "Em Estoque"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tires?cliente_id={CLIENTE_A}",
            json=tire_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Pneu criado com sucesso")
            
            # Verificar se o pneu foi criado para o cliente correto
            print("   Verificando se pneu pertence ao cliente correto...")
            check_response = requests.get(f"{BASE_URL}/tires?cliente_id={CLIENTE_A}")
            if check_response.status_code == 200:
                tires = check_response.json()
                tire_found = any(tire['id'] == unique_id for tire in tires)
                if tire_found:
                    print("   ✅ Pneu encontrado na lista do cliente A")
                else:
                    print("   ❌ Pneu não encontrado na lista do cliente A")
            
            # Verificar se pneu NÃO aparece para outro cliente
            print("   Verificando isolamento com cliente B...")
            check_response_b = requests.get(f"{BASE_URL}/tires?cliente_id={CLIENTE_B}")
            if check_response_b.status_code == 200:
                tires_b = check_response_b.json()
                tire_found_b = any(tire['id'] == unique_id for tire in tires_b)
                if not tire_found_b:
                    print("   ✅ Pneu NÃO aparece para cliente B (isolamento funcionando)")
                else:
                    print("   ❌ ERRO: Pneu aparece para cliente B (falha de isolamento)")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"   Erro na requisição: {e}")

def test_vehicles():
    """Testa operações com veículos"""
    print("\n🧪 Testando operações com veículos...")
    
    # Buscar veículos do cliente A
    try:
        response = requests.get(f"{BASE_URL}/vehicles?cliente_id={CLIENTE_A}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            vehicles = response.json()
            print(f"   Veículos encontrados: {len(vehicles)}")
        else:
            print(f"   Erro: {response.text}")
    except Exception as e:
        print(f"   Erro na requisição: {e}")

def test_events():
    """Testa operações com eventos"""
    print("\n🧪 Testando operações com eventos...")
    
    # Buscar eventos do cliente A
    try:
        response = requests.get(f"{BASE_URL}/events?cliente_id={CLIENTE_A}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"   Eventos encontrados: {len(events)}")
        else:
            print(f"   Erro: {response.text}")
    except Exception as e:
        print(f"   Erro na requisição: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando testes de multi-tenancy...")
    print(f"URL Base: {BASE_URL}")
    print(f"Cliente A: {CLIENTE_A}")
    print(f"Cliente B: {CLIENTE_B}")
    print("=" * 50)
    
    test_client_isolation()
    test_create_tire()
    test_vehicles()
    test_events()
    
    print("\n✅ Testes concluídos!")
