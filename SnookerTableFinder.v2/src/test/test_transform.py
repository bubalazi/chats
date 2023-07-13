import unittest
import os

from ..transform import transform_image

class TestTransform(unittest.TestCase):
    def test_transform_image(self):
        input_path = 'src/test/data/4.png'
        output_dir = 'src/test/output'

        transform_image(input_path, output_dir)

        output_path = os.path.join(output_dir, 'transformed_image.jpg')
        self.assertTrue(os.path.exists(output_path))

if __name__ == '__main__':
    unittest.main()
