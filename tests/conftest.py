"""
conftest.py -- Shared test setup.

The analyzer reads Azure OpenAI settings before creating the (mocked) client,
so tests need placeholder values. These are fake and never reach Azure.
"""
import pytest


@pytest.fixture(autouse=True)
def fake_azure_env(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_KEY", "test-key")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
