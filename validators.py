"""
Data validation module for the Employee Management System.
Provides comprehensive validation for all data flowing to/from the SQLite database.
"""

import re
from datetime import datetime
from typing import Optional, Tuple

# Constants for validation
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 254
MAX_ADDRESS_LENGTH = 500
MAX_JOB_TITLE_LENGTH = 100
MAX_JOB_DESCRIPTION_LENGTH = 2000
VALID_DEPARTMENTS = ["IT", "HR", "Finance", "Marketing"]
DATE_FORMAT = "%d/%m/%Y"


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_date(date_str: Optional[str], field_name: str = "Date", required: bool = False) -> Tuple[bool, str]:
    """
    Validate date string in DD/MM/YYYY format.
    
    Args:
        date_str: The date string to validate
        field_name: Name of the field for error messages
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_str or date_str.strip() == "":
        if required:
            return False, f"{field_name} is required."
        return True, ""
    
    date_str = date_str.strip()
    
    # Check format using regex first
    date_pattern = r'^(\d{1,2})/(\d{1,2})/(\d{4})$'
    match = re.match(date_pattern, date_str)
    
    if not match:
        return False, f"{field_name} must be in DD/MM/YYYY format."
    
    day_str, month_str, year_str = match.groups()
    
    try:
        day = int(day_str)
        month = int(month_str)
        year = int(year_str)
        
        # Check basic ranges before parsing
        if not (1 <= day <= 31):
            return False, f"{field_name} has invalid day value (must be 1-31)."
        if not (1 <= month <= 12):
            return False, f"{field_name} has invalid month value (must be 1-12)."
        if not (1900 <= year <= 2100):
            return False, f"{field_name} has invalid year value (must be 1900-2100)."
        
        # Use datetime to validate the actual date (handles leap years, etc.)
        parsed_date = datetime.strptime(date_str, DATE_FORMAT)
        
        # Additional check: date should not be in the far future
        if parsed_date > datetime(2100, 12, 31):
            return False, f"{field_name} cannot be beyond year 2100."
            
    except ValueError:
        return False, f"{field_name} is not a valid date. Please check the day/month values."
    
    return True, ""


def validate_email(email: Optional[str], required: bool = False) -> Tuple[bool, str]:
    """
    Validate email address format.
    
    Args:
        email: The email address to validate
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or email.strip() == "":
        if required:
            return False, "Email is required."
        return True, ""
    
    email = email.strip()
    
    if len(email) > MAX_EMAIL_LENGTH:
        return False, f"Email must be less than {MAX_EMAIL_LENGTH} characters."
    
    # RFC 5322 compliant email regex (simplified version)
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Email format is invalid. Expected format: example@domain.com"
    
    return True, ""


def validate_full_name(name: Optional[str], required: bool = True) -> Tuple[bool, str]:
    """
    Validate full name.
    
    Args:
        name: The full name to validate
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or name.strip() == "":
        if required:
            return False, "Full name is required."
        return True, ""
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Full name must be at least 2 characters."
    
    if len(name) > MAX_NAME_LENGTH:
        return False, f"Full name must be less than {MAX_NAME_LENGTH} characters."
    
    # Name should contain only letters, spaces, hyphens, and apostrophes
    name_pattern = r"^[a-zA-Z\s\-'\.]+$"
    if not re.match(name_pattern, name):
        return False, "Full name can only contain letters, spaces, hyphens, and apostrophes."
    
    return True, ""


def validate_department(dept: Optional[str], required: bool = True) -> Tuple[bool, str]:
    """
    Validate department name.
    
    Args:
        dept: The department name to validate
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not dept or dept.strip() == "":
        if required:
            return False, "Department is required."
        return True, ""
    
    dept = dept.strip()
    
    if dept not in VALID_DEPARTMENTS:
        return False, f"Department must be one of: {', '.join(VALID_DEPARTMENTS)}."
    
    return True, ""


