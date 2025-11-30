import webview
import json
import os

# HTML da calculadora com modo de edição
html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Editável</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .calculator {
            background: #fff;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 370px;
            position: relative;
        }
        
        .edit-toggle {
            position: absolute;
            top: -45px;
            right: 0;
            background: #222;
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            user-select: none;
            transition: 0.2s;
        }
        
        .edit-toggle:hover {
            background: #333;
        }
        
        .edit-mode .edit-toggle {
            background: #4CAF50;
        }
        
        .display {
            background: #f0f0f0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: right;
            min-height: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .expression {
            color: #888;
            font-size: 14px;
            min-height: 20px;
            margin-bottom: 5px;
        }
        
        .result {
            color: #333;
            font-size: 32px;
            font-weight: bold;
            word-wrap: break-word;
        }
        
        .buttons {
            position: relative;
            width: 100%;
            height: 400px;
            border: 2px dashed transparent;
            transition: 0.2s;
            background-image: 
                repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(200,200,200,0.3) 39px, rgba(200,200,200,0.3) 40px),
                repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(200,200,200,0.3) 39px, rgba(200,200,200,0.3) 40px);
            background-size: 40px 40px;
        }
        
        .edit-mode .buttons {
            border-color: rgba(102, 126, 234, 0.5);
            background-color: rgba(102, 126, 234, 0.05);
        }
        
        button {
            position: absolute;
            font-size: 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .num {
            background: #f5f5f5;
            color: #333;
        }
        
        .num:hover {
            background: #e0e0e0;
        }
        
        .operator {
            background: #667eea;
            color: white;
        }
        
        .operator:hover {
            background: #5568d3;
        }
        
        .equals {
            background: #764ba2;
            color: white;
        }
        
        .equals:hover {
            background: #653a8a;
        }
        
        .clear {
            background: #ff6b6b;
            color: white;
        }
        
        .clear:hover {
            background: #ee5a52;
        }
        
        /* Modo de edição */
        .edit-mode button {
            cursor: move;
            border: 2px solid rgba(0,0,0,0.1);
        }
        
        .edit-mode button:hover {
            border-color: #667eea;
            transform: none;
        }
        
        .edit-mode button.dragging {
            opacity: 0.7;
            z-index: 1000;
        }
        
        /* Handle de redimensionamento */
        .resize-handle {
            position: absolute;
            width: 12px;
            height: 12px;
            background: #667eea;
            bottom: -6px;
            right: -6px;
            border-radius: 50%;
            cursor: se-resize;
            display: none;
            z-index: 10;
        }
        
        .edit-mode .resize-handle {
            display: block;
        }
        
        .resize-handle:hover {
            background: #5568d3;
            transform: scale(1.3);
        }
        
        /* Informações de edição */
        .edit-info {
            position: absolute;
            top: -45px;
            left: 0;
            color: white;
            font-size: 12px;
            background: rgba(0,0,0,0.6);
            padding: 8px 12px;
            border-radius: 6px;
            display: none;
        }
        
        .edit-mode .edit-info {
            display: block;
        }
        
        /* Grade visível no modo edição */
        .edit-mode .buttons::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="edit-toggle" id="editToggle">🛠️ Modo Edição</div>
        <div class="edit-info">Arraste e redimensione na grade (40x40px por célula)</div>
        
        <div class="display">
            <div class="expression" id="expression"></div>
            <div class="result" id="result">0</div>
        </div>
        
        <div class="buttons" id="buttonArea"></div>
    </div>

    <script>
        // Configuração da grade
        const GRID_SIZE = 40; // Tamanho de cada célula da grade
        
        // Layout padrão dos botões (em células da grade)
        let buttonLayout = [
            { text: "C", class: "clear", gridX: 0, gridY: 0, gridWidth: 6, gridHeight: 2 },
            { text: "/", class: "operator", gridX: 6, gridY: 0, gridWidth: 2, gridHeight: 2 },
            { text: "×", class: "operator", gridX: 6, gridY: 2, gridWidth: 2, gridHeight: 2 },
            { text: "-", class: "operator", gridX: 6, gridY: 4, gridWidth: 2, gridHeight: 2 },
            
            { text: "7", class: "num", gridX: 0, gridY: 2, gridWidth: 2, gridHeight: 2 },
            { text: "8", class: "num", gridX: 2, gridY: 2, gridWidth: 2, gridHeight: 2 },
            { text: "9", class: "num", gridX: 4, gridY: 2, gridWidth: 2, gridHeight: 2 },
            { text: "+", class: "operator", gridX: 6, gridY: 6, gridWidth: 2, gridHeight: 2 },
            
            { text: "4", class: "num", gridX: 0, gridY: 4, gridWidth: 2, gridHeight: 2 },
            { text: "5", class: "num", gridX: 2, gridY: 4, gridWidth: 2, gridHeight: 2 },
            { text: "6", class: "num", gridX: 4, gridY: 4, gridWidth: 2, gridHeight: 2 },
            { text: "1", class: "num", gridX: 0, gridY: 6, gridWidth: 2, gridHeight: 2 },
            
            { text: "2", class: "num", gridX: 2, gridY: 6, gridWidth: 2, gridHeight: 2 },
            { text: "3", class: "num", gridX: 4, gridY: 6, gridWidth: 2, gridHeight: 2 },
            { text: "0", class: "num", gridX: 0, gridY: 8, gridWidth: 2, gridHeight: 2 },
            { text: ".", class: "num", gridX: 2, gridY: 8, gridWidth: 2, gridHeight: 2 },
            
            { text: "=", class: "equals", gridX: 4, gridY: 8, gridWidth: 4, gridHeight: 2 }
        ];

        const buttonArea = document.getElementById("buttonArea");
        let isEditMode = false;
        let draggedButton = null;
        let resizedButton = null;
        let dragOffset = { x: 0, y: 0 };
        let resizeStart = { gridX: 0, gridY: 0, gridWidth: 0, gridHeight: 0 };

        // Converter grade para pixels
        function gridToPixels(gridValue) {
            return gridValue * GRID_SIZE;
        }

        // Converter pixels para grade
        function pixelsToGrid(pixelValue) {
            return Math.round(pixelValue / GRID_SIZE);
        }

        // Criar botões
        function createButtons() {
            buttonArea.innerHTML = '';
            buttonLayout.forEach((btn, index) => {
                const button = document.createElement("button");
                button.textContent = btn.text;
                button.className = btn.class;
                button.style.left = gridToPixels(btn.gridX) + "px";
                button.style.top = gridToPixels(btn.gridY) + "px";
                button.style.width = gridToPixels(btn.gridWidth) + "px";
                button.style.height = gridToPixels(btn.gridHeight) + "px";
                button.dataset.index = index;
                
                // Handle de redimensionamento
                const resizeHandle = document.createElement("div");
                resizeHandle.className = "resize-handle";
                button.appendChild(resizeHandle);
                
                // Eventos de arrastar
                button.addEventListener("mousedown", startDrag);
                
                // Eventos de redimensionar
                resizeHandle.addEventListener("mousedown", startResize);
                
                // Eventos de clique (calculadora)
                button.addEventListener("click", handleButtonClick);
                
                buttonArea.appendChild(button);
            });
        }

        // Iniciar arrastar
        function startDrag(e) {
            if (!isEditMode || e.target.classList.contains("resize-handle")) return;
            
            e.preventDefault();
            draggedButton = e.currentTarget;
            draggedButton.classList.add("dragging");
            
            const rect = draggedButton.getBoundingClientRect();
            const parentRect = buttonArea.getBoundingClientRect();
            
            dragOffset.x = e.clientX - rect.left;
            dragOffset.y = e.clientY - rect.top;
        }

        // Iniciar redimensionar
        function startResize(e) {
            if (!isEditMode) return;
            
            e.preventDefault();
            e.stopPropagation();
            
            resizedButton = e.target.parentElement;
            const index = resizedButton.dataset.index;
            const btn = buttonLayout[index];
            
            resizeStart.gridX = btn.gridX;
            resizeStart.gridY = btn.gridY;
            resizeStart.gridWidth = btn.gridWidth;
            resizeStart.gridHeight = btn.gridHeight;
            resizeStart.startX = e.clientX;
            resizeStart.startY = e.clientY;
        }

        // Movimentar
        document.addEventListener("mousemove", (e) => {
            if (draggedButton) {
                const parentRect = buttonArea.getBoundingClientRect();
                let pixelX = e.clientX - parentRect.left - dragOffset.x;
                let pixelY = e.clientY - parentRect.top - dragOffset.y;
                
                // Converter para grade
                let gridX = pixelsToGrid(pixelX);
                let gridY = pixelsToGrid(pixelY);
                
                // Limitar dentro da área (8 colunas, 10 linhas)
                const index = draggedButton.dataset.index;
                const btn = buttonLayout[index];
                gridX = Math.max(0, Math.min(gridX, 8 - btn.gridWidth));
                gridY = Math.max(0, Math.min(gridY, 10 - btn.gridHeight));
                
                // Aplicar posição alinhada à grade
                draggedButton.style.left = gridToPixels(gridX) + "px";
                draggedButton.style.top = gridToPixels(gridY) + "px";
            }
            
            if (resizedButton) {
                const deltaX = e.clientX - resizeStart.startX;
                const deltaY = e.clientY - resizeStart.startY;
                
                // Converter delta para células da grade
                let newGridWidth = Math.max(1, resizeStart.gridWidth + pixelsToGrid(deltaX));
                let newGridHeight = Math.max(1, resizeStart.gridHeight + pixelsToGrid(deltaY));
                
                // Limitar tamanho máximo
                newGridWidth = Math.min(newGridWidth, 8 - resizeStart.gridX);
                newGridHeight = Math.min(newGridHeight, 10 - resizeStart.gridY);
                
                resizedButton.style.width = gridToPixels(newGridWidth) + "px";
                resizedButton.style.height = gridToPixels(newGridHeight) + "px";
            }
        });

        // Soltar
        document.addEventListener("mouseup", () => {
            if (draggedButton) {
                const index = draggedButton.dataset.index;
                buttonLayout[index].gridX = pixelsToGrid(parseInt(draggedButton.style.left));
                buttonLayout[index].gridY = pixelsToGrid(parseInt(draggedButton.style.top));
                draggedButton.classList.remove("dragging");
                draggedButton = null;
            }
            
            if (resizedButton) {
                const index = resizedButton.dataset.index;
                buttonLayout[index].gridWidth = pixelsToGrid(parseInt(resizedButton.style.width));
                buttonLayout[index].gridHeight = pixelsToGrid(parseInt(resizedButton.style.height));
                resizedButton = null;
            }
        });

        // Toggle modo de edição
        document.getElementById("editToggle").addEventListener("click", () => {
            isEditMode = !isEditMode;
            document.body.classList.toggle("edit-mode");
            document.getElementById("editToggle").textContent = 
                isEditMode ? "✓ Concluir" : "🛠️ Modo Edição";
        });

        // Lógica da calculadora
        let expression = '';
        let result = '0';
        
        function updateDisplay() {
            document.getElementById('expression').textContent = expression || '';
            document.getElementById('result').textContent = result;
        }
        
        function handleButtonClick(e) {
            if (isEditMode) return;
            
            const text = e.currentTarget.textContent;
            
            if (text === 'C') {
                clearDisplay();
            } else if (['+', '-', '×', '/'].includes(text)) {
                appendOperator(text);
            } else if (text === '=') {
                calculate();
            } else {
                appendNumber(text);
            }
        }
        
        function appendNumber(num) {
            if (result === '0' && num !== '.') {
                result = num;
            } else if (result === 'Erro') {
                result = num;
                expression = '';
            } else {
                result += num;
            }
            updateDisplay();
        }
        
        function appendOperator(op) {
            if (result && result !== 'Erro') {
                if (expression && !expression.endsWith(' ')) {
                    calculate();
                }
                expression = result + ' ' + op + ' ';
                result = '0';
            }
            updateDisplay();
        }
        
        function calculate() {
            if (expression && result && result !== 'Erro') {
                try {
                    const fullExpression = expression + result;
                    const evalResult = eval(fullExpression.replace('×', '*'));
                    result = String(Math.round(evalResult * 100000000) / 100000000);
                    expression = '';
                } catch (e) {
                    result = 'Erro';
                    expression = '';
                }
            }
            updateDisplay();
        }
        
        function clearDisplay() {
            expression = '';
            result = '0';
            updateDisplay();
        }
        
        // Suporte para teclado
        document.addEventListener('keydown', function(e) {
            if (isEditMode) return;
            
            if (e.key >= '0' && e.key <= '9' || e.key === '.') {
                appendNumber(e.key);
            } else if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
                appendOperator(e.key);
            } else if (e.key === 'Enter' || e.key === '=') {
                calculate();
            } else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') {
                clearDisplay();
            }
        });

        // Inicializar
        createButtons();
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    window = webview.create_window(
        'Calculadora Editável',
        html=html_content,
        width=410,
        height=700,
        resizable=False
    )
    webview.start()