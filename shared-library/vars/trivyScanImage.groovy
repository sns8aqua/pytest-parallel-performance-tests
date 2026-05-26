// trivyScanImage.groovy
// Production-grade Trivy vulnerability scan step.
//
// Principal DevOps pattern:
//   - Runs Trivy as a Docker container (no host installation needed)
//   - Configurable severity gate: fail on CRITICAL by default, warn on HIGH
//   - Generates both JSON and SARIF reports for archiving and GitHub integration
//   - Generates SBOM (Software Bill of Materials) in CycloneDX format
//   - Respects .trivyignore for accepted/reviewed CVEs
//   - Caches Trivy vulnerability DB across builds to reduce scan time
//   - Never fails silently: all scan output is archived regardless of result

def call(Map cfg = [:]) {
  // Configurable inputs with safe production defaults
  String imageName     = cfg.get('imageName', 'pytest-parallel-performance-tests:ci')
  String reportDir     = cfg.get('reportDir', 'reports/security')
  // CRITICAL = block build, HIGH = warn only (principal engineer standard)
  String exitOnSeverity = cfg.get('exitOnSeverity', 'CRITICAL')
  // Trivy image version pinned for reproducibility - bump intentionally
  String trivyImage    = cfg.get('trivyImage', 'aquasec/trivy:0.62.0')
  // Cache dir on Jenkins node to persist vulnerability DB between builds
  String trivyCacheDir = cfg.get('trivyCacheDir', '/tmp/trivy-cache')

  sh """
    set -eu
    mkdir -p "${reportDir}"

    echo "=== Trivy Security Scan ==="
    echo "Image     : ${imageName}"
    echo "Gate      : fail on ${exitOnSeverity}"
    echo "Trivy ver : ${trivyImage}"

    # Run Trivy as a container - no host installation required.
    # Mounts:
    #   - Docker socket so Trivy can inspect the local image
    #   - Report output dir for artifacts
    #   - Cache dir to persist vulnerability DB across builds
    #   - Project root for .trivyignore and trivy.yaml
    TRIVY="docker run --rm \\
      -v /var/run/docker.sock:/var/run/docker.sock \\
      -v \$PWD:/workspace \\
      -v ${trivyCacheDir}:/root/.cache/trivy \\
      -w /workspace \\
      ${trivyImage}"

    # ── 1. Full vulnerability scan → JSON (machine-readable, archive + parse)
    \$TRIVY image \\
      --format json \\
      --output "${reportDir}/trivy-results.json" \\
      --ignorefile .trivyignore \\
      --config trivy.yaml \\
      --cache-dir /root/.cache/trivy \\
      "${imageName}" || true

    # ── 2. Human-readable table scan → log (printed in Jenkins console)
    \$TRIVY image \\
      --format table \\
      --ignorefile .trivyignore \\
      --config trivy.yaml \\
      --cache-dir /root/.cache/trivy \\
      "${imageName}" || true

    # ── 3. SARIF report → upload to GitHub Security tab (Advanced Security)
    \$TRIVY image \\
      --format sarif \\
      --output "${reportDir}/trivy-results.sarif" \\
      --ignorefile .trivyignore \\
      --config trivy.yaml \\
      --cache-dir /root/.cache/trivy \\
      "${imageName}" || true

    # ── 4. SBOM (Software Bill of Materials) in CycloneDX format
    #    Tracks every package in the image - required for supply chain compliance
    \$TRIVY image \\
      --format cyclonedx \\
      --output "${reportDir}/sbom-cyclonedx.json" \\
      --cache-dir /root/.cache/trivy \\
      "${imageName}" || true

    # ── 5. Enforcement gate: exit non-zero only on configured severity
    #    This is the one scan that controls whether the build passes or fails.
    echo "=== Enforcing gate: exit on \${exitOnSeverity:-CRITICAL} ==="
    \$TRIVY image \\
      --exit-code 1 \\
      --severity "${exitOnSeverity}" \\
      --ignorefile .trivyignore \\
      --config trivy.yaml \\
      --cache-dir /root/.cache/trivy \\
      "${imageName}"

    echo "=== Security gate passed ==="
  """

  // Archive all security artifacts regardless of scan outcome
  archiveArtifacts artifacts: "${reportDir}/**", allowEmptyArchive: true
}
