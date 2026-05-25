FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY tests ./tests

CMD ["sh", "-c", "set -eu; mkdir -p reports; pytest tests/performance -n ${PYTEST_WORKERS:-4} -v --durations=10 --tb=short --junitxml=reports/junit.xml | tee reports/pytest.log"]
