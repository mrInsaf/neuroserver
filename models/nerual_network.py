import os
import subprocess
from diffusers import DiffusionPipeline
import torch
from huggingface_hub import login


# 🚀 Загрузка модели один раз при старте приложения
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# Загрузка PixArt-Sigma (легковесная альтернатива DeepFloyd)
pipe = DiffusionPipeline.from_pretrained(
    "PixArt-alpha/PixArt-Sigma-XL-2-1024-MS",
    torch_dtype=torch_dtype,
    use_safetensors=True
)

# 💡 Включаем xFormers для снижения потребления памяти
try:
    pipe.enable_xformers_memory_efficient_attention()
except ModuleNotFoundError:
    print("xFormers не установлен. Рекомендуется установить: pip install xformers")

# 📦 Переносим модель на устройство (GPU/CPU)
pipe = pipe.to(device)

# 📁 Настройка путей
current_dir = os.path.dirname(__file__)
stable_fast_3d_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'stable-fast-3d'))
demo_files_dir = os.path.join(stable_fast_3d_dir, 'demo_files', 'examples')
output_dir = os.path.join(demo_files_dir, 'output')
input_image_path = os.path.join(demo_files_dir, 'generated_image.jpg')

def generate_model(prompt):
    try:
        print(f"Generating image for prompt: {prompt}")
        image = pipe(prompt, height=1024, width=1024).images[0]

        # 📁 Сохраняем изображение
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
