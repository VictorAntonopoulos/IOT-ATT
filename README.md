# Sistema de Triangulação de Motos - IoT Prototype (Sprint 4)

## 📋 Descrição do Projeto
Este projeto apresenta um protótipo funcional de monitoramento inteligente de motos, desenvolvido como parte da Sprint 4 – Disruptive Architectures: IoT, IoB & Generative IA .
A solução simula dispositivos IoT enviando leituras de RFID, GPS e movimento para uma API Flask, que persiste os dados em SQLite e os exibe em um dashboard web em tempo real via Flask-SocketIO.

O sistema entrega um fluxo completo de captura → processamento → visualização, com ênfase em integração, usabilidade e arquitetura escalável.

## 🎯 Problema Resolvido

**Desafio**: Localização precisa e monitoramento em tempo real de motos em pátios da Mottu.
**Solução**: Sistema de triangulação usando múltiplos sensores RFID simulados que coletam dados de intensidade de sinal e enviam para uma API Python, permitindo rastreamento de até 3 dispositivos IoT simultaneamente.

## 🛠 Tecnologias Utilizadas

### Simulação de Hardware:

*   Sensores RFID (simulados via Python)
*   Atuadores simulados (LEDs virtuais ou mensagens de status)
*   3 dispositivos IoT simulados

### Software e Protocolos:

*   Python 3.13
*   Flask / Flask-SocketIO (API e comunicação em tempo real)
*   SQLite (persistência de dados)
*   HTTP/REST API
*   JSON (formato de dados)
*   Dashboard em Flask + HTML/JS
*   API de .NET conectada

### Links:

*   Pitch = https://www.youtube.com/watch?si=OhGFE0eqJH3WFoXn&v=tFLwiapUUiE&feature=youtu.be
*   Demostração = https://www.youtube.com/watch?v=4A9f6w5B5mk

## 🔧 Como Rodar o Projeto

### Clonar o repositório e criar ambiente virtual:

```bash
git clone <[URL_DO_REPO>](https://github.com/VictorAntonopoulos/IOT-ATT )
cd IOT
python -m venv venv
venv\\Scripts\\activate   # Windows
pip install -r requirements.txt
```

### Rodar a API:

```bash
python api.py
```

A API ficará escutando em `http://localhost:5007/api`.

### Rodar os dispositivos simulados (3 sensores/atuadores):

```bash
cd devices
python leitura.py --api-base http://localhost:5007/api --devices 3 --interval 3
```

Cada dispositivo envia leituras de RFID periodicamente para a API.

### Rodar o dashboard para visualização:

```bash
cd ../dashboard
python dashboard_server.py
```

Dashboard acessível em `http://localhost:5008`.
Mostra leituras recentes e status dos dispositivos em tempo real.

## 📊 Dados Enviados para API

Formato JSON:

```json
{
  "rfid": "ECAAAAAAAAAAAAAAAAAAAAAAMOTTU20293",
  "device_id": 1,
  "potencia_sinal": 13
}
```

## 🔄 Funcionamento do Sistema

### Fluxo de operação:

*   Simuladores IoT geram leituras de RFID e intensidade de sinal.
*   Os dados são enviados via HTTP POST à API.
*   API armazena os dados no banco SQLite.
*   O Socket.IO envia as atualizações para o dashboard web.
*   Dashboard consome API via REST + WebSocket e exibe telemetria em tempo real.
*   O dashboard exibe os dados em tempo real, com gráficos e mapa

### Testes Funcionais Simulados:

*   Simulação de perda de sinal e troca de posição.
*   Comunicação de até 3 dispositivos IoT simultaneamente.
*   Validação de latência e atualização em tempo real

## 🏗 Arquitetura do Sistema

`[Dispositivos IoT Simulados] → [API Flask] → [SQLite] → [Dashboard Flask/JS]`

## 📡 Protocolos de Comunicação

### Requisição HTTP

`POST /api/rfid`
`Content-Type: application/json`

```json
{
  "rfid": "string",
  "device_id": number,
  "potencia_sinal": number
}
```

### WebSocket

Dashboard recebe atualizações em tempo real via Flask-SocketIO.

## 📊 Dashboard – Funcionalidades

| **Função** | **Descrição** |
|-------------|----------------|
| **Leituras recentes** | Exibição instantânea das últimas leituras RFID |
| **Mapa interativo** | Localização das motos simuladas com Leaflet |
| **Gráficos** | Frequência e volume de leituras (Chart.js) |
| **Logs** | Histórico de leituras (até 100 mais recentes) |
| **Atualização em tempo real** | Integrado via Flask-SocketIO |





## Informações Adicionais

*   **Desenvolvido para**: DISRUPTIVE ARCHITECTURES: IOT, IOB & GENERATIVE IA
*   **Tecnologias**: Python, Flask, Flask-SocketIO, SQLite, HTTP, JSON
*   **Objetivo**: Protótipo funcional de sistema de triangulação de motos com múltiplos dispositivos IoT simulados

