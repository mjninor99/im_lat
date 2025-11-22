from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json

#file_path_read = "farmers-protest-tweets-2021-2-4.json"

def read_local_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_tweet_count = Counter()
    date_user_count = defaultdict(Counter)

    for line in read_local_file(file_path):
        if not line.strip():
            continue
        
        try:
            tweet = json.loads(line)
            # Fecha
            date_str = tweet.get('date')
            if not date_str:
                continue

            tweet_date = datetime.fromisoformat(
                date_str.replace('Z', '+00:00')
            ).date()

            # Usuario
            user = tweet.get('user', {})
            username = user.get('username')
            if not username:
                continue

            # Contadores
            date_tweet_count[tweet_date] += 1
            date_user_count[tweet_date][username] += 1

        except Exception:
            continue

    # Top 10 fechas con más tweets
    top_10 = date_tweet_count.most_common(10)

    result = []
    for tweet_date, _ in top_10:
        top_user = date_user_count[tweet_date].most_common(1)[0][0]
        result.append((tweet_date, top_user))

    return result
