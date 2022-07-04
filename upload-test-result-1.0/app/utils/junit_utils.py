import glob
import xml.etree.ElementTree as ET

template_junit_msg = '{ \
  "blocks": [ \
    { \
      "type": "section", \
      "text": { \
        "type": "mrkdwn", \
        "text": "*TEMPLATE_TITLE*" \
      } \
    }, \
    { \
      "type": "section", \
      "text": { \
        "type": "mrkdwn", \
        "text": "*JUnit Result*" \
      } \
    } \
  ], \
  "attachments": [ \
    { \
      "color": "TEMPLATE_COLOR", \
      "blocks": [ \
        { \
            "type": "section", \
            "fields": [ \
                { \
                  "type": "mrkdwn", \
                  "text": "*Successfully Tested*\nTEMPLATE_TESTED" \
                }, \
                { \
                  "type": "mrkdwn", \
                  "text": "*Failed Tests*\nTEMPLATE_FAILED" \
                } \
            ] \
        }, \
        { \
            "type": "section", \
            "fields": [ \
                { \
                  "type": "mrkdwn", \
                  "text": "*Skipped Tested*\nTAMPLATE_SKIPPED" \
                }, \
                { \
                  "type": "mrkdwn", \
                  "text": "*Total Tests*\nTEMPLATE_TOTAL" \
                } \
            ] \
        }, \
        { \
            "type": "section", \
            "fields": [ \
                { \
                  "type": "mrkdwn", \
                  "text": "*Result*\nTEMPLATE_RESULT" \
                }, \
                { \
                  "type": "mrkdwn", \
                  "text": "*Time*\nTEMPLATE_TIME" \
                } \
            ] \
        } \
      ] \
    } \
  ] \
}'


def merge_junit_results(xml_dirs, merged_file):
    failures = 0
    tests = 0
    errors = 0
    skipped = 0
    time = 0.0
    cases = []

    for file_name in glob.glob(xml_dirs + '/*.xml'):
        tree = ET.parse(file_name)
        test_suite = tree.getroot()
        failures += int(test_suite.attrib['failures'])
        tests += int(test_suite.attrib['tests'])
        errors += int(test_suite.attrib['errors'])
        skipped += int(test_suite.attrib['skipped'])
        time += float(test_suite.attrib['time'])
        for child in test_suite.iter():
            cases.append(child)

    new_root = ET.Element('testsuite')
    new_root.attrib['failures'] = '%s' % failures
    new_root.attrib['tests'] = '%s' % tests
    new_root.attrib['errors'] = '%s' % errors
    new_root.attrib['skipped'] = '%s' % skipped
    new_root.attrib['time'] = '%s' % round(time, 2)
    for case in cases:
        new_root.extend(case)
    new_tree = ET.ElementTree(new_root)
    new_tree.write(merged_file)

    return new_root.attrib


def get_junit_result(xml_file):
    tree = ET.parse(xml_file)

    return tree


def get_slack_junit_message(title, branch, reports):
    template_rule = dict()
    template_rule['failures'] = 'TEMPLATE_FAILED'
    template_rule['tests'] = 'TEMPLATE_TESTED'
    template_rule['skipped'] = 'TAMPLATE_SKIPPED'
    template_rule['time'] = 'TEMPLATE_TIME'

    merge_title = title
    if len(branch) > 0:
        merge_title = "{} - ({})".format(title, branch)
    slack_message = template_junit_msg
    slack_message = slack_message.replace('TEMPLATE_TITLE', merge_title)
    if reports['failures'] != '0':
        slack_message = slack_message.replace('TEMPLATE_RESULT', 'Fail')
        slack_message = slack_message.replace('TEMPLATE_COLOR', '#DC143C')
    else:
        slack_message = slack_message.replace('TEMPLATE_RESULT', 'Success')
        slack_message = slack_message.replace('TEMPLATE_COLOR', '#3CB371')
    total_tested = int(reports['failures']) + int(reports['tests']) + int(reports['skipped'])
    slack_message = slack_message.replace('TEMPLATE_TOTAL', str(total_tested))

    for factor in template_rule:
        if factor in reports:
            slack_message = slack_message.replace(template_rule[factor], reports[factor])

    return slack_message
