from ollama import generate
from pydantic import BaseModel
        
class DocumentModel(BaseModel):
    language: str
    genre: str
    subgenre: str
    subject: str

def get_category(file_name: str, thumbnail_path: str, model: str = 'qwen2.5vl:7b') -> str:  
    """Prompts VLM with filename and thumbnail to generate file category.

    Args:
        file_name (str): Name of file to catogerize.
        thumbnail_path (str): Path to file's thumbnail.
        model (str): Name of VLM in Ollama (default: 'qwen2.5vl:7b')

    Returns:
        predicted_category (str): File category predicted by VLM based on filename and thumbnail.
    """

    predicted_category = generate(
        model=model,
        system='You are an expert file categorization assistant. Given a filename and thumbnail, categorize the file into a single-word book genre, subgenre and language.',
        prompt=file_name,
        images=[thumbnail_path],
        stream=False,
        format=DocumentModel.model_json_schema(),
    )['response']

    return predicted_category


if __name__ == "__main__":
    import thumbnail_curation
    dic = thumbnail_curation.get_file_thumbnail_dict(files_dir_path = '~/Documents/papers')
    for fname, thumb_path in dic.items():
       print(fname, get_category(fname,thumb_path))