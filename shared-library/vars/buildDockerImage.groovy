// buildDockerImage.groovy
// Builds and optionally tags a Docker image from a given Dockerfile.
// Kept separate from test/scan steps so each stage has one responsibility.

def call(Map cfg = [:]) {
  String imageName  = cfg.get('imageName', 'pytest-parallel-performance-tests:ci')
  String dockerfile = cfg.get('dockerfile', 'Dockerfile')
  String context    = cfg.get('context', '.')

  sh """
    set -eu
    echo "=== Building Docker image: ${imageName} ==="
    docker build \\
      -f "${dockerfile}" \\
      -t "${imageName}" \\
      "${context}"
    echo "=== Build complete ==="
  """
}
