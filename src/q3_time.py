from typing import List, Tuple
from collections import Counter
import json
import re

def read_local_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    mention_counter = Counter()
       
    for line in read_local_file(file_path):
        if not line.strip():
            continue
        
        try:
            tweet = json.loads(line)
            
            # Primero intentar usar mentionedUsers (más confiable)
            mentioned_users = tweet.get('mentionedUsers')
            if mentioned_users:
                for user in mentioned_users:
                    username = user.get('username')
                    if username:
                        mention_counter[username] += 1
            else:
                # Fallback: extraer menciones del contenido con regex
                content = tweet.get('content', '') or tweet.get('renderedContent', '')
                if content:
                    # Buscar patrones @username
                    mentions = re.findall(r'@(\w+)', content)
                    for username in mentions:
                        mention_counter[username] += 1
            
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    
    # Retornar top 10 usuarios más mencionados
    return mention_counter.most_common(10)