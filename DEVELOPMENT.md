# Guia de Desenvolvimento

## Setup de Desenvolvimento

### 1. Clone o repositório

```bash
git clone https://github.com/gabrielramos/telegram-manager.git
cd telegram-manager
```

### 2. Configure o ambiente de desenvolvimento

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instale dependências de desenvolvimento

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

## Estrutura de Código

### Core Modules

```
telegram_manager/
├── core/
│   ├── client.py     - Gerenciamento de conexão
│   ├── scanner.py    - Lógica de escaneamento
│   └── exporter.py   - Exportação de dados
├── ui/
│   ├── theme.py      - Definições de tema
│   └── components.py - Componentes de UI
├── utils/
│   └── config.py     - Gerenciamento de config
└── __init__.py
```

## Convencões de Código

### Type Hints

Todos os arquivos devem ter type hints completos:

```python
from typing import List, Dict, Optional

def minha_funcao(param1: str, param2: int) -> Dict[str, int]:
    """Descrição da função."""
    return {param1: param2}
```

### Docstrings

Use docstrings em estilo Google:

```python
def minha_funcao(param1: str) -> str:
    """Resumo da função.
    
    Descrição mais longa explicando o que a função faz.
    
    Args:
        param1: Descrição do parâmetro.
        
    Returns:
        Descrição do valor retornado.
        
    Raises:
        ValueError: Quando algo dá errado.
    """
    pass
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Mensagem informativa")
logger.warning("Aviso")
logger.error("Erro")
logger.debug("Debug info")
```

### Async/Await

```python
async def minha_funcao_async() -> None:
    """Função assíncrona."""
    result = await alguma_operacao()
    return result
```

## Testes

### Executar todos os testes

```bash
pytest
```

### Executar testes com cobertura

```bash
pytest --cov=telegram_manager --cov-report=html
```

### Exemplo de teste

```python
import pytest
from telegram_manager.utils.config import TelegramConfig

def test_config_validation():
    """Testa validação de configuração."""
    config = TelegramConfig(
        api_id="123456",
        api_hash="a" * 32,
        phone="+5511999999999"
    )
    assert config.validate() is True

def test_config_invalid_api_id():
    """Testa rejeição de API ID inválida."""
    config = TelegramConfig(
        api_id="not_a_number",
        api_hash="a" * 32,
        phone="+5511999999999"
    )
    assert config.validate() is False
```

## Code Quality

### Formatacao com Black

```bash
black telegram_manager/
```

### Import sorting com isort

```bash
isort telegram_manager/
```

### Linting com flake8

```bash
flake8 telegram_manager/ --max-line-length=100
```

### Type checking com mypy

```bash
mypy telegram_manager/
```

### Pre-commit hooks

Crie `.git/hooks/pre-commit`:

```bash
#!/bin/bash
black telegram_manager/
isort telegram_manager/
flake8 telegram_manager/ --max-line-length=100
mypy telegram_manager/
pytest
```

## Adicionando novos módulos

### 1. Criar arquivo no pacote apropriado

```bash
touch telegram_manager/core/novo_modulo.py
```

### 2. Adicionar imports no `__init__.py`

```python
# telegram_manager/core/__init__.py
from .novo_modulo import MinhaClasse

__all__ = ['MinhaClasse']
```

### 3. Adicionar testes

```bash
mkdir -p tests/core
touch tests/core/test_novo_modulo.py
```

### 4. Adicionar documentação

Update README.md com informações sobre o novo módulo.

## Performance

### Profiling

```python
import cProfile
import pstats
from io import StringIO

pr = cProfile.Profile()
pr.enable()

# seu codigo aqui

pr.disable()
s = StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(10)  # Top 10
print(s.getvalue())
```

### Memory usage

```bash
pip install memory-profiler
python -m memory_profiler script.py
```

## Deploy

### Build package

```bash
pip install build
python -m build
```

### Upload to PyPI

```bash
pip install twine
twine upload dist/*
```

## Commit Messages

Use convenção Conventional Commits:

```
feat(scanner): adiciona suporte para bots oficiais
fix(ui): corrige cor do tema em modo escuro
docs: atualiza guia de instalação
test: adiciona testes para config validation
refactor: reorganiza imports
perf: otimiza scan de dialogos
```

## Issues & Pull Requests

### Antes de submeter

- [ ] Código segue convencões (Black, isort)
- [ ] Type hints são completos
- [ ] Testes passam (pytest)
- [ ] Linting passa (flake8, mypy)
- [ ] Documentação está atualizada
- [ ] Commit messages seguem Conventional Commits

## Recursos Úteis

- [Telethon Documentation](https://docs.telethon.dev/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Python Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Async Python](https://docs.python.org/3/library/asyncio.html)
- [Python Logging](https://docs.python.org/3/library/logging.html)

## Troubleshooting

### Import errors

Garanta que:
1. O pacote está instalado em modo edição: `pip install -e .`
2. O ambiente virtual está ativado
3. Executando Python do venv correto

### Test failures

```bash
pytest -vv -s  # Verbose + show output
pytest --pdb   # Debug com pdb
```

---

Happy coding! 🚀💜
