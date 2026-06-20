# GNU Radio + SDR image for the software-defined-radio chapters (5-6).
#
# These chapters are OPTIONAL and only needed if you want to process real
# RTL-SDR captures (or live hardware). GNU Radio and the osmosdr drivers are
# heavy and system-level, so they live here rather than in the core env.
#
# To use a real USB SDR you must pass the device through to the container, e.g.
#   podman run --device /dev/bus/usb -p 8890:8890 jansky-gnuradio
FROM debian:bookworm-slim

LABEL org.opencontainers.image.title="jansky-gnuradio" \
      org.opencontainers.image.description="GNU Radio + RTL-SDR for the SDR chapters (5-6)"

RUN apt-get update && apt-get install -y --no-install-recommends \
        gnuradio \
        gr-osmosdr \
        rtl-sdr \
        python3-pip \
        python3-numpy \
        python3-matplotlib \
        python3-scipy \
    && rm -rf /var/lib/apt/lists/*

# JupyterLab + pyrtlsdr on top of the system GNU Radio Python bindings.
# (Debian's externally-managed Python needs the break-system-packages flag.)
RUN pip install --no-cache-dir --break-system-packages \
        jupyterlab \
        pyrtlsdr \
        astropy

WORKDIR /workspace
COPY notebooks/05_sdr_basics.ipynb notebooks/06_hydrogen_line.ipynb ./notebooks/
COPY data ./data

ENV JANSKY_DATA_DIR=/workspace/data
EXPOSE 8890

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8890", "--no-browser", \
     "--allow-root", "--ServerApp.token=", "--ServerApp.password="]
