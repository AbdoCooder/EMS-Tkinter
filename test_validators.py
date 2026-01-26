"""
Unit tests for the validators module.
"""

import unittest
from validators import (
    validate_date,
    validate_email,
    validate_full_name,
    validate_department,
    validate_address,
    validate_job_title,
    validate_job_description,
    validate_employee_data,
    VALID_DEPARTMENTS
)


class TestDateValidation(unittest.TestCase):
    """Test cases for date validation."""
    
    def test_valid_date(self):
        """Test valid date formats."""
        valid, msg = validate_date("01/01/2000")
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_valid_date_with_single_digits(self):
        """Test valid date with single digit day/month."""
        valid, msg = validate_date("1/1/2000")
        self.assertTrue(valid)
    
    def test_valid_leap_year_date(self):
        """Test valid leap year date."""
        valid, msg = validate_date("29/02/2020")  # 2020 is a leap year
        self.assertTrue(valid)
    
    def test_invalid_leap_year_date(self):
        """Test invalid leap year date."""
        valid, msg = validate_date("29/02/2021")  # 2021 is not a leap year
        self.assertFalse(valid)
        self.assertIn("not a valid date", msg)
    
    def test_invalid_date_format(self):
        """Test invalid date format."""
        valid, msg = validate_date("2000-01-01")
        self.assertFalse(valid)
        self.assertIn("DD/MM/YYYY", msg)
    
    def test_invalid_day_value(self):
        """Test invalid day value."""
        valid, msg = validate_date("32/01/2000")
        self.assertFalse(valid)
    
    def test_invalid_month_value(self):
        """Test invalid month value."""
        valid, msg = validate_date("01/13/2000")
        self.assertFalse(valid)
    
    def test_invalid_year_value(self):
        """Test invalid year value (out of range)."""
        valid, msg = validate_date("01/01/1800")
        self.assertFalse(valid)
    
    def test_empty_date_not_required(self):
        """Test empty date when not required."""
        valid, msg = validate_date("", required=False)
        self.assertTrue(valid)
    
    def test_empty_date_required(self):
        """Test empty date when required."""
        valid, msg = validate_date("", required=True)
        self.assertFalse(valid)
    
    def test_none_date_not_required(self):
        """Test None date when not required."""
        valid, msg = validate_date(None, required=False)
        self.assertTrue(valid)
    
    def test_gibberish_date(self):
        """Test completely invalid date string."""
        valid, msg = validate_date("not-a-date")
        self.assertFalse(valid)


class TestEmailValidation(unittest.TestCase):
    """Test cases for email validation."""
    
    def test_valid_email(self):
        """Test valid email format."""
        valid, msg = validate_email("test@example.com")
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        valid, msg = validate_email("user@sub.domain.com")
        self.assertTrue(valid)
    
    def test_valid_email_with_plus(self):
        """Test valid email with plus sign."""
        valid, msg = validate_email("user+tag@example.com")
        self.assertTrue(valid)
    
    def test_invalid_email_no_at(self):
        """Test invalid email without @."""
        valid, msg = validate_email("testexample.com")
        self.assertFalse(valid)
    
    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        valid, msg = validate_email("test@")
        self.assertFalse(valid)
    
    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        valid, msg = validate_email("test@example")
        self.assertFalse(valid)
    
    def test_empty_email_not_required(self):
        """Test empty email when not required."""
        valid, msg = validate_email("", required=False)
        self.assertTrue(valid)
    
    def test_empty_email_required(self):
        """Test empty email when required."""
        valid, msg = validate_email("", required=True)
        self.assertFalse(valid)


class TestFullNameValidation(unittest.TestCase):
    """Test cases for full name validation."""
    
    def test_valid_name(self):
        """Test valid name."""
        valid, msg = validate_full_name("John Doe")
        self.assertTrue(valid)
    
    def test_valid_name_with_hyphen(self):
        """Test valid name with hyphen."""
        valid, msg = validate_full_name("Mary-Jane Watson")
        self.assertTrue(valid)
    
    def test_valid_name_with_apostrophe(self):
        """Test valid name with apostrophe."""
        valid, msg = validate_full_name("O'Connor")
        self.assertTrue(valid)
    
    def test_name_too_short(self):
        """Test name that is too short."""
        valid, msg = validate_full_name("A")
        self.assertFalse(valid)
        self.assertIn("at least 2 characters", msg)
    
    def test_name_with_numbers(self):
        """Test name with numbers (invalid)."""
        valid, msg = validate_full_name("John123")
        self.assertFalse(valid)
    
    def test_empty_name_required(self):
        """Test empty name when required."""
        valid, msg = validate_full_name("", required=True)
        self.assertFalse(valid)
    
    def test_empty_name_not_required(self):
        """Test empty name when not required."""
        valid, msg = validate_full_name("", required=False)
        self.assertTrue(valid)


class TestDepartmentValidation(unittest.TestCase):
    """Test cases for department validation."""
    
    def test_valid_departments(self):
        """Test all valid department values."""
        for dept in VALID_DEPARTMENTS:
            valid, msg = validate_department(dept)
            self.assertTrue(valid, f"Department '{dept}' should be valid")
    
    def test_invalid_department(self):
        """Test invalid department."""
        valid, msg = validate_department("Unknown")
        self.assertFalse(valid)
        self.assertIn("must be one of", msg)
    
    def test_empty_department_required(self):
        """Test empty department when required."""
        valid, msg = validate_department("", required=True)
        self.assertFalse(valid)
    
    def test_empty_department_not_required(self):
        """Test empty department when not required."""
        valid, msg = validate_department("", required=False)
        self.assertTrue(valid)


