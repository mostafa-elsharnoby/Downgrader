import re

from lxml import etree
import sys

# target_versions can be 2308 or 2207.0
def downgrade_project(input_file, current_version, target_version):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(input_file, parser)
    root = tree.getroot()

    # current_version = re.search(r'//\s*Project\s*([\d.]+)', doctype_line).group(1)

    if current_version == "2408":
        downgrade_to_2308(root)
    if (current_version == "2408" or "2308") and (target_version == "2207.0" or "2021.1"):
        downgrade_to_2207(root)
    # if (current_version == "2408" or "2308" or "2207.0") and target_version == "2021.1":
    #     downgrade_to_2021(root)

    # Make sure we still use UTF-8 encoding and double quotations to match input XML
    xml_str = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    xml_str = xml_str.replace(b"'", b'"')

    doctype_line = get_doctype_line(input_file)
    xml_str = update_doctype_with_version(doctype_line, target_version, xml_str)

    output_file = 'modified_project.xml'
    with open(output_file, 'wb') as f:
        f.write(xml_str)


def update_doctype_with_version(doctype_line, version, xml_str):
    if doctype_line:
        new_doctype_line = re.sub(r'//\s*Project\s*[\d.]+', f'//Project {version}', doctype_line)

        xml_lines = xml_str.decode('utf-8').splitlines()
        for i, line in enumerate(xml_lines):
            if line.strip().startswith('<!DOCTYPE'):
                xml_lines[i] = new_doctype_line
                break

        xml_str = '\n'.join(xml_lines).encode('utf-8')

    return xml_str


