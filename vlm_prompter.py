from ollama import generate
from typing import List

class Prompter:
    def __init__(self, categories: List[str], model: str = 'qwen2.5vl:7b'):
        self.categories = categories
        self.system_prompt = f'You are an expert file categorizer. Given a filename and thumbnail, respond only to which one of the following categories the file belongs: {", ".join(self.categories)}'
        self.model = model

    def get_category(self, file_name: str, thumbnail_path: str) -> str:  
        """Prompts VLM with filename and thumbnail to generate file category.

        Args:
            file_name (str): Name of file to catogerize.
            thumbnail_path (str): Path to file's thumbnail.

        Returns:
            predicted_category (str): File category from self.categories predicted by VLM based on filename and thumbnail.
        """

        predicted_category = generate(
            model=self.model,
            system=self.system_prompt,
            prompt=file_name,
            images=[thumbnail_path],
            stream=False,
        )['response']

        assert predicted_category in self.categories, f"Predicted category '{predicted_category}' not in predefined categories."

        return predicted_category


if __name__ == "__main__":
    import thumbnail_curation
    dic = thumbnail_curation.get_file_thumbnail_dict(files_dir_path = '~/Documents/papers')

    categories  = [ '3D Vision', 'Computer Vision', 'Natural Language Processing', 'Self-Supervised Learning', 'Generative AI', 'Remote Sensing', 'Reinforcement Learning']

    prompter = Prompter(categories=categories)

    for fname, thumb_path in dic.items():
        if thumb_path is not None:
            print(fname, '---', prompter.get_category(fname,thumb_path))
        else:
            print(fname, '---' , 'No thumbnail provided.')