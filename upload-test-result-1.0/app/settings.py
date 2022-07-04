import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '.'))
sys.path.append(PROJECT_DIR)

APP_VERSION = '1.0.0'

# Test results
JUNIT_MERGE_FILES = 'junit_merge.xml'
JUNIT_TEST_RESULTS = os.getenv('JUNIT_TEST_RESULTS', "build/test-results/test")
JACOCO_REPORTS = os.getenv("JACOCO_REPORTS", "build/reports/jacoco/test/jacocoTestReport.xml")
SOURCE_BRANCH = os.getenv("SOURCE_BRANCH", "")
SLACK_URL = os.getenv("SLACK_URL", "")
REPORT_TITLE = os.getenv('REPORT_TITLE', "자동화테스트 결과 알림")

