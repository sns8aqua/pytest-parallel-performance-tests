# Jenkins Shared Library Setup (Hands-On)

## What is a Shared Library?

A Jenkins Shared Library is a reusable Groovy codebase for pipelines.
It lets you move common CI/CD logic out of individual Jenkinsfiles and version it like normal code.

Typical production use cases:
- Standardized build/test/deploy stages across many repos
- Central security gates and quality checks
- Common notification logic (Slack, Teams, email)
- Shared Docker build and publishing workflows

## Library Scaffolding Added in This Repo

- `ci/shared-library/vars/runPytestPerfInDocker.groovy`
- `Jenkinsfile` (single pipeline entrypoint)

## Production Pattern (Recommended)

Use a separate Git repository for the shared library with this root layout:

- `vars/`
- `src/`
- `resources/`

For your first lab, you can start by moving the `ci/shared-library` content into a dedicated repo.

## Step-by-Step in Jenkins UI

1. Open **Manage Jenkins > System**.
2. Go to **Global Trusted Pipeline Libraries**.
3. Add a library:
   - Name: `pytest-shared-lib`
   - Default version: `main`
   - Load implicitly: unchecked (recommended for explicit usage)
   - Retrieval method: **Modern SCM**
   - Source Code Management: **Git**
   - Project Repository: your shared library Git URL
   - Credentials: set if private repo
4. Save.

## Use It in Pipeline

Use the root `Jenkinsfile` in this repo as the only pipeline file.
Add the shared library import at the top and call the shared step in stages.

Example:

```groovy
@Library('pytest-shared-lib@main') _

pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Test') {
      steps {
        runPytestPerfInDocker(workers: '4')
      }
    }
  }
}
```

Keep only one pipeline entrypoint in Jenkins job configuration:
- **Definition**: Pipeline script from SCM
- **Script Path**: `Jenkinsfile`

## Senior-Level Practices

- Version shared library with tags (`v1`, `v2`) and pin jobs to versions.
- Treat library as a product: tests, changelog, semantic versioning.
- Use `@Library('name@version')` for deterministic builds.
- Keep unsafe operations in trusted libraries only.
- Add unit tests for library functions using Jenkins Pipeline Unit.
- Add governance checks (SAST, license checks, artifact signing) in one place.

## Suggested Training Roadmap

1. Start with one function (`runPytestPerfInDocker`) and consume it from one pipeline.
2. Move Slack notification and log summarization into the library.
3. Add release tags in the library and pin pipelines to tags.
4. Add Jenkins Configuration as Code (JCasC) for full reproducibility.
