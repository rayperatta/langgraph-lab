# LangGraph Lab 🧪

Proyecto para aprender **LangChain + LangGraph** de forma progresiva y práctica.
Cada archivo es una lección autocontenida, corta y muy comentada (en español).
Objetivo: entender los conceptos ejecutando código real, no leyendo teoría.

> ⚡ **¿Solo quieres lo esencial?** Lee [`CHEATSHEET.md`](CHEATSHEET.md) — todos
> los conceptos que importan en 1 página, en 10 minutos.

## Ruta de aprendizaje

**Núcleo (01–05)** — esto es el 90% de lo que se usa en la vida real:

| # | Archivo | Concepto clave |
|---|---------|----------------|
| 01 | `01_langchain_basico.py` | LLM, prompts, chains (LCEL) |
| 02 | `02_langchain_tools.py` | Tools y cómo el modelo las invoca |
| 03 | `03_langgraph_estado.py` | StateGraph: estado, nodos y edges |
| 04 | `04_langgraph_condicional.py` | Edges condicionales (routers) |
| 05 | `05_langgraph_agente.py` | Agente ReAct con tools en un grafo |

**Opcional (06–07)** — útil saber que existe, no esencial para empezar:

| # | Archivo | Concepto clave |
|---|---------|----------------|
| 06 | `06_langgraph_memoria.py` | Checkpoints, threads y memoria |
| 07 | `07_langgraph_humano.py` | Human-in-the-loop (interrupt) |

Regla de oro: **ejecuta cada lección, rompe cosas, modifícala**. Se aprende en 20 min por archivo.
Los ejercicios 🧠 del final de cada lección son **opcionales** — hazlos solo si quieres profundizar.

## Setup

```bash
cd ~/Projects/langgraph-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## LLM: 3 modos (definido en `utils/llm.py`)

1. **Fake (default, 0 coste, offline)** — no configuras nada. Un modelo simulado
   que responde de forma determinista. Perfecto para aprender la *mecánica* de
   chains, grafos y agentes sin gastar tokens.
2. **OpenRouter** — copia `.env.example` a `.env` y pon `OPENROUTER_API_KEY`.
   Modelo gratis por defecto (`meta-llama/llama-3.3-70b-instruct:free`).
3. **Kimi / OpenAI-compatible** — pon `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`
   en `.env` (cualquier endpoint compatible con la API de OpenAI).

## Ejecutar

```bash
python 01_langchain_basico.py
python 03_langgraph_estado.py
# etc. Cada lección imprime paso a paso lo que ocurre.
```

## Mapa mental

```
LangChain = piezas sueltas (prompts, modelos, tools, chains lineales)
LangGraph = orquestador (grafo de estados: nodos que transforman, edges que deciden)
Agente    = LangGraph + LLM que decide qué nodo/tool ejecutar en cada paso
```
