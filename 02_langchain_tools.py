"""LECCIÓN 02 — Tools: cómo el modelo "usa herramientas"

Conceptos:
  - @tool convierte una función Python en herramienta invocable por el LLM
  - llm.bind_tools(tools): el modelo aprende qué tools existen
  - El LLM NO ejecuta nada: solo DEVUELVE una petición (tool_call).
    Tú (o un agente) decides ejecutarla. Esto es clave para entender agentes.

Ejecuta:  python 02_langchain_tools.py
"""
from langchain_core.tools import tool
from utils.llm import get_llm, modo_actual

print(f"🔌 Modo LLM: {modo_actual()}\n")


# --- 1. Definir tools: función + docstring + type hints --------------------
# El docstring ES la descripción que ve el modelo. Escríbelo bien.
@tool
def sumar(a: float, b: float) -> float:
    """Suma dos números y devuelve el resultado."""
    return a + b


@tool
def clima(ciudad: str) -> str:
    """Devuelve el clima actual de una ciudad (simulado)."""
    datos = {"lisboa": "22°C soleado", "madrid": "31°C despejado"}
    return datos.get(ciudad.lower(), f"sin datos de {ciudad}")


tools = [sumar, clima]

# --- 2. Inspeccionar qué ve el modelo --------------------------------------
print("1) Definición que recibe el LLM:")
for t in tools:
    print(f"   - {t.name}({t.args}): {t.description}")
print()

# --- 3. bind_tools + invoke -------------------------------------------------
llm = get_llm()
llm_con_tools = llm.bind_tools(tools)

msg = llm_con_tools.invoke("¿Cuánto es 15.5 + 4.5 y qué clima hace en Lisboa?")

print("2) Respuesta del modelo:")
print("   content:    ", repr(msg.content))
print("   tool_calls: ", msg.tool_calls, "\n")

# --- 4. Ejecutar los tool_calls manualmente --------------------------------
# El LLM pidió; NOSOTROS ejecutamos. Este bucle (pedir->ejecutar->devolver)
# es exactamente lo que un agente de LangGraph automatiza (lección 05).
mapa_tools = {t.name: t for t in tools}
print("3) Ejecutando tool_calls:")
for call in msg.tool_calls:
    fn = mapa_tools[call["name"]]
    resultado = fn.invoke(call["args"])
    print(f"   {call['name']}{call['args']} -> {resultado}")

# Nota: en modo FAKE no hay tool_calls (el fake no sabe usar tools).
# Pon un LLM real en .env para ver el flujo completo.

# 🧠 EJERCICIO: crea una tool `convertir_moneda(cantidad, de, a)` con tipos
# y docstring claro. Comprueba con `convertir_moneda.args` qué schema genera.
