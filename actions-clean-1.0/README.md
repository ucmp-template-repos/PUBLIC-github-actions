# Clean

A Github Action to clean the runner workspace

If you are using a self-hosted runner, 
it is **highly** recommended that you set this action to run unconditionally as your last step. 
This is crucial for cleaning up the runner workspace.

## Usage

```yaml
jobs:
  unit:
    runs-on: review-runner
# ...
    steps:
      - name: checkout src
        uses: actions/checkout@v3
# - step 2
# - step 3
# - ...
      - name: cleanup src
        if: ${{ always() }}
        uses: ucmp-template-repos/PUBLIC-github-actions/actions-clean-1.0@main
```
