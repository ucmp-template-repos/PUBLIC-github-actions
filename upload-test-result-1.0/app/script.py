from settings import *
from utils.junit_utils import *
from utils.jacoco_utils import *
from utils.slack_utils import *


def main():
    # JUnit result
    junit_report = merge_junit_results(JUNIT_TEST_RESULTS, JUNIT_MERGE_FILES)
    for key in junit_report.keys():
        print('%s %s' % (key, junit_report[key]))

    # Coverage result
    jacoco_report = get_jacoco_result(JACOCO_REPORTS)
    for key in jacoco_report.keys():
        print('%s %s' % (key, jacoco_report[key]))

    # Notify to Slack
    if len(junit_report.keys()) > 0:
        junit_msg = get_slack_junit_message(REPORT_TITLE, SOURCE_BRANCH, junit_report)
        send_message(SLACK_URL, junit_msg)

    if len(jacoco_report.keys()) > 0:
        junit_msg = get_slack_jacoco_message(jacoco_report)
        send_message(SLACK_URL, junit_msg)


if __name__ == "__main__":
    main()
