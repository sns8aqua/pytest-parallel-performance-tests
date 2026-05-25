// Load shared library from Jenkins Global Trusted Pipeline Libraries.
// Name/version must match Jenkins configuration.
@Library('pytest-shared-lib@main') _

// Declarative pipeline entrypoint for this repository.
pipeline {
  // Run on any available Jenkins agent (local node for your current setup).
  agent any

  // Global pipeline options applied to all stages.
  options {
    // Prefix console logs with wall-clock timestamps for easier debugging.
    timestamps()
  }

  // Build-time inputs exposed in Jenkins UI.
  parameters {
    // Controls pytest-xdist parallel workers passed to shared library step.
    // Examples: 2, 4, 8, auto
    string(name: 'PYTEST_WORKERS', defaultValue: '4', description: 'Number of pytest-xdist workers (for example: 2, 4, 8, auto)')
  }

  // Ordered stages for the CI workflow.
  stages {
    stage('Checkout') {
      steps {
        // Fetch the repository revision for this build from SCM.
        checkout scm
      }
    }

    stage('Run Performance Tests Through Shared Library') {
      steps {
        // Reusable shared-library step that:
        // 1) verifies Docker availability
        // 2) builds Docker image from Dockerfile
        // 3) runs pytest performance suite in container
        // 4) publishes JUnit and archives reports/* artifacts
        runPytestPerfInDocker(
          imageName: 'pytest-parallel-performance-tests:ci',
          workers: params.PYTEST_WORKERS,
          reportDir: 'reports',
          dockerfile: 'Dockerfile'
        )
      }
    }
  }

  // Post actions always run regardless of stage success/failure.
  post {
    always {
      script {
        // Publishing is intentionally centralized inside the shared step,
        // which keeps Jenkinsfile thin and reusable across repositories.
        echo 'Artifacts and JUnit publishing are handled by shared library step.'
      }
    }
  }
}
