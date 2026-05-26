// Load shared library from Jenkins Global Trusted Pipeline Libraries.
// Name/version must match Jenkins configuration.
@Library('pytest-shared-lib@main') _

// Declarative pipeline entrypoint for this repository.
// Principal DevOps pipeline pattern:
//   Checkout → Build → Security Scan (Trivy) → Test
//   Security gate blocks test stage on CRITICAL CVEs.
//   Every stage uses a focused shared-library step (single responsibility).
pipeline {
  agent any

  options {
    timestamps()
    // Discard old builds: keep 10 runs + 10 artifact sets to save disk
    buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
  }

  // Build-time inputs exposed in Jenkins UI.
  parameters {
    string(
      name: 'PYTEST_WORKERS',
      defaultValue: '4',
      description: 'Number of pytest-xdist workers (2, 4, 8, auto)'
    )
    choice(
      name: 'TRIVY_EXIT_SEVERITY',
      choices: ['CRITICAL', 'CRITICAL,HIGH', 'HIGH', 'NONE'],
      description: 'Severity level that blocks the build. NONE = scan but never fail.'
    )
  }

  environment {
    IMAGE_NAME = 'pytest-parallel-performance-tests:ci'
    REPORT_DIR = 'reports'
  }

  stages {
    stage('Checkout') {
      steps {
        // Fetch repository revision for this build from SCM.
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        // Build the Docker image used for both security scanning and test execution.
        // Separate stage: build failure is distinct from scan/test failure in UI.
        buildDockerImage(
          imageName: env.IMAGE_NAME,
          dockerfile: 'Dockerfile'
        )
      }
    }

    stage('Security Scan (Trivy)') {
      steps {
        // Trivy scans the built image before tests ever run.
        // Produces: JSON report, SARIF (GitHub Security tab), SBOM (CycloneDX).
        // exitOnSeverity controls the gate: build fails only on these severities.
        trivyScanImage(
          imageName: env.IMAGE_NAME,
          reportDir: "${env.REPORT_DIR}/security",
          exitOnSeverity: params.TRIVY_EXIT_SEVERITY,
          trivyImage: 'aquasec/trivy:0.62.0'
        )
      }
    }

    stage('Run Performance Tests') {
      steps {
        // Run pytest performance suite inside the already-built Docker image.
        // Only reached if security gate passed.
        runPytestPerfInDocker(
          imageName: env.IMAGE_NAME,
          workers: params.PYTEST_WORKERS,
          reportDir: env.REPORT_DIR,
          dockerfile: 'Dockerfile'
        )
      }
    }
  }

  post {
    always {
      // Surface JUnit results in Jenkins build summary.
      junit testResults: "${REPORT_DIR}/junit.xml", allowEmptyResults: true
      // Archive all reports (test + security) for traceability.
      archiveArtifacts artifacts: "${REPORT_DIR}/**", allowEmptyArchive: true
    }
    failure {
      echo "Build failed. Check Security Scan stage for CVE gate failures or Test stage for pytest failures."
    }
    success {
      echo "All stages passed: image built, security gate cleared, tests green."
    }
  }
}
