# Plano de Refatoração de Arquitetura

## Contexto
O repositório está desorganizado e com responsabilidades misturadas. O objetivo é organizar a base seguindo melhores práticas Python e uma arquitetura limpa “leve”, sem overengineering.

## Objetivos
- Tornar responsabilidades claras (CLI vs. aplicação vs. domínio vs. infraestrutura).
- Melhorar testabilidade e isolamento de dependências externas.
- Facilitar evolução do projeto sem aumentar a complexidade.
- Reduzir acoplamento entre UI/CLI e regras de negócio.

## Proposta de Arquitetura (camadas leves)
- **Interface**: entrada do sistema (CLI e UI). Sem lógica de negócio.
- **Aplicação**: casos de uso e orquestração, dependente apenas de portas (protocols).
- **Domínio**: entidades e regras puras, sem dependências externas.
- **Infraestrutura**: integrações externas (Telethon, IO, dotenv, filesystem).

## Estrutura alvo
```
telegram_manager/
  interface/
    cli.py
    ui/
      components.py
      theme.py
  application/
    bootstrap.py
    ports/
      dialog_scanner.py
      dialog_exporter.py
      media_downloader.py
    use_cases/
      scan_dialogs.py
      export_dialogs.py
      download_media.py
  domain/
    entities/
      dialog.py
    policies/
      bot_classification.py
  infrastructure/
    telethon/
      client.py
      scanner.py
      downloader.py
    storage/
      dialog_exporter.py
    config/
      env.py
```

## Movimentações principais
- `telegram_manager/core/client.py` -> `telegram_manager/infrastructure/telethon/client.py`
- `telegram_manager/core/scanner.py` -> `telegram_manager/infrastructure/telethon/scanner.py`
- `telegram_manager/core/exporter.py` -> `telegram_manager/infrastructure/storage/dialog_exporter.py`
- `telegram_manager/core/downloader.py` -> `telegram_manager/infrastructure/telethon/downloader.py`
- `telegram_manager/utils/config.py` -> `telegram_manager/infrastructure/config/env.py`
- `DialogInfo` e `ScanResult` -> `telegram_manager/domain/entities/dialog.py`
- regra de bot oficial -> `telegram_manager/domain/policies/bot_classification.py`
- `telegram_manager/ui/*` -> `telegram_manager/interface/ui/*`
- `telegram_manager/cli.py` permanece como entrada principal

## Casos de uso (aplicação)
- `scan_dialogs.py`: coordena o scanner e retorna `ScanResult`.
- `export_dialogs.py`: coordena exportações (JSON/CSV) a partir de `ScanResult`.
- `download_media.py`: coordena download por chats e filtros.

## Portas (protocols)
Definir interfaces simples para desacoplar aplicação de infraestrutura:
- `DialogScanner`: `scan_all_dialogs() -> ScanResult`
- `DialogExporter`: `export_to_json(result)`, `export_to_csv(result)`
- `MediaDownloader`: `download_all_media(dialogs, progress, ...)`

## Fluxo recomendado
CLI -> bootstrap -> casos de uso -> infra
- A CLI não conhece Telethon diretamente.
- A infra converte erros em mensagens claras (sem vazar tipos Telethon para a CLI).

## Passos de execução (ordem segura)
1. Criar novas pastas e mover entidades para domínio.
2. Criar portas e casos de uso na aplicação.
3. Mover implementações para infraestrutura e ajustar imports.
4. Atualizar CLI para usar casos de uso via bootstrap.
5. Atualizar `README.md` com a nova estrutura.
6. Adicionar testes unitários para domínio e aplicação (fakes das portas).

## Critérios de sucesso
- CLI funciona sem acessar classes Telethon diretamente.
- Domínio não depende de Rich, Telethon ou filesystem.
- Infra fica isolada e substituível.
- Estrutura do repositório fica clara e previsível.

## Riscos
- Import paths quebrados durante a migração.
- Necessidade de ajustes em testes e documentação.

## Próximos passos
- Aplicar a refatoração por etapas.
- Validar com execução manual e testes básicos.
