from __future__ import print_function
from pprint import pprint
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException

API_KEY = '8cf3c963-07a7-4cba-a639-622ac1a5c89a'

configuration = cloudmersive_barcode_api_client.Configuration()
configuration.api_key['Apikey'] = API_KEY

# file | Image file to perform the operation on.  Common file formats such as PNG, JPEG are supported.
test_path = 'static/test.jpg'
# str | QR code text to convert into the QR code barcode
test_value = 'QRcode'


def process(path: str):
    # create an instance of the API class
    api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(
        cloudmersive_barcode_api_client.ApiClient(configuration))
    try:
        # Scan and recognize an image of a barcode
        api_response = api_instance.barcode_scan_image(path)
        pprint(api_response)
        return api_response
    except ApiException as e:
        print("Exception when calling BarcodeScanApi->barcode_scan_image: %s\n" % e)


# process(test_path)


def generate_qr(text):
    # create an instance of the API class
    api_instance = \
        cloudmersive_barcode_api_client.GenerateBarcodeApi(cloudmersive_barcode_api_client.ApiClient(configuration))
    try:
        # Generate a QR code barcode as PNG file
        api_response = api_instance.generate_barcode_qr_code(text)
        # convert string to bytes array, .encode() doesn't work here
        result = eval(api_response)
        return result
    except ApiException as e:
        print("Exception when calling GenerateBarcodeApi->generate_barcode_qr_code: %s\n" % e)


# with open('static/generated_qr.png', 'wb') as gen_qr:
#     gen_qr.write(generate_qr(test_value))
