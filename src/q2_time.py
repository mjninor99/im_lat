from typing import List, Tuple
from collections import Counter
import json
import emoji

def read_local_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    emoji_counter = Counter()

    for line in read_local_file(file_path):

        line = line.strip()
        if not line or '{' not in line:
            continue  # filtro rápido: evita JSON inválidos

        try:
            tweet = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        # Extraer contenido
        content = tweet.get('renderedContent') or tweet.get('content')
        if not content:
            continue

        # Extraer emojis (lista de dicts)
        emojis_found = emoji.emoji_list(content)
        if emojis_found:
            # actualizar sin loop
            emoji_counter.update(e['emoji'] for e in emojis_found)

    return emoji_counter.most_common(10)