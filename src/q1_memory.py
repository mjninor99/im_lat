from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json

file_path_read = "farmers-protest-tweets-2021-2-4.json"

def read_local_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_tweet_count = {} 
    date_user_count = {}  
    
    for line in read_local_file(file_path_read):
        if not line.strip():
            continue
        
        try:
            tweet = json.loads(line)
            
            # Extraer fecha
            date_str = tweet.get('date')
            if not date_str:
                continue
            
            tweet_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
            
            # Extraer username
            username = tweet.get('user', {}).get('username')
            if not username:
                continue
            
            # Actualizar contadores (sin usar Counter para ahorrar memoria)
            date_tweet_count[tweet_date] = date_tweet_count.get(tweet_date, 0) + 1
            
            if tweet_date not in date_user_count:
                date_user_count[tweet_date] = {}
            date_user_count[tweet_date][username] = date_user_count[tweet_date].get(username, 0) + 1
            
            # Limpiar referencia al tweet inmediatamente
            del tweet
            
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    
    # Obtener top 10 fechas (ordenar manualmente)
    sorted_dates = sorted(date_tweet_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Para cada fecha, encontrar el usuario más activo
    result = []
    for tweet_date, _ in sorted_dates:
        if tweet_date in date_user_count:
            users = date_user_count[tweet_date]
            top_user = max(users.items(), key=lambda x: x[1])
            result.append((tweet_date, top_user[0]))
    
    return result
