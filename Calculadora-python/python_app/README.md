# Calculadora Minimalista Estilo iOS (Python Desktop)

Aplicação desktop profissional em Python com interface moderna inspirada no iOS, estritamente em tons monocromáticos (preto, cinzas e branco), seguindo os princípios de Clean Code, PEP 8, Type Hinting e arquitetura MVC (Model-View-Controller).

---

## 📱 Recursos Principais

1. **3 Modos de Operação**:
   - **Calculadora Simples**: Layout clássico 4x5 com adição, subtração, multiplicação, divisão, porcentagem (+/- e %) e precisão com `Decimal`.
   - **Calculadora Científica**: Teclado estendido com funções trigonométricas (`sin`, `cos`, `tan`), alternância `Rad`/`Deg`, logaritmos (`log`, `ln`), potências (`x²`, `x³`, `xʸ`, `eˣ`), raízes (`√x`, `³√x`), fatorial (`x!`), constantes (`π`, `e`) e memória (`Ans`).
   - **Conversor de Unidades**: Conversão instantânea bidirecional para **Comprimento**, **Peso**, **Temperatura** (com proteção de zero absoluto) e **Moedas** (com cache offline e atualização via API pública).

2. **Estética iOS Monocromática**:
   - Fundo preto OLED (`#000000`).
   - Botões com cantos arredondados nativos (`CustomTkinter`).
   - Números em cinza escuro (`#333333`), funções secundárias em cinza claro (`#A5A5A5`), operadores em cinza médio (`#505050`) e sem cores saturadas (sem laranja).
   - Display duplo com fonte em escala automática para acomodar números grandes sem truncar.

3. **Gerenciamento de Histórico (CRUD Completo)**:
   - **Create**: Cada operação calculada é gravada com carimbo de hora e modo.
   - **Read**: Painel retrátil lateral com rolagem suave.
   - **Update / Use**: Botão "Usar" em qualquer item do histórico para injetar o valor diretamente no cálculo ativo.
   - **Delete**: Exclusão individual por item (ícone de lixeira) ou limpeza total ("Limpar Histórico").
   - **Persistência**: Salvo em `data/history.json` com fallback defensivo contra arquivos corrompidos.

4. **Tratamento Defensivo de Erros**:
   - Divisão por zero: exibe `"Indefinido"`.
   - Overflow e erros matemáticos (ex: raiz negativa): `"Entrada Inválida"`.
   - Prevenção de injeção e manipulação de precisão via módulo `Decimal`.

5. **Acessibilidade & Atalhos de Teclado**:
   - Teclado numérico: `0` a `9`, `.`, `,`
   - Operadores: `+`, `-`, `*`, `/`
   - Executar cálculo: `Enter` ou `=`
   - Apagar dígito: `Backspace`
   - Limpar tudo (All Clear): `Esc`
   - Porcentagem: `%`

---

## 📂 Arquitetura de Pastas (MVC)

```
python_app/
├── main.py                  # Ponto de entrada da aplicação desktop
├── config.py                # Tokens de design monocromático e constantes
├── requirements.txt         # Dependências (customtkinter, requests, pytest)
├── models/
│   ├── calculator_engine.py # Motor matemático com alta precisão e defensiva
│   ├── unit_converter.py    # Conversor para 4 categorias de medidas
│   ├── exchange_service.py  # Serviço de câmbio com cache JSON e fallback offline
│   └── history_store.py     # CRUD completo de histórico persistido
├── views/
│   ├── main_window.py       # Janela CTk, alternador de modos e adaptação
│   ├── components.py        # Botões arredondados iOSButton e DisplayWidget
│   ├── simple_pad.py        # Grade 4x5 de botões simples
│   ├── scientific_pad.py    # Grade expandida científica
│   ├── converter_view.py    # Interface do conversor de unidades
│   └── history_drawer.py    # Painel lateral retrátil de histórico
├── controllers/
│   └── app_controller.py    # Mediador entre modelos, telas e atalhos
├── tests/
│   ├── test_calculator.py   # Testes unitários do motor matemático
│   ├── test_converter.py    # Testes unitários do conversor
│   └── test_history.py      # Testes unitários do CRUD de histórico
└── data/
    └── history.json         # Arquivo de persistência local
```

---

## 🚀 Como Executar

### 1. Instalar as dependências
```bash
pip install -r python_app/requirements.txt
```

### 2. Iniciar a Calculadora
```bash
python python_app/main.py
```

### 3. Executar os Testes Unitários
```bash
python -m unittest discover -s python_app/tests
```
