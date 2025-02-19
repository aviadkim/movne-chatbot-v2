import os
import pytest
from app.core.config import Settings
from huggingface_hub import HfApi
from transformers import AutoTokenizer, AutoModelForCausalLM

def test_huggingface_token_in_env():
    """Test if HUGGINGFACE_TOKEN is properly set in environment"""
    token = os.getenv('HUGGINGFACE_TOKEN')
    assert token is not None, "HUGGINGFACE_TOKEN not found in environment variables"
    assert len(token) > 0, "HUGGINGFACE_TOKEN is empty"

def test_settings_token_loading():
    """Test if Settings class properly loads the token"""
    settings = Settings()
    assert settings.HUGGINGFACE_TOKEN is not None, "Settings failed to load HUGGINGFACE_TOKEN"
    assert len(settings.HUGGINGFACE_TOKEN) > 0, "Settings loaded an empty HUGGINGFACE_TOKEN"

def test_huggingface_api_authentication():
    """Test if the token can authenticate with Hugging Face API"""
    settings = Settings()
    api = HfApi()
    try:
        user = api.whoami(token=settings.HUGGINGFACE_TOKEN)
        assert user is not None, "Failed to authenticate with Hugging Face API"
    except Exception as e:
        pytest.fail(f"Authentication failed: {str(e)}")

def test_model_tokenizer_loading():
    """Test if the model and tokenizer can be loaded with the token"""
    settings = Settings()
    model_name = "facebook/xglm-7.5B"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=settings.HUGGINGFACE_TOKEN,
            use_fast=True
        )
        assert tokenizer is not None, "Failed to load tokenizer"
    except Exception as e:
        pytest.fail(f"Tokenizer loading failed: {str(e)}")

    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=settings.HUGGINGFACE_TOKEN,
            torch_dtype="auto",
            device_map="auto"
        )
        assert model is not None, "Failed to load model"
    except Exception as e:
        pytest.fail(f"Model loading failed: {str(e)}")