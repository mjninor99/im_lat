from typing import List, Tuple
import json, emoji

def read_local_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Usar diccionario simple en lugar de Counter
       emoji_count = {}
       
       for line in read_local_file(file_path):
           if not line.strip():
               continue
           
           try:
               tweet = json.loads(line)
               
               content = tweet.get('renderedContent') or tweet.get('content', '')
               if not content:
                   continue
               
               # Extraer emojis
               emojis_found = emoji.emoji_list(content)
               
               # Actualizar contador manualmente
               for emoji_data in emojis_found:
                   emoji_char = emoji_data['emoji']
                   emoji_count[emoji_char] = emoji_count.get(emoji_char, 0) + 1
               
               # Limpiar referencias
               del tweet, content, emojis_found
               
           except (json.JSONDecodeError, KeyError, ValueError):
               continue
       
       # Ordenar y retornar top 10
       sorted_emojis = sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)[:10]
       return sorted_emojis