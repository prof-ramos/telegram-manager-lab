# Telegram Manager - Cyber Management Suite v2.0.0

> Interface CLI production-grade para gerenciar conversas do Telegram com estética cyberpunk/synthwave usando Python Rich.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Telethon](https://img.shields.io/badge/Telethon-1.33.0-blue)
![Rich](https://img.shields.io/badge/Rich-13.7.0-green)

## Requisitos

- Python 3.8+
- Conta Telegram ativa
- API ID e API Hash (obtidos em https://my.telegram.org/apps)

## Instalação

### 1. Clone ou baixe o projeto

```bash
cd telegram-manager-lab
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+5511999999999
```

## Uso

### Executar o programa

```bash
python main.py
```

O programa irá:

1. Conectar à sua conta Telegram
2. Escanear todos os seus diálogos (chats, grupos, canais)
3. Classificar em categorias (usuários, bots, grupos, canais)
4. Exportar os dados em JSON e CSV

### Estrutura de Diretórios

```
telegram-manager-lab/
├── telegram_manager/
│   ├── core/
│   │   ├── client.py        # Gerenciamento do cliente Telegram
│   │   ├── scanner.py       # Lógica de escaneamento
│   │   └── exporter.py      # Exportação de dados (JSON, CSV)
│   ├── ui/
│   │   ├── theme.py         # Paleta Synthwave/Cyberpunk
│   │   └── components.py    # Componentes UI reutilizáveis
│   ├── utils/
│   │   └── config.py        # Gerenciamento de configuração
│   └── __init__.py
├── main.py                   # Ponto de entrada
├── requirements.txt          # Dependências
├── .env.example             # Template de configuração
└── README.md                # Este arquivo
```

## Arquitetura

### Componentes Principais

#### `TelegramConfig` (utils/config.py)
- Carrega e valida configurações do arquivo `.env`
- Garante que todas as credenciais estão presentes
- Cria diretórios de backup automaticamente

#### `TelegramClientManager` (core/client.py)
- Gerencia a conexão com Telegram usando context manager
- Trata exceções (FloodWait, SessionPasswordNeeded)
- Garante desconexão apropriada

#### `TelegramScanner` (core/scanner.py)
- Itera sobre todos os diálogos
- Classifica em User, Bot, Group, Channel
- Extrai metadados (ID, nome, username, contagem de participantes)

#### `DialogExporter` (core/exporter.py)
- Exporta resultados em JSON
- Exporta resultados em CSV
- Cria diretório de exports automaticamente

#### `UIComponents` (ui/components.py)
- Componentes reutilizáveis de UI
- Painéis coloridos com tema Synthwave
- Tabelas formatadas

### Tema Synthwave/Cyberpunk

**Paleta de Cores:**
- 🔴 **Magenta Neon**: `#ff006e` (Primário)
- 🟢 **Ciano Elétrico**: `#06ffa5` (Secundário)
- 🟣 **Roxo Profundo**: `#8338ec` (Acentos)
- ⚫ **Background Escuro**: `#1a1a2e`

## Fluxo de Execução

```
Execução
    ↓
Carregar Configuração (.env)
    ↓
Validar Credenciais
    ↓
Conectar ao Telegram (TelegramClientManager)
    ↓
Escanear Diálogos (TelegramScanner)
    ↓
Classificar Entidades
    ↓
Exportar Dados (DialogExporter)
    ↓
Exibir Estatísticas
    ↓
Desconectar
```

## Tratamento de Erros

### FloodWaitError
O Telegram limita requisições. Se você receber este erro, o programa aguardará automaticamente.

### SessionPasswordNeededError
Se sua conta tem 2FA habilitado, será solicitada a senha durante a autenticação.

### Validação de Configuração
Todas as variáveis de ambiente são validadas antes da conexão.

## Exports

### JSON (`exports/dialogs.json`)

```json
{
  "stats": {
    "total_dialogs": 150,
    "users": 45,
    "bots": 12,
    "groups": 78,
    "channels": 15
  },
  "users": [...],
  "bots": [...],
  "groups": [...],
  "channels": [...]
}
```

### CSV (`exports/dialogs.csv`)

```csv
id,name,type,username,participants_count,is_official
123456789,John Doe,User,john_doe,0,false
987654321,My Group,Chat,,45,false
...
```

## Melhores Práticas Implementadas

✅ **Separação de Responsabilidades**: Cada módulo tem responsabilidade bem definida

✅ **Type Hints**: Uso extensivo de tipos para melhor IDE support

✅ **Context Managers**: Gerenciamento automático de recursos

✅ **Logging Estruturado**: Sistema de logs completo

✅ **Error Handling**: Tratamento robusto de exceções

✅ **Async/Await**: Código assíncrono para melhor performance

✅ **Dataclasses**: Estruturas de dados claras e tipadas

✅ **Configuration Management**: Centralização de configurações

✅ **Modular Architecture**: Fácil de estender e testar

✅ **UI Reutilizável**: Componentes de interface padronizados

## Uso Avançado

### Integrar em seu próprio código

```python
from telegram_manager.utils.config import TelegramConfig
from telegram_manager.core.client import TelegramClientManager
from telegram_manager.core.scanner import TelegramScanner
from telegram_manager.core.exporter import DialogExporter

async def meu_codigo():
    config = TelegramConfig.from_env()
    client_manager = TelegramClientManager(config)
    
    async with client_manager.get_client() as client:
        scanner = TelegramScanner(client)
        result = await scanner.scan_all_dialogs()
        
        exporter = DialogExporter()
        exporter.export_to_json(result)
```

## Troubleshooting

### "Variáveis de ambiente não encontradas"

Certifique-se de que:
1. Criou o arquivo `.env` baseado em `.env.example`
2. Preencheu TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE
3. O arquivo `.env` está no mesmo diretório de `main.py`

### "Connection refused"

Verifique se:
1. Sua conexão internet está ativa
2. Seus dados de API são corretos
3. Não está com IP bloqueado pelo Telegram

### "FloodWait de X segundos"

Espere o tempo indicado. O Telegram está limitando requisições para proteger seus servidores.

## Contribuindo

Melhorias são bem-vindas! Este projeto é um laboratório para aprender:
- Async Python com Telethon
- CLI com Rich
- Arquitetura modular
- Type hints
- Best practices Python

## Licença

MIT License - Use livremente!

## Autor

Gabriel Ramos (@gabrielramos)

---

**Made with ❤️ and Synthwave vibes** 🌆💜
