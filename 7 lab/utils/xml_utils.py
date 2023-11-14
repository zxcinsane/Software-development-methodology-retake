from typing import Dict
from lxml import etree


def dict_to_xml(tag: str, data: Dict[str, str]) -> str:
    elem = etree.Element(tag)
    for key, val in data.items():
        child = etree.Element(key)
        child.text = val
        elem.append(child)
    return etree.tostring(elem, pretty_print=True, encoding="UTF-8")


def xml_to_dict(xml: str) -> Dict[str, str]:
    root = etree.fromstring(xml)
    return dict((child.tag, child.text) for child in root.getchildren())
