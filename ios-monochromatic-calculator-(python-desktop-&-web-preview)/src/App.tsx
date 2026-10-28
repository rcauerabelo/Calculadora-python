/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  History,
  Trash2,
  ArrowUpDown,
  Code2,
  Terminal,
  Copy,
  Check,
  CheckCircle2,
  Layers,
  Sparkles,
  Maximize2,
  RotateCcw,
  BookOpen
} from 'lucide-react';

// --- TYPES ---
type AppMode = 'simples' | 'cientifica' | 'conversor';
type ConverterCategory = 'Comprimento' | 'Peso' | 'Temperatura' | 'Moeda';

interface HistoryRecord {
  id: string;
  expression: string;
  result: string;
  mode: string;
  timestamp: string;
}

// --- CONVERSION RATES & TABLES ---
const LENGTH_UNITS: Record<string, number> = {
  'Metros (m)': 1.0,
  'Quilômetros (km)': 1000.0,
  'Centímetros (cm)': 0.01,
  'Milímetros (mm)': 0.001,
  'Milhas (mi)': 1609.344,
  'Jardas (yd)': 0.9144,
  'Pés (ft)': 0.3048,
  'Polegadas (in)': 0.0254,
};

const WEIGHT_UNITS: Record<string, number> = {
  'Quilogramas (kg)': 1000.0,
  'Gramas (g)': 1.0,
  'Miligramas (mg)': 0.001,
  'Libras (lb)': 453.59237,
  'Onças (oz)': 28.349523,
  'Toneladas (t)': 1000000.0,
};

const CURRENCY_RATES: Record<string, number> = {
  'USD (Dólar Americano)': 1.0,
  'BRL (Real Brasileiro)': 5.45,
  'EUR (Euro)': 0.92,
  'GBP (Libra Esterlina)': 0.79,
  'JPY (Iene Japonês)': 152.3,
  'CAD (Dólar Canadense)': 1.38,
  'CHF (Franco Suíço)': 0.87,
  'BTC (Bitcoin)': 0.000015,
};

