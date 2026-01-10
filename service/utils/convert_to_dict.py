from zeep.helpers import serialize_object

from service.utils.logger import logger


def convert_zeep_object_to_dict(afip_response: object) -> dict:

    """
    Zeep usually returns an object of type '<class 'zeep.objects.[service response]'>'.
    To work with the returned data, this object needs to be converted into a dictionary.
    This function performs that conversion and saves the data as a JSON file.
    """

    # Convert to dict/OrderedDict
    serialized_xml = serialize_object(afip_response)
    logger.debug("Zeep object converted to dict.")

    return serialized_xml