class TestAddressValidation(unittest.TestCase):
    """Test cases for address validation."""
    
    def test_valid_address(self):
        """Test valid address."""
        valid, msg = validate_address("123 Main Street, City")
        self.assertTrue(valid)
    
    def test_empty_address_not_required(self):
        """Test empty address when not required."""
        valid, msg = validate_address("", required=False)
        self.assertTrue(valid)
    
    def test_empty_address_required(self):
        """Test empty address when required."""
        valid, msg = validate_address("", required=True)
        self.assertFalse(valid)
    
    def test_address_too_long(self):
        """Test address that exceeds maximum length."""
        long_address = "A" * 501
        valid, msg = validate_address(long_address)
        self.assertFalse(valid)


class TestJobTitleValidation(unittest.TestCase):
    """Test cases for job title validation."""
    
    def test_valid_job_title(self):
        """Test valid job title."""
        valid, msg = validate_job_title("Software Engineer")
        self.assertTrue(valid)
    
    def test_empty_job_title_not_required(self):
        """Test empty job title when not required."""
        valid, msg = validate_job_title("", required=False)
        self.assertTrue(valid)
    
    def test_job_title_too_long(self):
        """Test job title that exceeds maximum length."""
        long_title = "A" * 101
        valid, msg = validate_job_title(long_title)
        self.assertFalse(valid)


class TestJobDescriptionValidation(unittest.TestCase):
    """Test cases for job description validation."""
    
    def test_valid_job_description(self):
        """Test valid job description."""
        valid, msg = validate_job_description("Responsible for developing software solutions.")
        self.assertTrue(valid)
    
    def test_empty_job_description_not_required(self):
        """Test empty job description when not required."""
        valid, msg = validate_job_description("", required=False)
        self.assertTrue(valid)
    
    def test_job_description_too_long(self):
        """Test job description that exceeds maximum length."""
        long_desc = "A" * 2001
        valid, msg = validate_job_description(long_desc)
        self.assertFalse(valid)


class TestEmployeeDataValidation(unittest.TestCase):
    """Test cases for complete employee data validation."""
    
    def test_valid_employee_data(self):
        """Test valid complete employee data."""
        data = {
            "full_name": "John Doe",
            "birth_date": "15/03/1990",
            "hiring_date": "01/06/2020",
            "dept_name": "IT",
            "email": "john.doe@example.com",
            "address": "123 Main Street",
            "job_title": "Software Engineer",
            "job_description": "Develops software"
        }
        valid, errors = validate_employee_data(data)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_minimal_valid_data(self):
        """Test minimal required employee data."""
        data = {
            "full_name": "John Doe",
            "birth_date": "",
            "hiring_date": "",
            "dept_name": "IT",
            "email": "",
            "address": "",
            "job_title": "",
            "job_description": ""
        }
        valid, errors = validate_employee_data(data)
        self.assertTrue(valid)
    
    def test_missing_required_fields(self):
        """Test missing required fields."""
        data = {
            "full_name": "",
            "birth_date": "",
            "hiring_date": "",
            "dept_name": "",
            "email": "",
            "address": "",
            "job_title": "",
            "job_description": ""
        }
        valid, errors = validate_employee_data(data)
        self.assertFalse(valid)
        self.assertIn("Full name is required.", errors)
        self.assertIn("Department is required.", errors)
    
    def test_invalid_dates(self):
        """Test invalid date formats."""
        data = {
            "full_name": "John Doe",
            "birth_date": "invalid-date",
            "hiring_date": "2020-01-01",
            "dept_name": "IT",
            "email": "",
            "address": "",
            "job_title": "",
            "job_description": ""
        }
        valid, errors = validate_employee_data(data)
        self.assertFalse(valid)
        self.assertTrue(len(errors) >= 2)  # Both dates should fail
    
    def test_hiring_before_birth(self):
        """Test that hiring date must be after birth date."""
        data = {
            "full_name": "John Doe",
            "birth_date": "01/01/2000",
            "hiring_date": "01/01/1990",
            "dept_name": "IT",
            "email": "",
            "address": "",
            "job_title": "",
            "job_description": ""
        }
        valid, errors = validate_employee_data(data)
        self.assertFalse(valid)
        self.assertIn("Hiring date must be after birth date.", errors)
    
    def test_employee_too_young(self):
        """Test that employee must be at least 16 at hiring."""
        data = {
            "full_name": "John Doe",
            "birth_date": "01/01/2010",
            "hiring_date": "01/01/2020",  # Would be 10 years old
            "dept_name": "IT",
            "email": "",
            "address": "",
            "job_title": "",
            "job_description": ""
        }
        valid, errors = validate_employee_data(data)
        self.assertFalse(valid)
        self.assertIn("Employee must be at least 16 years old at the time of hiring.", errors)
    
    def test_invalid_email_format(self):
        """Test invalid email format."""
        data = {
            "full_name": "John Doe",
            "birth_date": "",
            "hiring_date": "",
            "dept_name": "IT",
            "email": "invalid-email",
            "address": "",
            "job_title": "",
            "job_description": ""
        }
        valid, errors = validate_employee_data(data)
        self.assertFalse(valid)
        self.assertTrue(any("Email" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