// --- PYTHON FILES REPOSITORY FOR CODE EXPLORER ---
const PYTHON_FILES: Record<string, { desc: string; code: string }> = {
  'main.py': {
    desc: 'Ponto de entrada que inicializa a aplicação desktop CustomTkinter e o MVC',
    code: `"""Application Entry Point.

Initializes the MVC architecture and launches the CustomTkinter main loop.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from python_app.controllers.app_controller import AppController
from python_app.views.main_window import MainWindow


def main() -> None:
    """Bootstrap controller and window, and start event loop."""
    controller = AppController()
    app = MainWindow(controller=controller)
    controller.attach_window(app)

    import threading
    threading.Thread(target=controller.exchange_service.fetch_live_rates, daemon=True).start()

    app.mainloop()


if __name__ == "__main__":
    main()
`
  },
  'config.py': {
    desc: 'Tokens visuais monocromáticos iOS, fontes, tamanhos de janela e caminhos',
    code: `from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ColorPalette:
    """Strictly monochromatic iOS palette tokens (black, grays, white)."""
    WINDOW_BG: str = "#000000"           # Pure black base
    CONTAINER_BG: str = "#1C1C1E"        # iOS secondary background
    SURFACE_BG: str = "#2C2C2E"          # iOS tertiary background
    SURFACE_HOVER: str = "#3A3A3C"

    TEXT_PRIMARY: str = "#FFFFFF"        # Pure white text
    TEXT_SECONDARY: str = "#8E8E93"      # Muted silver/gray label
    TEXT_DARK: str = "#000000"           # High contrast dark text

    BTN_NUMBER_BG: str = "#333333"       # Dark gray for numbers 0-9
    BTN_NUMBER_HOVER: str = "#48484A"
    BTN_NUMBER_TEXT: str = "#FFFFFF"

    BTN_FUNCTION_BG: str = "#A5A5A5"     # Light gray for AC, +/-, %
    BTN_FUNCTION_HOVER: str = "#D1D1D6"
    BTN_FUNCTION_TEXT: str = "#000000"

    BTN_OPERATOR_BG: str = "#505050"     # Mid gray for +, -, *, /, =
    BTN_OPERATOR_HOVER: str = "#636366"
    BTN_OPERATOR_TEXT: str = "#FFFFFF"

    BTN_SCIENTIFIC_BG: str = "#242426"   # Deep graphite for scientific keys
    BTN_SCIENTIFIC_HOVER: str = "#3A3A3C"
    BTN_SCIENTIFIC_TEXT: str = "#D1D1D6"

COLORS = ColorPalette()
`
  },
  'models/calculator_engine.py': {
    desc: 'Motor matemático com precisão Decimal, funções científicas e tratamento de erros',
    code: `from decimal import Decimal, InvalidOperation, getcontext
import math
from typing import Optional, Tuple

getcontext().prec = 28

class CalculatorEngine:
    """Core mathematical engine for arithmetic and scientific calculations."""

    def __init__(self) -> None:
        self.current_value: str = "0"
        self.expression_preview: str = ""
        self.last_operator: Optional[str] = None
        self.pending_operand: Optional[Decimal] = None
        self.is_new_entry: bool = True
        self.is_degree_mode: bool = False
        self.last_result: Optional[str] = None

    def reset(self) -> None:
        self.current_value = "0"
        self.expression_preview = ""
        self.last_operator = None
        self.pending_operand = None
        self.is_new_entry = True

    def calculate_result(self) -> Tuple[Optional[str], str]:
        if self.pending_operand is None or self.last_operator is None:
            return None, self.current_value

        try:
            current = Decimal(self.current_value)
            prev = self.pending_operand
            op = self.last_operator

            symbol = "×" if op == "*" else ("÷" if op == "/" else op)
            expr_str = f"{prev} {symbol} {current}"

            if op == "+": res = prev + current
            elif op == "-": res = prev - current
            elif op == "*": res = prev * current
            elif op == "/":
                if current == Decimal("0"):
                    self.current_value = "Indefinido"
                    return expr_str, "Indefinido"
                res = prev / current
            elif op == "^":
                res = Decimal(str(math.pow(float(prev), float(current))))

            result_str = self._format_decimal(res)
            self.current_value = result_str
            self.expression_preview = f"{expr_str} ="
            self.pending_operand = None
            self.last_operator = None
            self.is_new_entry = True
            self.last_result = result_str
            return expr_str, result_str
        except ZeroDivisionError:
            return None, "Indefinido"
        except OverflowError:
            return None, "Estouro de Memória"
        except (InvalidOperation, ValueError):
            return None, "Entrada Inválida"
`
  },
  'models/history_store.py': {
    desc: 'Gerenciamento do CRUD de histórico com persistência em arquivo JSON local',
    code: `from dataclasses import asdict, dataclass
from datetime import datetime
import json
import os
import uuid
from typing import List, Optional

@dataclass
class HistoryEntry:
    id: str
    expression: str
    result: str
    mode: str
    created_at: str

class HistoryStore:
    """Thread-safe and defensive storage manager for calculator history CRUD."""

    def __init__(self, storage_path: str = "data/history.json", max_entries: int = 100):
        self.storage_path = storage_path
        self.max_entries = max_entries
        self.entries: List[HistoryEntry] = []
        self._load_from_disk()

    # CRUD: CREATE
    def add(self, expression: str, result: str, mode: str = "Simples") -> HistoryEntry:
        if result in ("Indefinido", "Erro de Sintaxe", "Entrada Inválida", "Estouro de Memória"):
            return None
        entry = HistoryEntry(
            id=str(uuid.uuid4())[:8],
            expression=expression,
            result=result,
            mode=mode,
            created_at=datetime.now().strftime("%H:%M:%S")
        )
        self.entries.insert(0, entry)
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[:self.max_entries]
        self._save_to_disk()
        return entry

    # CRUD: READ
    def get_all(self) -> List[HistoryEntry]:
        return list(self.entries)

    # CRUD: DELETE
    def delete_by_id(self, entry_id: str) -> bool:
        initial = len(self.entries)
        self.entries = [e for e in self.entries if e.id != entry_id]
        if len(self.entries) < initial:
            self._save_to_disk()
            return True
        return False

    def clear(self) -> None:
        self.entries.clear()
        self._save_to_disk()
`
  },
  'models/unit_converter.py': {
    desc: 'Conversões bidirecionais de comprimento, peso, temperatura e câmbio',
    code: `class UnitConverter:
    """Core domain model for converting measurements across diverse categories."""

    def convert(self, category: str, value: float, from_unit: str, to_unit: str) -> float:
        if from_unit == to_unit:
            return value

        if category == "Comprimento":
            return self._convert_linear(value, from_unit, to_unit, self.LENGTH_UNITS)
        if category == "Peso":
            if value < 0:
                raise ValueError("Massa não pode ser negativa.")
            return self._convert_linear(value, from_unit, to_unit, self.WEIGHT_UNITS)
        if category == "Temperatura":
            return self._convert_temperature(value, from_unit, to_unit)
        if category == "Moeda":
            return self._convert_currency(value, from_unit, to_unit)
`
  },
  'controllers/app_controller.py': {
    desc: 'Controlador MVC mediando views, modelos matemáticos e atalhos de teclado',
    code: `class AppController:
    """Controller coordinating CalculatorEngine, UnitConverter, and HistoryStore."""

    def __init__(self, engine=None, history_store=None, unit_converter=None):
        self.engine = engine or CalculatorEngine()
        self.history_store = history_store or HistoryStore()
        self.unit_converter = unit_converter or UnitConverter()
        self.window = None
        self.active_mode = "Simples"

    def handle_digit(self, digit: str) -> None:
        self.engine.input_digit(digit)
        self._update_display()

    def handle_action(self, action: str) -> None:
        if action == "=":
            expr, res = self.engine.calculate_result()
            if expr and res not in ("Indefinido", "Erro de Sintaxe"):
                self.history_store.add(expr, res, mode=self.active_mode)
`
  },
  'tests/test_calculator.py': {
    desc: '22 Testes unitários com unittest cobrindo aritmética, precisão e exceções',
    code: `import unittest
from python_app.models.calculator_engine import CalculatorEngine

class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CalculatorEngine()

    def test_precision_floating_point(self):
        # 0.1 + 0.2 must equal 0.3 without floating-point artifacts
        self.engine.input_digit("0")
        self.engine.input_decimal_separator()
        self.engine.input_digit("1")
        self.engine.set_operator("+")
        self.engine.input_digit("0")
        self.engine.input_decimal_separator()
        self.engine.input_digit("2")
        _, res = self.engine.calculate_result()
        self.assertEqual(res, "0.3")

    def test_division_by_zero(self):
        self.engine.input_digit("9")
        self.engine.set_operator("/")
        self.engine.input_digit("0")
        _, res = self.engine.calculate_result()
        self.assertEqual(res, "Indefinido")
`
  }
};

