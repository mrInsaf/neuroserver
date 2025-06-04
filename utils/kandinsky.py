import json
import time

import requests
import base64

class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f'{prompt}'
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, save_path, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                image_data = data['result']['files'][0]  # Получаем Base64 строку

                # Убираем префикс, если он есть (например: data:image/jpeg;base64,)
                if ',' in image_data:
                    image_data = image_data.split(',')[1]

                # Декодируем и сохраняем в файл
                image_bytes = base64.b64decode(image_data)
                filename = save_path
                with open(filename, 'wb') as f:
                    f.write(image_bytes)

                return filename  # Возвращаем имя файла

            attempts -= 1
            time.sleep(delay)
        return None
