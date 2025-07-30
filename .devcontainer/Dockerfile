FROM archlinux:latest

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm base-devel python python-pip python-virtualenv jupyter-notebook \
                           git gcc pkgconf cmake ffmpeg 

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm sudo && \
    useradd --create-home --shell /bin/bash --groups wheel vscode && \
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER vscode


CMD [ "/bin/bash" ]