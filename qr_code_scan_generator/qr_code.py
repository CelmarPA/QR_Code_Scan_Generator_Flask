import ast
import base64
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
import cv2

# Configure API key authorization for the Cloudmersive Barcode API
configuration = cloudmersive_barcode_api_client.Configuration()
configuration.api_key["Apikey"] = "<YOUR API KEY FROM CLOUDMERSIVE>"  # Replace with your actual API key


class GenerateQRCode:
    """
    Class to generate and scan QR Codes using Cloudmersive Barcode API and OpenCV.

    Methods:
        - generate_qr_code(value): Generates a QR code image bytes from the input string.
        - get_base64_img(): Returns the generated QR code image as a base64-encoded data URI.
        - save_qr_code(filename): Saves the generated QR code image to a file.
        - scan_qr_code(image_path): Static method that scans a QR code from an image file and returns decoded data.
    """

    def __init__(self):
        # Initialize instance variables
        self.value = None  # The string value to encode into QR code
        self.data_str = None  # Raw response string from API (not used explicitly here)
        self.image_bytes = None  # Bytes of the generated QR code image
        # Initialize API client instance for barcode generation
        self.api_instance = cloudmersive_barcode_api_client.GenerateBarcodeApi(
            cloudmersive_barcode_api_client.ApiClient(configuration)
        )

    def generate_qr_code(self, value):
        """
        Generate a QR code image from a string value using Cloudmersive API.

        :param value: (str) The string content to encode in the QR code.

        Sets:
            self.image_bytes: (bytes): The raw image bytes of the generated QR code.

        :return: data-str if success, or None if exception occurs (also prints error).
        """

        self.value = value

        try:
            # Call the API to generate QR code image (returns a string representation of bytes)
            api_response = self.api_instance.generate_barcode_qr_code(value)

            data_str = api_response

            # Convert the string representation of bytes to actual bytes object
            self.image_bytes = ast.literal_eval(data_str)

            return data_str

        except ApiException as e:
            # Handle exceptions from the API call
            print(f"Error generating QR Code: {e}")

            return None

    def get_base64_img(self):
        """
        Convert the generated QR code image bytes to a base64-encoded string suitable for embedding in HTML.

        :return: Data URI string of the QR code image in PNG format.
        """

        # Encode the image bytes to base64 and decode to UTF-8 string
        img_base64 = base64.b64encode(self.image_bytes).decode("utf-8")

        # Return a full data URI for direct use in <img> tags or CSS
        return f"data:image/png;base64,{img_base64}"

    def save_qr_code(self, filename="my_qr_code.png"):
        """
        Save the generated QR code image bytes to a PNG file.

        :param filename: (str) File path to save the image (default: "my_qr_code.png").
        """

        if hasattr(self, 'image_bytes'):
            with open(filename, "wb") as f:
                f.write(self.image_bytes)
        else:
            print("⚠️ No image generated yet.")

    @staticmethod
    def scan_qr_code(image_path):
        """
         Scan and decode a QR code from an image file using OpenCV

        :param image_path: (str) Path to the image file to scan.

        :return: (str) The decoded data from the QR code if detected, otherwise None.
        """

        # Read the image from the specified path
        img = cv2.imread(image_path)

        if img is None:
            print(f"❌ Image not found or invalid: {image_path}")
            return None

        # Initialize OpenCV's QR code detector
        detector = cv2.QRCodeDetector()

        # Detect and decode QR code in the image
        data, vertices, _ = detector.detectAndDecode(img)

        if data:
            print(f"✅ QR Code detected: {data}")

        else:
            print("⚠️ No QR Code detected.")

        return data
