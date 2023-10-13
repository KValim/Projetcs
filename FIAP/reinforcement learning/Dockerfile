# Usamos uma imagem base do Python 3.10 no Ubuntu 22.04
FROM python:3.10-slim-bullseye

# Mantenedor (opcional, mas uma boa prática)
LABEL maintainer="kaiquevalim23@gmail.com"

# Evite perguntas interativas de apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Atualize o sistema e instale os pacotes necessários
RUN apt-get update && apt-get install -y \
    ffmpeg \
    xvfb \
    gcc \
    python3-dev \
    build-essential

# Instale o Jupyter Notebook e outras bibliotecas Python
RUN pip install --no-cache-dir \
    jupyter \
    gym==0.24 \
    pygame \
    numpy \
    huggingface_hub \
    pickle5 \
    pyyaml==6.0 \
    imageio \
    imageio_ffmpeg \
    pyglet==1.5.1 \
    tqdm \
    xvfbwrapper \
    pyvirtualdisplay

# Exponha a porta padrão do Jupyter Notebook
EXPOSE 8888

# Comando padrão para iniciar o Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]