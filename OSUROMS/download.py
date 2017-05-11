import os
from urlparse import urljoin
import urllib
from dateutil import parser
from datetime import datetime, timedelta
from defusedxml import ElementTree
import urllib2


CATALOG_XML_NAME = "catalog.xml"
URL = "http://ingria.coas.oregonstate.edu/opendap/ORWA/"
XML_NAMESPACE = "{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}"

def get_ingria_xml_tree():
    # todo: need to handle if the xml file isn't available
    xml_url = urljoin(URL, CATALOG_XML_NAME)
    catalog_xml = urllib2.urlopen(xml_url)
    tree = ElementTree.parse(catalog_xml)
    return tree

def extract_modified_datetime_from_xml(elem):
    modified_datetime_string = elem.find(XML_NAMESPACE + 'date').text
    naive_datetime = parser.parse(modified_datetime_string)  # the date in the xml file follows iso standards, so we're gold.
    #modified_datetime = timezone.make_aware(naive_datetime, timezone.utc)
    return naive_datetime

def download():
    days_to_retrieve = [datetime.now().date()]

    '''
    days_to_retrieve = [now().date(),
                        timezone.now().date() + timedelta(days=1),
                        timezone.now().date() + timedelta(days=2),
                        timezone.now().date() + timedelta(days=3)]
    '''
    files_to_retrieve = []
    tree = get_ingria_xml_tree()  # yes, we just did this to see if there's a new file. refactor later.
    tags = tree.iter(XML_NAMESPACE + 'dataset')

    for elem in tags:
        server_filename = elem.get('name')
        if not server_filename.startswith('ocean_his'):
            continue
        date_string_from_filename = server_filename.split('_')[-1]
        model_date = datetime.strptime(date_string_from_filename, "%d-%b-%Y.nc").date()   # this could fail, need error handling badly
        modified_datetime = extract_modified_datetime_from_xml(elem)

        # TODO: REVIEW: Do what now??

        for day_to_retrieve in days_to_retrieve:
            if model_date - day_to_retrieve == timedelta(days=0):
                files_to_retrieve.append((server_filename, model_date, modified_datetime))

    new_file_ids = []

    for server_filename, model_date, modified_datetime in files_to_retrieve:
        url = urljoin(URL, server_filename)
        local_filename = "{0}_{1}.nc".format("ROMS", model_date)
        print "Retrieving: " + str(local_filename)
        urllib.urlretrieve(url=url, filename=os.path.join("/home/data/files/", local_filename)) # this also needs a try/catch


    return #Filename

if __name__ == "__main__":
    print download()
