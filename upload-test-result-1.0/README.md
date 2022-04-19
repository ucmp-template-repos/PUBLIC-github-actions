# JUNIT Slack Reporter with coverage
Github Action to send JUnit results to Slack.

## What it does!
This action will:
  * Merge JUnit test results of individual xml
  * Parse Coverage report
  * Send JUnit test result to slack
  * (Optional) Send Coverage report to slack

## What you need!
  * Slack Incomming URL

## Setting up the action
| Environment Variable  | Example                                        | Description                                                   | 	Required? |
| ------------- |------------------------------------------------|---------------------------------------------------------------|------------|
| JUNIT_TEST_RESULTS  | build/test-results/test                        | Path (relative to workspce directory) to JUnit report         | Y |
| JACOCO_REPORTS  | build/reports/jacoco/test/jacocoTestReport.xml | File Path (relative to workspce directory) to Coverage report | Y*         |
| SLACK_URL  | https://hooks.slack.com/services/XXXXXXXXXXXXX | Slack Incomming Webhook URL                                   | Y          |

## Sample Workflow section
```
    - name: notify-tests
      uses: protodevteam/upload-test-result@release
      env:
        JUNIT_TEST_RESULTS: build/test-results/test
        JACOCO_REPORTS: build/reports/jacoco/test/jacocoTestReport.xml
        SLACK_URL: ${{ secrets.SLACK_URL }}
```

# Slack message example
<img width="551" alt="image" src="https://user-images.githubusercontent.com/83627893/163830042-d1434a9e-7324-468f-97a5-0c4adc953059.png">


