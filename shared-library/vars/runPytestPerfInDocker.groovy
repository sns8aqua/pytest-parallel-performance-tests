// runPytestPerfInDocker.groovy
// Runs the pytest performance suite inside a pre-built Docker image.
// Assumes buildDockerImage() has already run in a prior stage.
// Single responsibility: test execution only.

def call(Map cfg = [:]) {
  String imageName = cfg.get('imageName', 'pytest-parallel-performance-tests:ci')
  String workers   = "${cfg.get('workers', '4')}"
  String reportDir = cfg.get('reportDir', 'reports')

  sh """
    set -eu
    mkdir -p "${reportDir}"

    echo "=== Running pytest performance suite ==="
    echo "Image  : ${imageName}"
    echo "Workers: ${workers}"

    docker run --rm \\
      -e PYTEST_WORKERS="${workers}" \\
      -v "\$PWD/${reportDir}:/workspace/${reportDir}" \\
      "${imageName}"

    echo "=== Test run complete ==="
  """

  junit testResults: "${reportDir}/junit.xml", allowEmptyResults: true
  archiveArtifacts artifacts: "${reportDir}/*.log", allowEmptyArchive: true
}
