import os
import subprocess
import torch
from huggingface_hub import login

from utils.kandinsky import FusionBrainAPI

login(token="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")


# 📁 Настройка путей
current_dir = os.path.dirname(__file__)
stable_fast_3d_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'stable-fast-3d'))
demo_files_dir = os.path.join(stable_fast_3d_dir, 'demo_files', 'examples')
output_dir = os.path.join(demo_files_dir, 'output')
input_image_path = os.path.join(demo_files_dir, 'generated_image.jpg')

def generate_model(prompt):
    # Этап 1 генерация изображения
    try:
        correct_prompt = f"{prompt} on white background"
        print(f"Generating image for prompt: {correct_prompt}")

        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', 'D0681623CF84256B48952B6167A13C72',
                             'CEEC564CF61B94990B929FBC9753B969')
        pipeline_id = api.get_pipeline()
        uuid = api.generate("gnome on white background", pipeline_id)

        os.makedirs(demo_files_dir, exist_ok=True)

        api.check_generation(uuid, input_image_path)
        print(f"Image saved to {input_image_path}")
    except Exception as e:
        return f"Error during image generation: {str(e)}"

    # Этап 2: Генерация 3D-модели с помощью Stable Fast 3D
    try:
        # Путь к скрипту run.py
        script_path = os.path.join(stable_fast_3d_dir, 'run.py')

        # Настройка параметров команды
        pretrained_model = 'stabilityai/stable-fast-3d'
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        texture_resolution = 512
        batch_size = 1

        # Команда для запуска Stable Fast 3D
        command = [
            'python', script_path,
            '--device', device,
            '--pretrained-model', pretrained_model,
            '--output-dir', output_dir,
            '--texture-resolution', str(texture_resolution),
            '--batch_size', str(batch_size),
            input_image_path
        ]

        print(f"Running Stable Fast 3D with command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print("3D model generation successful!")
            return f"3D model generated successfully! Output saved to {output_dir}"
        else:
            return f"Error during 3D model generation: {result.stderr}"
    except Exception as e:
        return f"Error during 3D model generation: {str(e)}"
