from PIL import Image

class ImageProcessor:
    """A utility class for processing uploaded images."""

    # Define a fixed size for all button images for a consistent look
    FIXED_SIZE = (100, 100)

    @staticmethod
    def process_and_save(image_stream, output_path):
        """
        Converts an image to PNG, resizes it, and saves it.

        Args:
            image_stream: The file-like object from the request (e.g., request.files['image_file']).
            output_path: The full path where the processed PNG image should be saved.
        """
        try:
            with Image.open(image_stream) as img:
                # Resize the image with a high-quality downsampling filter
                resized_img = img.resize(ImageProcessor.FIXED_SIZE, Image.Resampling.LANCZOS)
                # Save the image as a PNG, which handles transparency well.
                resized_img.save(output_path, 'PNG')
        except Exception as e:
            print(f"Error processing image: {e}")
            raise  # Re-raise the exception to be handled by the route