def validate_address(address: Optional[str], required: bool = False) -> Tuple[bool, str]:
    """
    Validate address.
    
    Args:
        address: The address to validate
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not address or address.strip() == "":
        if required:
            return False, "Address is required."
        return True, ""
    
    address = address.strip()
    
    if len(address) > MAX_ADDRESS_LENGTH:
        return False, f"Address must be less than {MAX_ADDRESS_LENGTH} characters."
    
    return True, ""


def validate_job_title(title: Optional[str], required: bool = False) -> Tuple[bool, str]:
    """
    Validate job title.
    
    Args:
        title: The job title to validate
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or title.strip() == "":
        if required:
            return False, "Job title is required."
        return True, ""
    
    title = title.strip()
    
    if len(title) > MAX_JOB_TITLE_LENGTH:
        return False, f"Job title must be less than {MAX_JOB_TITLE_LENGTH} characters."
    
    return True, ""


def validate_job_description(description: Optional[str], required: bool = False) -> Tuple[bool, str]:
    """
    Validate job description.
    
    Args:
        description: The job description to validate
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not description or description.strip() == "":
        if required:
            return False, "Job description is required."
        return True, ""
    
    description = description.strip()
    
    if len(description) > MAX_JOB_DESCRIPTION_LENGTH:
        return False, f"Job description must be less than {MAX_JOB_DESCRIPTION_LENGTH} characters."
    
    return True, ""


def validate_employee_data(data: dict) -> Tuple[bool, list]:
    """
    Validate all employee data fields.
    
    Args:
        data: Dictionary containing employee data with keys:
              full_name, birth_date, hiring_date, dept_name, email, 
              address, job_title, job_description
              
    Returns:
        Tuple of (is_valid, list_of_error_messages)
    """
    errors = []
    
    # Validate full name (required)
    valid, msg = validate_full_name(data.get("full_name"), required=True)
    if not valid:
        errors.append(msg)
    
    # Validate birth date (optional but must be valid if provided)
    valid, msg = validate_date(data.get("birth_date"), field_name="Birth date", required=False)
    if not valid:
        errors.append(msg)
    
    # Validate hiring date (optional but must be valid if provided)
    valid, msg = validate_date(data.get("hiring_date"), field_name="Hiring date", required=False)
    if not valid:
        errors.append(msg)
    
    # Validate department (required)
    valid, msg = validate_department(data.get("dept_name"), required=True)
    if not valid:
        errors.append(msg)
    
    # Validate email (optional but must be valid if provided)
    valid, msg = validate_email(data.get("email"), required=False)
    if not valid:
        errors.append(msg)
    
    # Validate address (optional)
    valid, msg = validate_address(data.get("address"), required=False)
    if not valid:
        errors.append(msg)
    
    # Validate job title (optional)
    valid, msg = validate_job_title(data.get("job_title"), required=False)
    if not valid:
        errors.append(msg)
    
    # Validate job description (optional)
    valid, msg = validate_job_description(data.get("job_description"), required=False)
    if not valid:
        errors.append(msg)
    
    # Cross-field validation: hiring date should be after birth date
    birth_date_str = data.get("birth_date", "").strip()
    hiring_date_str = data.get("hiring_date", "").strip()
    
    if birth_date_str and hiring_date_str:
        try:
            birth_date = datetime.strptime(birth_date_str, DATE_FORMAT)
            hiring_date = datetime.strptime(hiring_date_str, DATE_FORMAT)
            
            if hiring_date <= birth_date:
                errors.append("Hiring date must be after birth date.")
            
            # Employee should be at least 16 years old at hiring
            age_at_hiring = (hiring_date - birth_date).days / 365.25
            if age_at_hiring < 16:
                errors.append("Employee must be at least 16 years old at the time of hiring.")
                
        except ValueError:
            # Date parsing already handled above
            pass
    
    return len(errors) == 0, errors
