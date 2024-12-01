from pydantic import BaseModel
import yaml

class NormConfig(BaseModel):
    max_tokens: int
    temperature: int | float
    top_p: int | float
    stop_sequences: list[str]

class ConfigTranslator:
    # Cache for config object
    PROVIDERS_CONFIG_MAPPING = None

    @classmethod
    def set_essentials(cls) -> dict:
        """
        
        Method to read the Provider class generation configuration and NormConfig mappings

        Returns:
        --------
            dict: Mapping between Provider's generation configuration and NormConfig
        
        """
        return yaml.safe_load("aisuite/config_translator/providers_config.yml")

    def __init__(self):
        # Caching the translation mapping
        if ConfigTranslator.PROVIDERS_CONFIG_MAPPING is None: 
            ConfigTranslator.PROVIDERS_CONFIG_MAPPING = ConfigTranslator.set_essentials()
    
    def translate(self, provider_object: object, norm_config: dict) -> dict:
        """
        
        Method to translate the user given generation config to actual Provider's configuration

        Args:
        -----
            provider_object: Object of the Providers' class
            norm_config: User given generation config where fields are from NormConfig
        
        Returns:
        --------

        """

        provider_name = provider_object.__class__.__name__
        translation_mapping = ConfigTranslator.PROVIDERS_CONFIG_MAPPING[provider_name]

        provider_config = {
            provider_field: norm_config[norm_field]
            for provider_field, norm_field in translation_mapping if norm_field in norm_config
        }

        return provider_config
    