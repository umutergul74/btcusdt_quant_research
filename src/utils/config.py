import os
import yaml
from typing import Any, Dict

class Config:
    """Config manager that loads YAML files and provides access to settings."""
    def __init__(self, project_root: str = "/content/drive/MyDrive/btcusdt_quant_research"):
        self.project_root = project_root
        self.config_dir = os.path.join(project_root, "configs")
        self.settings: Dict[str, Any] = {}
        self.load_all_configs()

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Loads a YAML file safely."""
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r") as f:
            try:
                return yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Error loading {file_path}: {e}")
                return {}

    def load_all_configs(self):
        """Loads all YAML files under configs/ and merges them."""
        config_files = [
            "data_config.yaml",
            "feature_config.yaml",
            "labeling_config.yaml",
            "model_config.yaml",
            "validation_config.yaml",
            "backtest_config.yaml",
            "risk_config.yaml",
            "github_config.yaml"
        ]
        for filename in config_files:
            name = filename.replace("_config.yaml", "")
            path = os.path.join(self.config_dir, filename)
            if not os.path.exists(path):
                # Fallback to local workspace paths if running locally or before Drive is mounted
                path = os.path.join(os.getcwd(), "configs", filename)
            self.settings[name] = self.load_yaml(path)

    def get(self, section: str, key: str = None, default: Any = None) -> Any:
        """Retrieves a setting by section and key."""
        section_data = self.settings.get(section, {})
        if key is None:
            return section_data
        return section_data.get(key, default)

def load_global_config(project_root: str = "/content/drive/MyDrive/btcusdt_quant_research") -> Config:
    """Loads and returns the global configuration object."""
    return Config(project_root)
