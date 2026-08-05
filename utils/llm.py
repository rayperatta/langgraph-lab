"""Fábrica de LLM para el lab.

3 modos (en orden de prioridad):
  1. LLM_BASE_URL + LLM_API_KEY + LLM_MODEL  -> cualquier endpoint OpenAI-compatible
  2. OPENROUTER_API_KEY                      -> OpenRouter con modelo gratis
  3. (sin env)                               -> FakeListChatModel offline, 0 coste

El modo FAKE responde de forma determinista: suficiente para aprender la
mecánica de chains, tools y grafos sin gastar un solo token.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm(temperature: float = 0):
    # --- Modo 1: endpoint OpenAI-compatible genérico ---
    if os.getenv("LLM_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url=os.environ["LLM_BASE_URL"],
            api_key=os.environ["LLM_API_KEY"],
            model=os.environ.get("LLM_MODEL", "kimi-for-coding"),
            temperature=temperature,
        )

    # --- Modo 2: OpenRouter (modelo gratis por defecto) ---
    if os.getenv("OPENROUTER_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            model=os.environ.get("LLM_MODEL", "meta-llama/llama-3.3-70b-instruct:free"),
            temperature=temperature,
        )

    # --- Modo 3: FAKE offline (default del lab) ---
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
    respuestas = [
        "Soy un LLM simulado. Respuesta determinista para aprender sin gastar tokens.",
    ]
    return FakeListChatModel(responses=respuestas * 50)  # cicla la lista


def modo_actual() -> str:
    if os.getenv("LLM_API_KEY"):
        return f"OpenAI-compatible ({os.environ.get('LLM_MODEL')})"
    if os.getenv("OPENROUTER_API_KEY"):
        return "OpenRouter"
    return "FAKE offline (0 coste)"


if __name__ == "__main__":
    print("Modo:", modo_actual())