def get_doctype_line(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    doctype_line = ""
    for line in lines:
        if line.strip().startswith('<!DOCTYPE'):
            doctype_line = line.strip()
            break
    return doctype_line


def downgrade_to_2308(root):
    # singlelineendtype entityyy should be renamed to highwayendtype/deleted
    remove_attribute(root, "releaselevel", "designpropertytagediting")

    remove_attribute(root, "attributetext", "isfixposition")
    remove_attribute(root, "xreftext", "isfixposition")
    remove_attribute(root, "proptext", "isfixposition")
    remove_attribute(root, "diagramtext", "isfixposition")
    remove_attribute(root, "compositetext", "isfixposition")
    remove_attribute(root, "variantdimensiontext", "isfixposition")
    remove_attribute(root, "propertiedtext", "isfixposition")

    remove_attribute(root, "functionaldesignref", "modificationtimestamp")
    remove_attribute(root, "sourcedesignref", "modificationtimestamp")
    remove_attribute(root, "functionallogicdesignref", "modificationtimestamp")

    remove_attribute(root, "deviceslotelement", "weight")#exists
    remove_attribute(root, "deviceslotelement", "analysablesymbolid")#exists
    remove_attribute(root, "deviceslotelement", "architecturalcost")#exists
    remove_attribute(root, "deviceslotelement", "incbom")#exists
    remove_attribute(root, "deviceslotelement", "mcadid")#exists
    remove_attribute(root, "deviceslotelement", "shortdescription")#exists
    remove_attribute(root, "deviceslotelement", "location")#exists
    remove_attribute(root, "deviceslotelement", "function")#exists
    remove_attribute(root, "deviceslotelement", "harness")#exists
    remove_attribute(root, "deviceslotelement", "designabstraction")#exists
    remove_attribute(root, "deviceslotelement", "overriddenname")#exists
    remove_attribute(root, "deviceslotelement", "generatedname")#exists
    remove_attribute(root, "deviceslotelement", "numconnectors")#exists
    remove_attribute(root, "deviceslotelement", "numdeviceconnectors")#exists

    remove_attribute_from_all_elements(root, "propertytag")
    remove_attribute_from_all_elements(root, "structuremodifiedtimestamp")

    # This is to remove constraints and constraint elements that are not present in older versions.
    remove_any_element_with_attribute_value(root, "UID1b94e9-18cf84b5dd4-4dddc0f8ea9c32abf59fa23df9f7d1e8")
    remove_any_element_with_attribute_value(root, "UID1b94e9-18cf84b5dd5-4dddc0f8ea9c32abf59fa23df9f7d1e8")
    remove_any_element_with_attribute_value(root, "UID36b079-18b6105aced-3b04b6d712b80ba0babe7752b7fcef21")
    remove_any_element_with_attribute_value(root, "UID46850a-18b8ff831b8-7476d7596cd16a69f56555b4971cc18e")
    remove_any_element_with_attribute_value(root, "UID63fbd3-18b151f3b59-951674017f9da9a9d7efd1144b4ea718")
    remove_any_element_with_attribute_value(root, "UID63fbd3-18b151f3b5b-951674017f9da9a9d7efd1144b4ea718")
    remove_any_element_with_attribute_value(root, "UID74c27e-18b150c3418-951674017f9da9a9d7efd1144b4ea718")
    remove_any_element_with_attribute_value(root, "UID8ca2e5-18b4c9aa45f-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa50-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa51-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa52-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa53-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa54-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa55-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa56-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDac51f6-18bea3afa57-2306dde2f14a43fb6bf916fa17bae1e3")
    remove_any_element_with_attribute_value(root, "UIDb8b17f-18aaf3ff677-0d80d61dae8194776b6f616f0e6aa853")
    remove_any_element_with_attribute_value(root, "UIDb8b17f-18aaf3ff678-0d80d61dae8194776b6f616f0e6aa853")
    remove_any_element_with_attribute_value(root, "UIDd389a5-18b902b12a2-7476d7596cd16a69f56555b4971cc18e")
    remove_any_element_with_attribute_value(root, "UIDd4b5f7-18b60ed807b-3b04b6d712b80ba0babe7752b7fcef21")


def downgrade_to_2207(root):
    remove_attribute_issue_release_level_category(root)
    remove_attribute(root, "schemindicator", "indicatortype")
    remove_attribute(root, "releaselevel", "unfreezesharedobjectsrequired")
    remove_attribute(root, "projectdesshdcondusageconn", "connectedpin")

    remove_attribute_from_all_elements(root, "partmodifiedtimestamp")
    remove_attribute_from_all_elements(root, "isnoninhousetwistednumosspec")
    remove_attribute_from_all_elements(root, "stringsubtype")
    remove_attribute_from_all_elements(root, "displayinqep")
    remove_attribute_from_all_elements(root, "skeletalstyleapplied")

    remove_element(root, "viewconfigmgr")

    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce103147-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce10314d-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce103183-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce103189-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce1031cd-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce1031d7-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0bb5c5-181ce103231-37d70397fac71e8111998cabdbb39ddc")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f0a-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f14-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f1a-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f6e-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f78-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f7e-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID0e0cbf-180c8b82f8e-ef5aab0be9e6800788642848ed4679b2")
    remove_any_element_with_attribute_value(root, "UID17dbbd-18331f32abd-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID17dbbd-18331f32abe-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID17dbbd-18331f32abf-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID17dbbd-18331f32ac0-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID17dbbd-18331f32ac1-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID17dbbd-18331f32ac2-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID30b7eb-184a3a2a1c6-9593c7df27ce73f069df6fffcba07735")
    remove_any_element_with_attribute_value(root, "UID30b7eb-184a3a2a1c7-9593c7df27ce73f069df6fffcba07735")
    remove_any_element_with_attribute_value(root, "UID4a2447-182166591f7-b2c64f906ab63000d402f36d87cfae96")
    remove_any_element_with_attribute_value(root, "UID4a2447-182166591f8-b2c64f906ab63000d402f36d87cfae96")
    remove_any_element_with_attribute_value(root, "UID4a2447-182166591f9-b2c64f906ab63000d402f36d87cfae96")
    remove_any_element_with_attribute_value(root, "UID4a2447-182166591fa-b2c64f906ab63000d402f36d87cfae96")
    remove_any_element_with_attribute_value(root, "UID4da10f-182b575720b-5f724c63c6eb4806bd6ffbca8915717b")
    remove_any_element_with_attribute_value(root, "UID4da10f-182b575720c-5f724c63c6eb4806bd6ffbca8915717b")
    remove_any_element_with_attribute_value(root, "UID4da10f-182b575720d-5f724c63c6eb4806bd6ffbca8915717b")
    remove_any_element_with_attribute_value(root, "UID4da10f-182b575720e-5f724c63c6eb4806bd6ffbca8915717b")
    remove_any_element_with_attribute_value(root, "UID4da10f-182b5757210-5f724c63c6eb4806bd6ffbca8915717b")
    remove_any_element_with_attribute_value(root, "UID6e78c9-18331f8fa38-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID6e78c9-18331f8fa39-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID6e78c9-18331f8fa3a-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID6e78c9-18331f8fa3b-ec81c5bbbe260969bebc161acf470d69")
    remove_any_element_with_attribute_value(root, "UID85489f-183e4436c9a-47424175957b2ba682244396c4f2e416")
    remove_any_element_with_attribute_value(root, "UID85489f-183e4436c9b-47424175957b2ba682244396c4f2e416")
    remove_any_element_with_attribute_value(root, "UID85489f-183e4436c9c-47424175957b2ba682244396c4f2e416")
    remove_any_element_with_attribute_value(root, "UID85489f-183e4436c9d-47424175957b2ba682244396c4f2e416")
    remove_any_element_with_attribute_value(root, "UID85489f-183e4436c9e-47424175957b2ba682244396c4f2e416")
    remove_any_element_with_attribute_value(root, "UIDcc1544-183d4b1ba2a-448282272531623edef5db955d752363")
    remove_any_element_with_attribute_value(root, "UIDcc1544-183d4b1ba2b-448282272531623edef5db955d752363")
    remove_any_element_with_attribute_value(root, "UIDcc1544-183d4b1ba2c-448282272531623edef5db955d752363")
    remove_any_element_with_attribute_value(root, "UIDcc1544-183d4b1ba2d-448282272531623edef5db955d752363")
    remove_any_element_with_attribute_value(root, "UIDcc1544-183d4b1ba2f-448282272531623edef5db955d752363")
    remove_any_element_with_attribute_value(root, "UIDea380c-18211d91153-b2c64f906ab63000d402f36d87cfae96")
    remove_any_element_with_attribute_value(root, "UIDea380c-18211d9123a-b2c64f906ab63000d402f36d87cfae96")


