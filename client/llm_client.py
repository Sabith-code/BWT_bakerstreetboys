from json import tool
from openai import AsyncOpenAI
from client.response import TextDelta
from client.response import TokenUsage
from client.response import StreamEvent
from typing import Any, AsyncGenerator
from client.response import StreamEventType
from openai import RateLimitError
from openai import APIConnectionError
from openai import APIError
import asyncio
import os
from pathlib import Path
class LLMClient:
    def __init__(self) -> None:
        self._client : AsyncOpenAI | None = None
        self._max_retries: int = 3
        self._load_env_file()

    def _load_env_file(self) -> None:
        env_path = Path(__file__).resolve().parents[1] / ".env"
        if not env_path.exists():
            return
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

    def _get_api_key(self) -> str:
        return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    
    def get_client(self)-> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self._get_api_key(),
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )
        return self._client

    def _get_candidate_models(self) -> list[str]:
        preferred_model = os.getenv("GEMINI_MODEL")
        fallback_models = [
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
            "gemini-2.5-flash",
        ]
        models: list[str] = []
        if preferred_model:
            models.append(self._normalize_model_name(preferred_model))
        for model in fallback_models:
            normalized = self._normalize_model_name(model)
            if normalized not in models:
                models.append(normalized)
        return models

    def _normalize_model_name(self, model_name: str) -> str:
        model = model_name.strip()
        if model.startswith("models/"):
            return model
        if "/" in model:
            model = model.split("/")[-1]
        return f"models/{model}"

    async def close(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None
    def _build_tools(self, tools: list[dict[str, Any]]):
        return [
            {
                "function_declarations": [
                    {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {
                            "type": "object",
                            "properties": {}
                        })
                    }
                ]
            }
            for tool in tools
        ]
    
    async def chat_completion(self, messages: list[dict[str, Any]] , stream:bool=True, tools: list[dict[str, Any]] | None = None) -> AsyncGenerator[StreamEvent, None]:
        if not self._get_api_key():
            yield StreamEvent(
                type=StreamEventType.ERROR,
                error="Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your current terminal session or in .env.",
            )
            return
        client = self.get_client()
        last_error: str | None = None
        for model in self._get_candidate_models():
            kwargs = {
                "model": model,
                "messages": messages,
                "stream": stream,
            }
            for attempt in range(self._max_retries + 1):
                try:
                    if stream:
                        async for event in self._stream_response(client, kwargs):
                            yield event
                    else:
                        event = await self._non_stream_response(client, kwargs)
                        yield event
                    return
                except RateLimitError as e:
                    error_text = str(e)
                    last_error = error_text
                    if "limit: 0" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                        break
                    if attempt < self._max_retries:
                        wait_time = 2**attempt
                        await asyncio.sleep(wait_time)
                    else:
                        break
                except APIConnectionError as e:
                    if attempt < self._max_retries:
                        wait_time = 2**attempt
                        await asyncio.sleep(wait_time)
                    else:
                        yield StreamEvent(
                            type=StreamEventType.ERROR,
                            error=f" API connection error:  {e}"
                        )
                        return
                except APIError as e:
                    error_text = str(e)
                    last_error = error_text
                    if "unexpected model name format" in error_text or "INVALID_ARGUMENT" in error_text:
                        break
                    if "404" in error_text or "NOT_FOUND" in error_text:
                        break
                    if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                        break
                    yield StreamEvent(
                        type=StreamEventType.ERROR,
                        error=f" API connection error:  {e}"
                    )
                    return

        details = f" ({last_error})" if last_error else ""
        yield StreamEvent(
            type=StreamEventType.ERROR,
            error=(
                "No usable Gemini model found for this API key/project. "
                "Set GEMINI_MODEL to a model available in your account, or wait/reset quota if rate-limited."
                f"{details}"
            ),
        )
        return
                    




    async def _stream_response(self,client: AsyncOpenAI, kwargs: dict[str, Any]) -> AsyncGenerator[StreamEvent,None]:
        response = await client.chat.completions.create(**kwargs)
        usage : TokenUsage | None = None
        finish_reason: str | None = None
        async for chunk in response:
            if hasattr(chunk, "usage") and chunk.usage:
                usage  = TokenUsage(
                prompt_tokens=chunk.usage.prompt_tokens,
                completion_tokens=chunk.usage.completion_tokens,
                total_tokens = chunk.usage.total_tokens,
                cached_tokens = chunk.usage.prompt_tokens_details.cached_tokens
                )
            if not chunk.choices:
                continue
            choice= chunk.choices[0]
            delta = choice.delta
            if choice.finish_reason:
                finish_reason = choice.finish_reason
            if delta.content:
                yield StreamEvent(
                    type=StreamEventType.TEXT_DELTA,
                    text_delta=TextDelta(delta.content)
                )

        yield StreamEvent(
            type=StreamEventType.MESSAGE_COMPLETE,
            finish_reason=finish_reason,
            usage=usage)

    async def _non_stream_response(self, client: AsyncOpenAI, kwargs: dict[str, Any]) -> StreamEvent:
        response = await client.chat.completions.create(**kwargs)
        choice  = response.choices[0]
        message = choice.message
        text_delta = None
        if message.content:
            text_delta = TextDelta(content=message.content)
        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens = response.usage.total_tokens,
                cached_tokens = response.usage.prompt_tokens_details.cached_tokens)
        return StreamEvent(
            type=StreamEventType.MESSAGE_COMPLETE,
            text_delta=text_delta,
            finish_reason=choice.finish_reason,
            usage=usage
        )