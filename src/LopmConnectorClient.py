import requests
import os
import itertools
from pydantic import HttpUrl


class LopmConnectorClient:

    duplicate_set = set() 
    def get_entities(self, last_run_index) -> dict:
        try:
            # 1. Сначала проверяем, есть ли файл локально. 
            # Если нет или он старый — скачиваем один раз целиком.
            if not os.path.exists("domainList.txt"):
                r = requests.get("https://phishing.army/download/phishing_army_blocklist.txt")
                # Сохраняем весь файл целиком
                with open("domainList.txt", "w") as f:
                    f.write(r.text[446:])

            block_list = []
            next_index = last_run_index
            limit = 100000 # Твой лимит

            with open("domainList.txt", "r") as f:
                # Читаем все строки
                all_lines = f.readlines()
                
                # Берем кусок от last_run_index до last_run_index + limit
                chunk = all_lines[last_run_index : last_run_index + limit]
                
                for line in chunk:
                    clean_line = line.strip()
                    if clean_line:
                        block_list.append(clean_line)
                
                # Вычисляем новый индекс для следующего запуска
                next_index = last_run_index + len(chunk)
                
                # Если файл закончился, можно обнулить индекс или удалить файл
                if next_index >= len(all_lines):
                    next_index = 0 
                    os.remove("domainList.txt")

            return block_list, next_index    
        
            raise NotImplementedError
        
        except Exception as e:
            # Печатаем саму ошибку, чтобы знать, что чинить
            print(f"Error in LopmClient: {e}")
            # Возвращаем текущий индекс и пустой список, чтобы коннектор не упал
            return [], last_run_index