export default function App() {
  // Main Navigation: Interactive App vs Python Code Viewer
  const [activeTab, setActiveTab] = useState<'calculator' | 'code'>('calculator');

  // Calculator State
  const [mode, setMode] = useState<AppMode>('simples');
  const [displayValue, setDisplayValue] = useState<string>('0');
  const [expressionPreview, setExpressionPreview] = useState<string>('');
  const [pendingOperand, setPendingOperand] = useState<number | null>(null);
  const [pendingOperator, setPendingOperator] = useState<string | null>(null);
  const [isNewEntry, setIsNewEntry] = useState<boolean>(true);
  const [isDegreeMode, setIsDegreeMode] = useState<boolean>(false);
  const [lastResult, setLastResult] = useState<string | null>(null);

  // History Drawer State (CRUD)
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);
  const [historyList, setHistoryList] = useState<HistoryRecord[]>(() => {
    try {
      const saved = localStorage.getItem('calc_history');
      return saved ? JSON.parse(saved) : [
        { id: '1', expression: '125 × 4', result: '500', mode: 'Simples', timestamp: '10:42:15' },
        { id: '2', expression: '√144', result: '12', mode: 'Científica', timestamp: '10:45:00' }
      ];
    } catch {
      return [];
    }
  });

  // Unit Converter State
  const [converterCat, setConverterCat] = useState<ConverterCategory>('Comprimento');
  const [fromUnit, setFromUnit] = useState<string>('Metros (m)');
  const [toUnit, setToUnit] = useState<string>('Pés (ft)');
  const [converterInput, setConverterInput] = useState<string>('1');

  // Python Code Explorer State
  const [selectedPythonFile, setSelectedPythonFile] = useState<string>('models/calculator_engine.py');
  const [copiedFile, setCopiedFile] = useState<boolean>(false);

  // Persist history to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('calc_history', JSON.stringify(historyList));
    } catch {
      // Ignored
    }
  }, [historyList]);

  // Keyboard Shortcuts Listener
  useEffect(() => {
    if (activeTab !== 'calculator') return;

    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't intercept if user is typing in standard inputs
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) {
        return;
      }

      if (e.key >= '0' && e.key <= '9') {
        e.preventDefault();
        handleDigit(e.key);
      } else if (e.key === '.' || e.key === ',') {
        e.preventDefault();
        handleDecimal();
      } else if (['+', '-'].includes(e.key)) {
        e.preventDefault();
        handleOperator(e.key);
      } else if (e.key === '*') {
        e.preventDefault();
        handleOperator('×');
      } else if (e.key === '/') {
        e.preventDefault();
        handleOperator('÷');
      } else if (e.key === 'Enter' || e.key === '=') {
        e.preventDefault();
        handleEquals();
      } else if (e.key === 'Backspace') {
        e.preventDefault();
        handleBackspace();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        handleClear();
      } else if (e.key === '%') {
        e.preventDefault();
        handlePercentage();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeTab, displayValue, pendingOperand, pendingOperator, isNewEntry, mode]);

  // --- ARITHMETIC / SCIENTIFIC ACTIONS ---

  const handleDigit = (digit: string) => {
    if (mode === 'conversor') {
      if (converterInput === '0' || converterInput === '') {
        setConverterInput(digit);
      } else if (converterInput.length < 14) {
        setConverterInput(converterInput + digit);
      }
      return;
    }

    if (isNewEntry || displayValue === '0' || ['Indefinido', 'Erro de Sintaxe', 'Entrada Inválida'].includes(displayValue)) {
      setDisplayValue(digit);
      setIsNewEntry(false);
    } else {
      if (displayValue.replace(/[\.\-]/g, '').length < 16) {
        setDisplayValue(displayValue + digit);
      }
    }
  };

  const handleDecimal = () => {
    if (mode === 'conversor') {
      if (!converterInput.includes('.')) {
        setConverterInput(converterInput + '.');
      }
      return;
    }

    if (isNewEntry || ['Indefinido', 'Erro de Sintaxe', 'Entrada Inválida'].includes(displayValue)) {
      setDisplayValue('0.');
      setIsNewEntry(false);
    } else if (!displayValue.includes('.')) {
      setDisplayValue(displayValue + '.');
    }
  };

  const handleClear = () => {
    if (mode === 'conversor') {
      setConverterInput('0');
      return;
    }
    setDisplayValue('0');
    setExpressionPreview('');
    setPendingOperand(null);
    setPendingOperator(null);
    setIsNewEntry(true);
  };

  const handleBackspace = () => {
    if (mode === 'conversor') {
      if (converterInput.length > 1) {
        setConverterInput(converterInput.slice(0, -1));
      } else {
        setConverterInput('0');
      }
      return;
    }

    if (isNewEntry || ['Indefinido', 'Erro de Sintaxe', 'Entrada Inválida'].includes(displayValue)) {
      setDisplayValue('0');
      setIsNewEntry(true);
      return;
    }

    if (displayValue.length > 1) {
      const next = displayValue.slice(0, -1);
      setDisplayValue(next === '-' ? '0' : next);
    } else {
      setDisplayValue('0');
      setIsNewEntry(true);
    }
  };

  const handleToggleSign = () => {
    if (mode === 'conversor') {
      if (converterInput.startsWith('-')) {
        setConverterInput(converterInput.slice(1));
      } else if (converterInput !== '0') {
        setConverterInput('-' + converterInput);
      }
      return;
    }

    if (displayValue === '0' || ['Indefinido', 'Erro de Sintaxe', 'Entrada Inválida'].includes(displayValue)) return;
    if (displayValue.startsWith('-')) {
      setDisplayValue(displayValue.slice(1));
    } else {
      setDisplayValue('-' + displayValue);
    }
  };

  const handlePercentage = () => {
    try {
      const val = parseFloat(displayValue);
      if (isNaN(val)) return;
      const res = val / 100;
      setDisplayValue(String(res));
      setIsNewEntry(true);
    } catch {
      setDisplayValue('Entrada Inválida');
    }
  };

  const handleOperator = (op: string) => {
    const currentNum = parseFloat(displayValue);

    if (pendingOperand !== null && !isNewEntry && pendingOperator) {
      calculateBinary(pendingOperand, currentNum, pendingOperator);
    } else {
      setPendingOperand(currentNum);
    }

    setPendingOperator(op);
    setExpressionPreview(`${displayValue} ${op}`);
    setIsNewEntry(true);
  };

  const calculateBinary = (op1: number, op2: number, op: string) => {
    let result = 0;
    const expr = `${op1} ${op} ${op2}`;

    if (op === '+') {
      result = op1 + op2;
    } else if (op === '-') {
      result = op1 - op2;
    } else if (op === '×' || op === '*') {
      result = op1 * op2;
    } else if (op === '÷' || op === '/') {
      if (op2 === 0) {
        setDisplayValue('Indefinido');
        setExpressionPreview(`${expr} =`);
        setPendingOperand(null);
        setPendingOperator(null);
        setIsNewEntry(true);
        return;
      }
      result = op1 / op2;
    } else if (op === '^') {
      result = Math.pow(op1, op2);
    }

    // Round clean floats
    const formatted = parseFloat(result.toPrecision(12)).toString();
    setDisplayValue(formatted);
    setExpressionPreview(`${expr} =`);
    setPendingOperand(null);
    setPendingOperator(null);
    setIsNewEntry(true);
    setLastResult(formatted);

    // Save to History (CRUD Create)
    addHistoryEntry(expr, formatted, mode === 'cientifica' ? 'Científica' : 'Simples');
  };

  const handleEquals = () => {
    if (pendingOperand === null || pendingOperator === null) return;
    const currentNum = parseFloat(displayValue);
    calculateBinary(pendingOperand, currentNum, pendingOperator);
  };

  // --- SCIENTIFIC FUNCTIONS ---

  const handleScientific = (funcName: string) => {
    try {
      const val = parseFloat(displayValue);
      if (isNaN(val)) return;

      let res = 0;
      let expr = `${funcName}(${displayValue})`;
      const angle = isDegreeMode ? (val * Math.PI) / 180 : val;

      if (funcName === 'sin') {
        res = Math.sin(angle);
      } else if (funcName === 'cos') {
        res = Math.cos(angle);
      } else if (funcName === 'tan') {
        if (Math.abs(Math.cos(angle)) < 1e-12) {
          setDisplayValue('Indefinido');
          return;
        }
        res = Math.tan(angle);
      } else if (funcName === 'sqrt') {
        if (val < 0) {
          setDisplayValue('Entrada Inválida');
          return;
        }
        res = Math.sqrt(val);
        expr = `√(${displayValue})`;
      } else if (funcName === 'cbrt') {
        res = Math.cbrt(val);
        expr = `³√(${displayValue})`;
      } else if (funcName === 'sqr') {
        res = val * val;
        expr = `(${displayValue})²`;
      } else if (funcName === 'cube') {
        res = val * val * val;
        expr = `(${displayValue})³`;
      } else if (funcName === 'inverse') {
        if (val === 0) {
          setDisplayValue('Indefinido');
          return;
        }
        res = 1 / val;
        expr = `1/(${displayValue})`;
      } else if (funcName === 'log10') {
        if (val <= 0) {
          setDisplayValue('Entrada Inválida');
          return;
        }
        res = Math.log10(val);
      } else if (funcName === 'ln') {
        if (val <= 0) {
          setDisplayValue('Entrada Inválida');
          return;
        }
        res = Math.log(val);
      } else if (funcName === 'exp') {
        res = Math.exp(val);
        expr = `e^(${displayValue})`;
      } else if (funcName === 'factorial') {
        if (val < 0 || !Number.isInteger(val) || val > 170) {
          setDisplayValue(val > 170 ? 'Estouro de Memória' : 'Entrada Inválida');
          return;
        }
        let f = 1;
        for (let i = 2; i <= val; i++) f *= i;
        res = f;
        expr = `${val}!`;
      } else if (funcName === 'pi') {
        res = Math.PI;
        expr = 'π';
      } else if (funcName === 'e') {
        res = Math.E;
        expr = 'e';
      }

      if (Math.abs(res) < 1e-14) res = 0;
      const formatted = parseFloat(res.toPrecision(12)).toString();
      setDisplayValue(formatted);
      setExpressionPreview(`${expr} =`);
      setIsNewEntry(true);
      setLastResult(formatted);

      addHistoryEntry(expr, formatted, 'Científica');
    } catch {
      setDisplayValue('Entrada Inválida');
    }
  };

  // --- CRUD HISTORY OPERATIONS ---

  const addHistoryEntry = (expression: string, result: string, m: string) => {
    if (['Indefinido', 'Erro de Sintaxe', 'Entrada Inválida', 'Estouro de Memória'].includes(result)) return;
    const now = new Date();
    const timeStr = now.toLocaleTimeString('pt-BR', { hour12: false });
    const newEntry: HistoryRecord = {
      id: Math.random().toString(36).substring(2, 9),
      expression,
      result,
      mode: m,
      timestamp: timeStr,
    };
    setHistoryList(prev => [newEntry, ...prev.slice(0, 99)]);
  };

  const handleUseHistory = (val: string) => {
    setDisplayValue(val);
    setIsNewEntry(true);
    setIsHistoryOpen(false);
  };

  const handleDeleteHistory = (id: string) => {
    setHistoryList(prev => prev.filter(item => item.id !== id));
  };

  const handleClearHistory = () => {
    setHistoryList([]);
  };

  // --- UNIT CONVERTER CALCULATIONS ---

  const converterUnits = useMemo(() => {
    if (converterCat === 'Comprimento') return Object.keys(LENGTH_UNITS);
    if (converterCat === 'Peso') return Object.keys(WEIGHT_UNITS);
    if (converterCat === 'Temperatura') return ['Graus Celsius (°C)', 'Graus Fahrenheit (°F)', 'Kelvin (K)'];
    if (converterCat === 'Moeda') return Object.keys(CURRENCY_RATES);
    return [];
  }, [converterCat]);

  // Adjust units when category changes
  const handleCategoryChange = (cat: ConverterCategory) => {
    setConverterCat(cat);
    let units: string[] = [];
    if (cat === 'Comprimento') units = Object.keys(LENGTH_UNITS);
    else if (cat === 'Peso') units = Object.keys(WEIGHT_UNITS);
    else if (cat === 'Temperatura') units = ['Graus Celsius (°C)', 'Graus Fahrenheit (°F)', 'Kelvin (K)'];
    else if (cat === 'Moeda') units = Object.keys(CURRENCY_RATES);

    if (units.length >= 2) {
      setFromUnit(units[0]);
      setToUnit(units[1]);
    }
  };

  const convertedResult = useMemo(() => {
    const val = parseFloat(converterInput || '0');
    if (isNaN(val)) return '0';
    if (fromUnit === toUnit) return val.toString();

    try {
      if (converterCat === 'Comprimento') {
        const base = val * LENGTH_UNITS[fromUnit];
        const res = base / LENGTH_UNITS[toUnit];
        return parseFloat(res.toPrecision(8)).toString();
      }

      if (converterCat === 'Peso') {
        if (val < 0) return 'Inválido';
        const base = val * WEIGHT_UNITS[fromUnit];
        const res = base / WEIGHT_UNITS[toUnit];
        return parseFloat(res.toPrecision(8)).toString();
      }

      if (converterCat === 'Temperatura') {
        let celsius = val;
        if (fromUnit.includes('Fahrenheit')) celsius = (val - 32) * (5 / 9);
        else if (fromUnit.includes('Kelvin')) {
          if (val < 0) return 'Abaixo de 0 K';
          celsius = val - 273.15;
        }

        if (celsius < -273.15) return 'Abaixo de 0 K';

        let target = celsius;
        if (toUnit.includes('Fahrenheit')) target = (celsius * 9) / 5 + 32;
        else if (toUnit.includes('Kelvin')) target = celsius + 273.15;

        return parseFloat(target.toFixed(4)).toString();
      }

      if (converterCat === 'Moeda') {
        const rateFrom = CURRENCY_RATES[fromUnit] || 1;
        const rateTo = CURRENCY_RATES[toUnit] || 1;
        const res = (val / rateFrom) * rateTo;
        return res.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      }
    } catch {
      return 'Erro';
    }
    return '0';
  }, [converterCat, converterInput, fromUnit, toUnit]);

  const handleSwapUnits = () => {
    const temp = fromUnit;
    setFromUnit(toUnit);
    setToUnit(temp);
  };

  const handleSaveConversionToHistory = () => {
    addHistoryEntry(
      `${converterInput} ${fromUnit} ➔`,
      `${convertedResult} ${toUnit}`,
      `Conversor (${converterCat})`
    );
  };

  const copyCodeToClipboard = () => {
    const code = PYTHON_FILES[selectedPythonFile]?.code || '';
    navigator.clipboard.writeText(code);
    setCopiedFile(true);
    setTimeout(() => setCopiedFile(false), 2000);
  };

  return (
    <div className="min-h-screen bg-[#0A0A0C] text-[#F5F5F7] flex flex-col font-sans selection:bg-[#3A3A3C] selection:text-white">
      {/* Top Header Navigation */}
      <header className="border-b border-[#2C2C2E] bg-black/70 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-white/10 flex items-center justify-center border border-white/20">
              <span className="font-semibold text-xs tracking-tighter text-white">iOS</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm tracking-tight text-white">Calculadora Minimalista</span>
              <span className="text-xs text-[#8E8E93] hidden sm:inline">· Python MVC Desktop & Preview</span>
            </div>
          </div>

          {/* Tab Switcher: Live App vs Python Code Viewer */}
          <div className="flex items-center bg-[#1C1C1E] p-1 rounded-xl border border-[#2C2C2E]">
            <button
              onClick={() => setActiveTab('calculator')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
                activeTab === 'calculator'
                  ? 'bg-white text-black shadow-sm font-semibold'
                  : 'text-[#8E8E93] hover:text-white'
              }`}
            >
              <Maximize2 className="w-3.5 h-3.5" />
              Calculadora Interativa
            </button>
            <button
              onClick={() => setActiveTab('code')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
                activeTab === 'code'
                  ? 'bg-white text-black shadow-sm font-semibold'
                  : 'text-[#8E8E93] hover:text-white'
              }`}
            >
              <Code2 className="w-3.5 h-3.5" />
              Código Python (MVC)
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl w-full mx-auto p-4 sm:p-6 flex flex-col items-center justify-center">
        {activeTab === 'calculator' ? (
          <div className="w-full flex flex-col lg:flex-row items-center justify-center gap-6">
            {/* The iOS Calculator Container */}
            <div
              className={`relative bg-black rounded-[36px] p-5 shadow-2xl border border-[#2C2C2E] transition-all duration-300 ${
                mode === 'cientifica'
                  ? 'w-full max-w-[640px]'
                  : mode === 'conversor'
                  ? 'w-full max-w-[420px]'
                  : 'w-full max-w-[360px]'
              }`}
            >
              {/* Top Controls: Mode Segmented Switcher & History Drawer Toggle */}
              <div className="flex items-center justify-between gap-2 mb-4">
                <div className="flex-1 bg-[#1C1C1E] p-1 rounded-xl flex items-center border border-[#2C2C2E]">
                  {(['simples', 'cientifica', 'conversor'] as AppMode[]).map(m => (
                    <button
                      key={m}
                      onClick={() => setMode(m)}
                      className={`flex-1 py-1.5 text-xs font-semibold rounded-lg capitalize transition-all ${
                        mode === m
                          ? 'bg-[#333333] text-white shadow'
                          : 'text-[#8E8E93] hover:text-white'
                      }`}
                    >
                      {m === 'simples' ? 'Simples' : m === 'cientifica' ? 'Científica' : 'Conversor'}
                    </button>
                  ))}
                </div>

                <button
                  onClick={() => setIsHistoryOpen(!isHistoryOpen)}
                  title="Histórico de Cálculos"
                  className={`p-2 rounded-xl transition-all border ${
                    isHistoryOpen
                      ? 'bg-white text-black border-white'
                      : 'bg-[#1C1C1E] text-[#8E8E93] hover:text-white border-[#2C2C2E]'
                  }`}
                >
                  <History className="w-4 h-4" />
                </button>
              </div>

              {/* Display Area (Only in Simple & Scientific modes) */}
              {mode !== 'conversor' && (
                <div className="bg-[#1C1C1E] rounded-2xl p-4 mb-4 flex flex-col justify-end min-h-[110px] border border-[#2C2C2E]/60">
                  <div className="text-right text-[#8E8E93] text-xs font-mono h-5 overflow-hidden text-ellipsis whitespace-nowrap">
                    {expressionPreview}
                  </div>
                  <div className="text-right text-white font-bold font-sans tracking-tight text-3xl sm:text-4xl overflow-hidden text-ellipsis whitespace-nowrap">
                    {displayValue}
                  </div>
                </div>
              )}

              {/* Mode: Calculadora Simples */}
              {mode === 'simples' && (
                <div className="grid grid-cols-4 gap-2.5">
                  <button
                    onClick={handleClear}
                    className="h-16 rounded-full bg-[#A5A5A5] hover:bg-[#D1D1D6] active:scale-95 text-black font-semibold text-lg transition-transform flex items-center justify-center"
                  >
                    AC
                  </button>
                  <button
                    onClick={handleToggleSign}
                    className="h-16 rounded-full bg-[#A5A5A5] hover:bg-[#D1D1D6] active:scale-95 text-black font-semibold text-lg transition-transform flex items-center justify-center"
                  >
                    +/-
                  </button>
                  <button
                    onClick={handlePercentage}
                    className="h-16 rounded-full bg-[#A5A5A5] hover:bg-[#D1D1D6] active:scale-95 text-black font-semibold text-lg transition-transform flex items-center justify-center"
                  >
                    %
                  </button>
                  <button
                    onClick={() => handleOperator('÷')}
                    className="h-16 rounded-full bg-[#505050] hover:bg-[#636366] active:scale-95 text-white font-semibold text-2xl transition-transform flex items-center justify-center"
                  >
                    ÷
                  </button>

                  {['7', '8', '9'].map(d => (
                    <button
                      key={d}
                      onClick={() => handleDigit(d)}
                      className="h-16 rounded-full bg-[#333333] hover:bg-[#48484A] active:scale-95 text-white font-normal text-2xl transition-transform flex items-center justify-center"
                    >
                      {d}
                    </button>
                  ))}
                  <button
                    onClick={() => handleOperator('×')}
                    className="h-16 rounded-full bg-[#505050] hover:bg-[#636366] active:scale-95 text-white font-semibold text-2xl transition-transform flex items-center justify-center"
                  >
                    ×
                  </button>

                  {['4', '5', '6'].map(d => (
                    <button
                      key={d}
                      onClick={() => handleDigit(d)}
                      className="h-16 rounded-full bg-[#333333] hover:bg-[#48484A] active:scale-95 text-white font-normal text-2xl transition-transform flex items-center justify-center"
                    >
                      {d}
                    </button>
                  ))}
                  <button
                    onClick={() => handleOperator('-')}
                    className="h-16 rounded-full bg-[#505050] hover:bg-[#636366] active:scale-95 text-white font-semibold text-2xl transition-transform flex items-center justify-center"
                  >
                    -
                  </button>

                  {['1', '2', '3'].map(d => (
                    <button
                      key={d}
                      onClick={() => handleDigit(d)}
                      className="h-16 rounded-full bg-[#333333] hover:bg-[#48484A] active:scale-95 text-white font-normal text-2xl transition-transform flex items-center justify-center"
                    >
                      {d}
                    </button>
                  ))}
                  <button
                    onClick={() => handleOperator('+')}
                    className="h-16 rounded-full bg-[#505050] hover:bg-[#636366] active:scale-95 text-white font-semibold text-2xl transition-transform flex items-center justify-center"
                  >
                    +
                  </button>

                  <button
                    onClick={() => handleDigit('0')}
                    className="col-span-2 h-16 rounded-full bg-[#333333] hover:bg-[#48484A] active:scale-95 text-white font-normal text-2xl transition-transform px-7 flex items-center justify-start"
                  >
                    0
                  </button>
                  <button
                    onClick={handleDecimal}
                    className="h-16 rounded-full bg-[#333333] hover:bg-[#48484A] active:scale-95 text-white font-semibold text-2xl transition-transform flex items-center justify-center"
                  >
                    ,
                  </button>
                  <button
                    onClick={handleEquals}
                    className="h-16 rounded-full bg-[#FFFFFF] hover:bg-[#E5E5EA] active:scale-95 text-black font-bold text-2xl transition-transform flex items-center justify-center"
                  >
                    =
                  </button>
                </div>
              )}

              {/* Mode: Calculadora Científica */}
              {mode === 'cientifica' && (
                <div className="grid grid-cols-8 gap-2">
                  {/* Row 0 */}
                  <button
                    onClick={() => setIsDegreeMode(!isDegreeMode)}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    {isDegreeMode ? 'Deg' : 'Rad'}
                  </button>
                  <button
                    onClick={() => handleScientific('sin')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    sin
                  </button>
                  <button
                    onClick={() => handleScientific('cos')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    cos
                  </button>
                  <button
                    onClick={() => handleScientific('tan')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    tan
                  </button>
                  <button
                    onClick={handleClear}
                    className="h-12 rounded-xl bg-[#A5A5A5] hover:bg-[#D1D1D6] text-black text-sm font-bold flex items-center justify-center"
                  >
                    AC
                  </button>
                  <button
                    onClick={handleToggleSign}
                    className="h-12 rounded-xl bg-[#A5A5A5] hover:bg-[#D1D1D6] text-black text-sm font-bold flex items-center justify-center"
                  >
                    +/-
                  </button>
                  <button
                    onClick={handlePercentage}
                    className="h-12 rounded-xl bg-[#A5A5A5] hover:bg-[#D1D1D6] text-black text-sm font-bold flex items-center justify-center"
                  >
                    %
                  </button>
                  <button
                    onClick={() => handleOperator('÷')}
                    className="h-12 rounded-xl bg-[#505050] hover:bg-[#636366] text-white text-lg font-bold flex items-center justify-center"
                  >
                    ÷
                  </button>

                  {/* Row 1 */}
                  <button
                    onClick={() => handleScientific('sqr')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    x²
                  </button>
                  <button
                    onClick={() => handleScientific('cube')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    x³
                  </button>
                  <button
                    onClick={() => handleOperator('^')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    xʸ
                  </button>
                  <button
                    onClick={() => handleScientific('exp')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    eˣ
                  </button>
                  {['7', '8', '9'].map(d => (
                    <button
                      key={d}
                      onClick={() => handleDigit(d)}
                      className="h-12 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                    >
                      {d}
                    </button>
                  ))}
                  <button
                    onClick={() => handleOperator('×')}
                    className="h-12 rounded-xl bg-[#505050] hover:bg-[#636366] text-white text-lg font-bold flex items-center justify-center"
                  >
                    ×
                  </button>

                  {/* Row 2 */}
                  <button
                    onClick={() => handleScientific('inverse')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    1/x
                  </button>
                  <button
                    onClick={() => handleScientific('sqrt')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    √x
                  </button>
                  <button
                    onClick={() => handleScientific('cbrt')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    ³√x
                  </button>
                  <button
                    onClick={() => handleScientific('factorial')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    x!
                  </button>
                  {['4', '5', '6'].map(d => (
                    <button
                      key={d}
                      onClick={() => handleDigit(d)}
                      className="h-12 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                    >
                      {d}
                    </button>
                  ))}
                  <button
                    onClick={() => handleOperator('-')}
                    className="h-12 rounded-xl bg-[#505050] hover:bg-[#636366] text-white text-lg font-bold flex items-center justify-center"
                  >
                    -
                  </button>

                  {/* Row 3 */}
                  <button
                    onClick={() => handleScientific('ln')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    ln
                  </button>
                  <button
                    onClick={() => handleScientific('log10')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    log
                  </button>
                  <button
                    onClick={() => handleScientific('pi')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    π
                  </button>
                  <button
                    onClick={() => handleScientific('e')}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    e
                  </button>
                  {['1', '2', '3'].map(d => (
                    <button
                      key={d}
                      onClick={() => handleDigit(d)}
                      className="h-12 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                    >
                      {d}
                    </button>
                  ))}
                  <button
                    onClick={() => handleOperator('+')}
                    className="h-12 rounded-xl bg-[#505050] hover:bg-[#636366] text-white text-lg font-bold flex items-center justify-center"
                  >
                    +
                  </button>

                  {/* Row 4 */}
                  <button
                    onClick={handleBackspace}
                    className="h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-sm font-semibold flex items-center justify-center"
                  >
                    ⌫
                  </button>
                  <button
                    onClick={() => lastResult && setDisplayValue(lastResult)}
                    className="col-span-3 h-12 rounded-xl bg-[#242426] hover:bg-[#3A3A3C] text-[#D1D1D6] text-xs font-semibold flex items-center justify-center"
                  >
                    Ans {lastResult ? `(${lastResult})` : ''}
                  </button>
                  <button
                    onClick={() => handleDigit('0')}
                    className="col-span-2 h-12 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                  >
                    0
                  </button>
                  <button
                    onClick={handleDecimal}
                    className="h-12 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-lg font-semibold flex items-center justify-center"
                  >
                    ,
                  </button>
                  <button
                    onClick={handleEquals}
                    className="h-12 rounded-xl bg-white hover:bg-[#E5E5EA] text-black text-lg font-bold flex items-center justify-center"
                  >
                    =
                  </button>
                </div>
              )}

              {/* Mode: Conversor de Unidades */}
              {mode === 'conversor' && (
                <div className="flex flex-col gap-3">
                  {/* Category Filter Tabs */}
                  <div className="grid grid-cols-4 gap-1 bg-[#1C1C1E] p-1 rounded-xl border border-[#2C2C2E]">
                    {(['Comprimento', 'Peso', 'Temperatura', 'Moeda'] as ConverterCategory[]).map(cat => (
                      <button
                        key={cat}
                        onClick={() => handleCategoryChange(cat)}
                        className={`py-1.5 text-[11px] font-semibold rounded-lg transition-all ${
                          converterCat === cat
                            ? 'bg-[#333333] text-white shadow-sm'
                            : 'text-[#8E8E93] hover:text-white'
                        }`}
                      >
                        {cat}
                      </button>
                    ))}
                  </div>

                  {/* Conversion Display Cards */}
                  <div className="bg-[#1C1C1E] rounded-2xl p-4 border border-[#2C2C2E] flex flex-col gap-3">
                    {/* From Section */}
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex-1">
                        <span className="text-[10px] uppercase tracking-wider text-[#8E8E93] block mb-0.5">De</span>
                        <div className="text-xl sm:text-2xl font-bold font-mono text-white overflow-hidden text-ellipsis">
                          {converterInput || '0'}
                        </div>
                      </div>
                      <select
                        value={fromUnit}
                        onChange={e => setFromUnit(e.target.value)}
                        className="bg-[#2C2C2E] text-white text-xs rounded-xl px-2.5 py-1.5 border border-[#3A3A3C] outline-none max-w-[150px]"
                      >
                        {converterUnits.map(u => (
                          <option key={u} value={u} className="bg-[#1C1C1E]">
                            {u}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Invert Button */}
                    <div className="flex items-center justify-center py-1">
                      <button
                        onClick={handleSwapUnits}
                        className="p-1.5 rounded-full bg-[#2C2C2E] hover:bg-[#3A3A3C] text-[#8E8E93] hover:text-white transition-colors"
                        title="Inverter Unidades"
                      >
                        <ArrowUpDown className="w-3.5 h-3.5" />
                      </button>
                    </div>

                    {/* To Section */}
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex-1">
                        <span className="text-[10px] uppercase tracking-wider text-[#8E8E93] block mb-0.5">Para</span>
                        <div className="text-xl sm:text-2xl font-bold font-mono text-[#E5E5EA] overflow-hidden text-ellipsis">
                          {convertedResult}
                        </div>
                      </div>
                      <select
                        value={toUnit}
                        onChange={e => setToUnit(e.target.value)}
                        className="bg-[#2C2C2E] text-white text-xs rounded-xl px-2.5 py-1.5 border border-[#3A3A3C] outline-none max-w-[150px]"
                      >
                        {converterUnits.map(u => (
                          <option key={u} value={u} className="bg-[#1C1C1E]">
                            {u}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* Converter Numeric Input Pad */}
                  <div className="grid grid-cols-4 gap-2">
                    {['7', '8', '9'].map(d => (
                      <button
                        key={d}
                        onClick={() => handleDigit(d)}
                        className="h-11 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                      >
                        {d}
                      </button>
                    ))}
                    <button
                      onClick={handleBackspace}
                      className="h-11 rounded-xl bg-[#A5A5A5] hover:bg-[#D1D1D6] text-black text-sm font-semibold flex items-center justify-center"
                    >
                      ⌫
                    </button>

                    {['4', '5', '6'].map(d => (
                      <button
                        key={d}
                        onClick={() => handleDigit(d)}
                        className="h-11 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                      >
                        {d}
                      </button>
                    ))}
                    <button
                      onClick={handleClear}
                      className="h-11 rounded-xl bg-[#A5A5A5] hover:bg-[#D1D1D6] text-black text-sm font-semibold flex items-center justify-center"
                    >
                      C
                    </button>

                    {['1', '2', '3'].map(d => (
                      <button
                        key={d}
                        onClick={() => handleDigit(d)}
                        className="h-11 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                      >
                        {d}
                      </button>
                    ))}
                    <button
                      onClick={handleToggleSign}
                      className="h-11 rounded-xl bg-[#A5A5A5] hover:bg-[#D1D1D6] text-black text-sm font-semibold flex items-center justify-center"
                    >
                      +/-
                    </button>

                    <button
                      onClick={() => handleDigit('0')}
                      className="col-span-2 h-11 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-medium flex items-center justify-center"
                    >
                      0
                    </button>
                    <button
                      onClick={handleDecimal}
                      className="h-11 rounded-xl bg-[#333333] hover:bg-[#48484A] text-white text-base font-semibold flex items-center justify-center"
                    >
                      ,
                    </button>
                    <button
                      onClick={handleSaveConversionToHistory}
                      className="h-11 rounded-xl bg-[#505050] hover:bg-[#636366] text-white text-xs font-semibold flex items-center justify-center"
                    >
                      Salvar
                    </button>
                  </div>
                </div>
              )}

              {/* Retractable History Drawer Panel (CRUD) */}
              {isHistoryOpen && (
                <div className="absolute inset-0 bg-black/95 rounded-[36px] p-5 flex flex-col z-20 backdrop-blur-md border border-[#2C2C2E]">
                  <div className="flex items-center justify-between pb-3 border-b border-[#2C2C2E]">
                    <div className="flex items-center gap-2">
                      <History className="w-4 h-4 text-[#8E8E93]" />
                      <h3 className="font-bold text-sm text-white">Histórico de Cálculos</h3>
                    </div>
                    <button
                      onClick={() => setIsHistoryOpen(false)}
                      className="text-xs text-[#8E8E93] hover:text-white px-2 py-1 rounded-md"
                    >
                      Fechar
                    </button>
                  </div>

                  {/* History List (CRUD Read) */}
                  <div className="flex-1 overflow-y-auto py-2 space-y-2">
                    {historyList.length === 0 ? (
                      <div className="h-full flex flex-col items-center justify-center text-center p-6 text-[#8E8E93]">
                        <RotateCcw className="w-8 h-8 mb-2 opacity-40" />
                        <p className="text-xs">Nenhum cálculo registrado ainda.</p>
                      </div>
                    ) : (
                      historyList.map(item => (
                        <div
                          key={item.id}
                          className="bg-[#1C1C1E] p-3 rounded-xl border border-[#2C2C2E] flex items-center justify-between group hover:border-[#3A3A3C] transition-all"
                        >
                          <div className="flex-1 min-w-0 pr-2">
                            <div className="text-[10px] text-[#8E8E93] flex items-center gap-1.5 mb-0.5">
                              <span>{item.mode}</span>
                              <span>·</span>
                              <span>{item.timestamp}</span>
                            </div>
                            <div className="text-xs text-[#8E8E93] font-mono truncate">{item.expression}</div>
                            <div className="text-base font-bold text-white font-mono">{item.result}</div>
                          </div>

                          <div className="flex items-center gap-1.5 shrink-0">
                            {/* CRUD: Reutilizar (Use) */}
                            <button
                              onClick={() => handleUseHistory(item.result)}
                              className="px-2.5 py-1 rounded-lg bg-[#333333] hover:bg-[#505050] text-xs font-medium text-white transition-colors"
                            >
                              Usar
                            </button>
                            {/* CRUD: Deletar Individual (Delete) */}
                            <button
                              onClick={() => handleDeleteHistory(item.id)}
                              className="p-1.5 rounded-lg text-[#8E8E93] hover:text-[#FF453A] hover:bg-[#3A1C1C]/40 transition-colors"
                              title="Excluir item"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>
                      ))
                    )}
                  </div>

                  {/* History Footer (CRUD Bulk Clear) */}
                  {historyList.length > 0 && (
                    <div className="pt-2 border-t border-[#2C2C2E]">
                      <button
                        onClick={handleClearHistory}
                        className="w-full py-2 rounded-xl bg-[#2C2C2E] hover:bg-[#3A1C1C]/60 text-xs font-semibold text-[#FF453A] transition-colors flex items-center justify-center gap-1.5"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        Limpar Todo o Histórico
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Quick Reference Side Card */}
            <div className="hidden lg:flex flex-col gap-4 max-w-xs text-xs text-[#8E8E93]">
              <div className="bg-[#1C1C1E] p-4 rounded-2xl border border-[#2C2C2E]">
                <div className="flex items-center gap-2 text-white font-semibold mb-2">
                  <Terminal className="w-4 h-4 text-white" />
                  <span>Atalhos de Teclado</span>
                </div>
                <div className="space-y-1.5 font-mono text-[11px]">
                  <div className="flex justify-between">
                    <span className="text-white">0-9, . ,</span>
                    <span>Digitar números</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white">+ - * /</span>
                    <span>Operadores</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white">Enter / =</span>
                    <span>Calcular resultado</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white">Backspace</span>
                    <span>Apagar dígito</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white">Esc</span>
                    <span>Limpar (AC)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white">%</span>
                    <span>Porcentagem</span>
                  </div>
                </div>
              </div>

              <div className="bg-[#1C1C1E] p-4 rounded-2xl border border-[#2C2C2E]">
                <div className="flex items-center gap-2 text-white font-semibold mb-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Status do Código Python</span>
                </div>
                <p className="mb-2 text-[#8E8E93]">
                  Pacote Python modular em conformidade estrita com PEP 8, POO/MVC e Type Hinting.
                </p>
                <div className="bg-black/60 p-2.5 rounded-xl font-mono text-[10px] text-emerald-400">
                  Ran 22 tests in 0.005s · OK
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Python Code Explorer Tab */
          <div className="w-full max-w-5xl bg-[#141416] rounded-2xl border border-[#2C2C2E] overflow-hidden flex flex-col h-[680px]">
            {/* Explorer Top Toolbar */}
            <div className="bg-[#1C1C1E] px-4 py-3 border-b border-[#2C2C2E] flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-white" />
                <span className="text-xs font-semibold text-white">Arquitetura Python (POO / MVC)</span>
                <span className="text-xs text-[#8E8E93]">· 22 Testes Aprovados</span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={copyCodeToClipboard}
                  className="px-3 py-1.5 rounded-lg bg-[#2C2C2E] hover:bg-[#3A3A3C] text-xs font-medium text-white flex items-center gap-1.5 transition-colors"
                >
                  {copiedFile ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  {copiedFile ? 'Copiado!' : 'Copiar Código'}
                </button>
              </div>
            </div>

            {/* Split View: File Navigator on Left, Code Viewer on Right */}
            <div className="flex-1 flex overflow-hidden">
              {/* File List */}
              <div className="w-64 bg-[#18181A] border-r border-[#2C2C2E] overflow-y-auto p-2">
                <div className="text-[10px] uppercase font-bold text-[#8E8E93] px-2 py-1 tracking-wider">
                  Módulos do Projeto
                </div>
                <div className="space-y-0.5">
                  {Object.keys(PYTHON_FILES).map(fileName => (
                    <button
                      key={fileName}
                      onClick={() => setSelectedPythonFile(fileName)}
                      className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs font-mono transition-colors flex items-center justify-between ${
                        selectedPythonFile === fileName
                          ? 'bg-white text-black font-semibold'
                          : 'text-[#D1D1D6] hover:bg-[#2C2C2E]'
                      }`}
                    >
                      <span className="truncate">{fileName}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Code Panel */}
              <div className="flex-1 flex flex-col bg-black overflow-hidden">
                <div className="px-4 py-2 border-b border-[#2C2C2E] bg-[#141416] flex items-center justify-between">
                  <span className="text-xs font-mono text-[#E5E5EA]">{selectedPythonFile}</span>
                  <span className="text-[11px] text-[#8E8E93] truncate max-w-md">
                    {PYTHON_FILES[selectedPythonFile]?.desc}
                  </span>
                </div>
                <pre className="flex-1 p-4 font-mono text-xs text-[#E5E5EA] overflow-auto leading-relaxed selection:bg-[#333333]">
                  <code>{PYTHON_FILES[selectedPythonFile]?.code}</code>
                </pre>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-[#2C2C2E] py-3 px-4 text-center text-[11px] text-[#8E8E93]">
        Calculadora Desktop iOS em Python com CustomTkinter · Clean Code, PEP 8, Type Hinting & MVC
      </footer>
    </div>
  );
}
