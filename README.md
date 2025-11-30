# CalcPythonHtml

Este projeto é uma calculadora desenvolvida em Python, com interface simples e possibilidade de empacotamento para distribuição. O objetivo é fornecer uma ferramenta prática para realizar operações matemáticas básicas.

## Estrutura do Projeto
- `calculadora.py`: Código principal da calculadora.
- `Calculadora.spec`: Arquivo de especificação para empacotamento (PyInstaller).
- `build/`: Pasta gerada automaticamente contendo arquivos de build e distribuição.

## Como usar
1. Execute o arquivo `calculadora.py` para utilizar a calculadora diretamente em Python.
2. Para gerar um executável, utilize o PyInstaller com o arquivo `.spec`:
   ```bash
   pyinstaller Calculadora.spec
   ```
3. O executável será gerado na pasta `build/Calculadora/`.

## Ignorados pelo Git
- Pastas de build
- Arquivos `.spec`
- Arquivos `.zip`

## Autor
DadosCoelho

## Interface
A interface da calculadora é moderna e responsiva, construída em HTML e CSS, exibida por meio de uma janela Python usando o módulo `webview`. Os principais destaques são:

- **Visual agradável:** Fundo com gradiente, botões arredondados e efeitos de sombra.
- **Modo de edição:** Permite ao usuário arrastar e redimensionar os botões na grade, personalizando o layout da calculadora. O modo é ativado pelo botão "🛠️ Modo Edição".
- **Grade editável:** Cada botão pode ser movido e redimensionado em células de 40x40px, facilitando a organização.
- **Display:** Mostra a expressão matemática e o resultado, com destaque visual.
- **Suporte ao teclado:** É possível operar a calculadora usando o teclado, tornando o uso mais prático.

A interface foi pensada para ser intuitiva, funcional e flexível, permitindo personalização sem perder a simplicidade de uso.

---
Sinta-se à vontade para contribuir ou sugerir melhorias!
