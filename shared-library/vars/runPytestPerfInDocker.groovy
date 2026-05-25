def call(Map cfg = [:]) {
  String imageName = cfg.get('imageName', 'pytest-parallel-performance-tests:ci')
  String workers = "${cfg.get('workers', '4')}"
  String reportDir = cfg.get('reportDir', 'reports')
  String dockerfile = cfg.get('dockerfile', 'Dockerfile')

  sh """
    set -eu
    command -v docker >/dev/null 2>&1 || {
      echo "ERROR: docker CLI not found on Jenkins node PATH."
      echo "Fix node provisioning (service PATH / agent image), not pipeline code."
      exit 1
    }

    docker version --format 'Docker version {{.Client.Version}}'
    docker build -f "${dockerfile}" -t "${imageName}" .

    mkdir -p "${reportDir}"
    docker run --rm \
      -e PYTEST_WORKERS="${workers}" \
      -v "\$PWD/${reportDir}:/workspace/${reportDir}" \
      "${imageName}"
  """

  junit testResults: "${reportDir}/junit.xml", allowEmptyResults: true
  archiveArtifacts artifacts: "${reportDir}/*", allowEmptyArchive: true
}
