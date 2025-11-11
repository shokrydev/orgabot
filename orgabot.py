from thumbnail_curation import get_file_thumbnail_dict
from vlm_prompter import Prompter
from pathlib import Path
from typing import Dict
import json

class OrgaBot:
    def __init__(self, files_dir_path: str | Path, categories_filename: str = "categories.json", cache_path: str | Path = "~/.cache", model: str = 'qwen2.5vl:7b'):
        self.file_thumbnail_dict = get_file_thumbnail_dict(files_dir_path, cache_path)
        self.model = model

        with open(categories_filename, "r") as f:
            categories_json = json.load(f)

        self.categories = categories_json["categories"]
        self.vlm_prompter = Prompter(self.categories, model=self.model)

    def categorize_files(self) -> Dict[str, str | None]:
        """Categorizes files based on their thumbnails using VLM.
        
        Returns:
            categorized_files (Dict[str, str | None]): Dictionary mapping file names to their predicted categories or None if no thumbnail exists.
        """

        categorized_files = {}
        
        for file_name, thumbnail_path in self.file_thumbnail_dict.items():
            assert file_name not in categorized_files, f"Duplicate file name found: {file_name}"

            if thumbnail_path is not None:
                category = self.vlm_prompter.get_category(file_name, thumbnail_path)
                categorized_files[file_name] = category
            else:
                categorized_files[file_name] = None

        return categorized_files

if __name__ == "__main__":

    # Simple test example in local environment
    orgabot = OrgaBot(files_dir_path = '~/Documents/papers')
    categories = orgabot.categorize_files()
    for file_name, category in categories.items():
        print(f"{file_name}: {category}")