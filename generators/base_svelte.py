from pathlib import Path
from typing import Dict, Any
from .base_frontend import BaseFrontendGenerator


class BaseSvelteGenerator:
    """Base class for Svelte-specific generators"""
    
    def __init__(self, main_generator: 'SvelteFrontendGenerator'):
        self.main_generator = main_generator
        self.frontend_dir = main_generator.frontend_dir
        self.project_name = main_generator.project_name
        self.features = main_generator.features
    
    def write_file(self, file_path: Path, content: str) -> None:
        """Write content to file using main generator's method"""
        self.main_generator.write_file(file_path, content)
    
    def load_and_substitute_template(self, template_name: str, substitutions: Dict[str, Any]) -> str:
        """Load and substitute template using main generator's method"""
        return self.main_generator.load_and_substitute_template(template_name, substitutions)
    
    def get_common_substitutions(self) -> Dict[str, Any]:
        """Get common template substitutions"""
        return {
            'PROJECT_NAME': self.project_name,
            'project_name': self.project_name.lower(),
            'features': self.features,
        }