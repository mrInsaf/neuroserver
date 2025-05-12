import os
import subprocess
from diffusers import DiffusionPipeline
import torch
from huggingface_hub import login


def generate_model(prompt):
    login(token="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")

    # Настройка путей
    current_dir = os.path.dirname(__file__)  # Папка, где расположен этот скрипт
    stable_fast_3d_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'stable-fast-3d'))
    demo_files_dir = os.path.join(stable_fast_3d_dir, 'demo_files', 'examples')
    output_dir = os.path.join(demo_files_dir, 'output')
    input_image_path = os.path.join(demo_files_dir, 'generated_image.jpg')

    # Этап 1: Генерация 2D-изображения с помощью DeepFloyd
    try:
        print("Loading DeepFloyd model...")
        pipe = (DiffusionPipeline.from_pretrained(
            "DeepFloyd/IF-I-XL-v1.0",
            variant="fp16",
            torch_dtype=torch.float16,
            safety_checker=None
            )
        )
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

        # Генерация изображения
        print(f"Generating image for prompt: {prompt}")
        image = pipe(prompt).images[0]

        # Сохранение изображения в папку demo_files/examples
        os.makedirs(demo_files_dir, exist_ok=True)
        image.save(input_image_path)
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
