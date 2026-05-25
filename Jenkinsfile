pipeline {
  agent any

  options {
    timestamps()
  }

  parameters {
    string(name: 'PYTEST_WORKERS', defaultValue: '4', description: 'Number of pytest-xdist workers (for example: 2, 4, 8, auto)')
  }

  environment {
    VENV_DIR = '.venv'
    REPORT_DIR = 'reports'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set Up Python') {
      steps {
        sh '''
          set -eu
          python3 -m venv "$VENV_DIR"
          . "$VENV_DIR/bin/activate"
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run Performance Tests') {
      steps {
        sh '''
          set -eu
          mkdir -p "$REPORT_DIR"
          . "$VENV_DIR/bin/activate"
          pytest tests/performance \
            -n "$PYTEST_WORKERS" \
            -v \
            --durations=10 \
            --tb=short \
            --junitxml="$REPORT_DIR/junit.xml" | tee "$REPORT_DIR/pytest.log"
        '''
      }
    }
  }

  post {
    always {
      junit testResults: 'reports/junit.xml', allowEmptyResults: true
      archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
    }
  }
}
