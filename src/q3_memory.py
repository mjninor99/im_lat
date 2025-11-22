from typing import List, Tuple
import json
import re

def read_local_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line
            
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # Usar diccionario simple
    mention_count = {}
    
    for line in read_local_file(file_path):
        if not line.strip():
            continue
        
        try:
            tweet = json.loads(line)
            
            # Procesar menciones
            mentioned_users = tweet.get('mentionedUsers')
            if mentioned_users:
                for user in mentioned_users:
                    username = user.get('username')
                    if username:
                        mention_count[username] = mention_count.get(username, 0) + 1
            else:
                content = tweet.get('content', '') or tweet.get('renderedContent', '')
                if content:
                    mentions = re.findall(r'@(\w+)', content)
                    for username in mentions:
                        mention_count[username] = mention_count.get(username, 0) + 1
            
            # Limpiar referencias inmediatamente
            del tweet
            
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    
    # Ordenar y retornar top 10
    sorted_mentions = sorted(mention_count.items(), key=lambda x: x[1], reverse=True)[:10]
    return sorted_mentions