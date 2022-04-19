import xml.etree.ElementTree as ET
from os.path import exists

template_coverage_msg = '{ \
  "blocks": [ \
    { \
      "type": "section", \
      "text": { \
        "type": "mrkdwn", \
        "text": "*Coverage Result*" \
      } \
    } \
  ], \
  "attachments": [ \
    { \
      "color": "#3CB371", \
      "blocks": [ \
        { \
            "type": "section", \
            "fields": [ \
                { \
                  "type": "mrkdwn", \
                  "text": "*Class*\nTEMPLATE_CLASS" \
                }, \
                { \
                  "type": "mrkdwn", \
                  "text": "*Method*\nTEMPLATE_METHOD" \
                } \
            ] \
        }, \
   { \
            "type": "section", \
            "fields": [ \
                { \
                  "type": "mrkdwn", \
                  "text": "*Instruciton*\nTEMPLATE_INSTRUCTION" \
                }, \
                { \
                  "type": "mrkdwn", \
                  "text": "*Branch*\nTEMPLATE_BRANCH" \
                } \
            ] \
        }, \
        { \
            "type": "section", \
            "fields": [ \
                { \
                  "type": "mrkdwn", \
                  "text": "*Line*\nTEMPLATE_LINE" \
                } \
            ] \
        } \
      ] \
    } \
  ] \
}'


def get_jacoco_result(xml_file):
    coverage = dict()
    if not exists(xml_file):
        return coverage

    tree = ET.parse(xml_file)
    for child in tree.getroot():
        if child.tag == 'counter':
            coverage[child.attrib['type']] = (child.attrib['missed'], child.attrib['covered'])

    return coverage


def get_percentage_coverage(stat):
    missed, covered = stat
    ratio = round(int(covered) / (int(covered) + int(missed)) * 100, 2)

    return str(ratio) + '%'


def get_slack_jacoco_message(reports):
    template_rule = dict()
    template_rule['INSTRUCTION'] = 'TEMPLATE_INSTRUCTION'
    template_rule['BRANCH'] = 'TEMPLATE_BRANCH'
    template_rule['CLASS'] = 'TEMPLATE_CLASS'
    template_rule['METHOD'] = 'TEMPLATE_METHOD'
    template_rule['LINE'] = 'TEMPLATE_LINE'

    slack_message = template_coverage_msg
    for factor in template_rule:
        if factor in reports:
            ratio = get_percentage_coverage(reports[factor])
            slack_message = slack_message.replace(template_rule[factor], ratio)

    return slack_message