def downgrade_to_2021(root):
    remove_attribute(root, "multicore", "isnoninhousetwistednumosspec")
    remove_attribute(root, "wire", "isroutedbyconstraint")
    remove_attribute(root, "deviceslotelement", "partnumberinintegrator")
    remove_attribute(root, "schemindicator", "indicatortype")
    remove_attribute(root, "spliceslotelement", "signalref")


def remove_element(root, element_to_remove):
    etree.strip_elements(root, element_to_remove)


def remove_element_with_attribute_value(root, element_to_remove, attribute, value):
    for element in root.xpath(f"//{element_to_remove}[@{attribute}='{value}']"):
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)


def remove_any_element_with_attribute_value(root, value):
    for element in root.xpath(f"//*[@*='{value}']"):
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)


def remove_attribute(current_element, target_element, attribute_to_remove):
    if current_element.tag == target_element and attribute_to_remove in current_element.attrib:
        del current_element.attrib[attribute_to_remove]

    for child in current_element:
        remove_attribute(child, target_element, attribute_to_remove)


def remove_attribute_from_all_elements(current_element, attribute_to_remove):
    if attribute_to_remove in current_element.attrib:
        del current_element.attrib[attribute_to_remove]

    for child in current_element:
        remove_attribute_from_all_elements(child, attribute_to_remove)



def remove_attribute_issue_release_level_category(root):
    for element in root.iter("releaselevel"):
        if "releaselevelcategory" in element.attrib and element.attrib["releaselevelcategory"] == "issue":
            if "isissuedeletionstatus" in element.attrib:
                del element.attrib["isissuedeletionstatus"]


if __name__ == "__main__":
    input_file = sys.argv[1]
    current_version = sys.argv[2]
    target_version = sys.argv[3]
    downgrade_project(input_file, current_version, target_version)
