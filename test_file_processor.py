import unittest
from unittest.mock import patch, MagicMock
from file_processor import process_and_upload_file, get_file_category, is_file_type_valid

class TestFileProcessor(unittest.TestCase):

    # Test cases for get_file_category
    @patch('file_processor.openai.Completion.create')
    def test_get_file_category_specification(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].text = "Specification"
        mock_openai.return_value = mock_response
        self.assertEqual(get_file_category("spec.pdf"), "Specification")

    @patch('file_processor.openai.Completion.create')
    def test_get_file_category_plans(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].text = "Plans"
        mock_openai.return_value = mock_response
        self.assertEqual(get_file_category("plan.pdf"), "Plans")

    @patch('file_processor.openai.Completion.create')
    def test_get_file_category_others(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].text = "SomeOtherCategory"
        mock_openai.return_value = mock_response
        self.assertEqual(get_file_category("other.txt"), "Others")

    # Test cases for is_file_type_valid
    def test_is_file_type_valid(self):
        self.assertTrue(is_file_type_valid("spec.pdf", "Specification"))
        self.assertTrue(is_file_type_valid("spec.doc", "Specification"))
        self.assertTrue(is_file_type_valid("spec.docx", "Specification"))
        self.assertFalse(is_file_type_valid("spec.txt", "Specification"))
        self.assertTrue(is_file_type_valid("plan.pdf", "Plans"))
        self.assertFalse(is_file_type_valid("plan.doc", "Plans"))

    # Test cases for process_and_upload_file
    @patch('file_processor.get_blob_service_client')
    @patch('file_processor.get_file_category', return_value="Specification")
    @patch('file_processor.is_file_type_valid', return_value=True)
    @patch('file_processor.upload_file_to_blob', return_value=True)
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b"data")
    def test_process_and_upload_success(self, mock_get_blob_service_client, mock_get_category, mock_is_valid, mock_upload, mock_open):
        mock_get_blob_service_client.return_value = MagicMock()
        result = process_and_upload_file("dummy_path/spec.pdf", "conn_str", "container")
        self.assertIn("uploaded successfully", result)

    @patch('file_processor.get_file_category', return_value="Specification")
    @patch('file_processor.is_file_type_valid', return_value=False)
    def test_process_and_upload_invalid_type(self, mock_get_category, mock_is_valid):
        result = process_and_upload_file("dummy_path/spec.txt", "conn_str", "container")
        self.assertIn("is not accepted", result)

    @patch('file_processor.get_file_category', return_value="Others")
    def test_process_and_upload_other_category(self, mock_get_category):
        result = process_and_upload_file("dummy_path/other.txt", "conn_str", "container")
        self.assertIn("is not a specification or a plan", result)

if __name__ == '__main__':
    unittest.main()