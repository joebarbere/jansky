# CASA-enabled image for the radio interferometry chapter (Chapter 12).
#
# CASA's modular packages (casatools/casatasks) only support specific Python
# versions and pull in large binary dependencies, which is exactly why we keep
# them out of the main environment and in this dedicated container.
FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="jansky-casa" \
      org.opencontainers.image.description="CASA + jansky for VLA imaging (Chapter 12)"

# CASA runtime needs a handful of system libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgfortran5 \
        libgomp1 \
        libgl1 \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Modular CASA + the analysis stack used in the imaging notebook.
RUN pip install --no-cache-dir \
        casatools \
        casatasks \
        casadata \
        numpy \
        matplotlib \
        astropy \
        jupyterlab

COPY notebooks/12_vla_imaging.ipynb ./notebooks/12_vla_imaging.ipynb
COPY data ./data

ENV JANSKY_DATA_DIR=/workspace/data
EXPOSE 8889

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8889", "--no-browser", \
     "--allow-root", "--ServerApp.token=", "--ServerApp.password="]
