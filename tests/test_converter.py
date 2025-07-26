import pytest

from address_converter import (evm_to_tron, get_address_type, tron_to_evm,
                               validate_tron_base58_address,
                               validate_tron_hex_address)

# Valid test addresses
VALID_EVM_ADDRESS = "0x123456789abcdef123456789abcdef123456789a"
VALID_TRON_BASE58 = "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
VALID_TRON_HEX = "41123456789abcdef123456789abcdef123456789a"


# Basic functionality tests
def test_evm_to_tron_base58():
    """Test converting EVM address to Base58 format"""
    tron_address = evm_to_tron(VALID_EVM_ADDRESS, output_format="base58")
    assert isinstance(tron_address, str)
    assert tron_address.startswith("T")
    assert validate_tron_base58_address(tron_address)


def test_evm_to_tron_hex():
    """Test converting EVM address to hex format"""
    tron_address = evm_to_tron(VALID_EVM_ADDRESS, output_format="hex")
    assert isinstance(tron_address, str)
    assert tron_address.startswith("41")
    assert validate_tron_hex_address(tron_address)


def test_tron_to_evm():
    """Test converting from alternative format to EVM format"""
    evm_address = tron_to_evm(VALID_TRON_BASE58)
    assert isinstance(evm_address, str)
    assert evm_address.startswith("0x")
    assert len(evm_address) == 42


# Parameterized tests: address type detection
@pytest.mark.parametrize(
    "address,expected_type",
    [
        (VALID_EVM_ADDRESS, "evm"),
        ("123456789abcdef123456789abcdef123456789a", "evm"),  # Unprefixed EVM address
        (VALID_TRON_BASE58, "tron_base58"),
        (VALID_TRON_HEX, "tron_hex"),
        ("invalid_address", None),
        ("", None),
        (" ", None),
    ],
)
def test_address_type_detection(address, expected_type):
    """Test address type detection functionality"""
    assert get_address_type(address) == expected_type


# Parameterized tests: invalid input handling
@pytest.mark.parametrize(
    "invalid_address,expected_error",
    [
        ("0x123", "Invalid EVM address length"),  # Address too short
        ("0xGGGG", "Invalid hex characters"),  # Invalid characters
        (None, "Address must be a string"),  # Non-string input
        ("", "Empty address"),  # Empty address
        (" ", "Empty address"),  # Blank address
    ],
)
def test_invalid_inputs(invalid_address, expected_error):
    """Test handling of invalid inputs"""
    with pytest.raises(ValueError, match=expected_error):
        evm_to_tron(invalid_address)


# Bidirectional conversion consistency tests
@pytest.mark.parametrize(
    "original_address",
    [
        VALID_EVM_ADDRESS,
        "0X123456789ABCDEF123456789ABCDEF123456789A",  # Uppercase address
        "123456789abcdef123456789abcdef123456789a",  # Unprefixed address
    ],
)
def test_bidirectional_conversion(original_address):
    """Test bidirectional consistency of address conversion"""
    # EVM -> Alternative -> EVM
    tron_address = evm_to_tron(original_address)
    converted_back = tron_to_evm(tron_address)

    # Compare after removing 0x prefix
    assert converted_back.lower().replace("0x", "") == original_address.lower().replace(
        "0x", ""
    )

    # Alternative -> EVM -> Alternative
    evm_address = tron_to_evm(VALID_TRON_BASE58)
    converted_back = evm_to_tron(evm_address)
    assert converted_back == VALID_TRON_BASE58


# Format options tests
def test_format_options():
    """Test different format options"""
    # Test output_format option
    with pytest.raises(ValueError, match="output_format must be 'base58' or 'hex'"):
        evm_to_tron(VALID_EVM_ADDRESS, output_format="invalid")

    # Test add_prefix option
    assert not tron_to_evm(VALID_TRON_BASE58, add_prefix=False).startswith("0x")
    assert tron_to_evm(VALID_TRON_BASE58, add_prefix=True).startswith("0x")


# Address validation tests
def test_address_validation():
    """Test address validation functionality"""
    # Base58 address validation
    assert validate_tron_base58_address(VALID_TRON_BASE58)
    assert not validate_tron_base58_address("T" + "1" * 33)  # Invalid Base58 address

    # Hex address validation
    assert validate_tron_hex_address(VALID_TRON_HEX)
    assert not validate_tron_hex_address("42" + "1" * 40)  # Invalid prefix
    assert not validate_tron_hex_address("41" + "1" * 39)  # Invalid length


# Case handling tests
def test_case_handling():
    """Test case handling"""
    upper_evm = VALID_EVM_ADDRESS.upper()
    lower_evm = VALID_EVM_ADDRESS.lower()

    # Ensure case-insensitive input yields the same result
    assert evm_to_tron(upper_evm) == evm_to_tron(lower_evm)

    # Ensure output EVM address is always lowercase
    assert tron_to_evm(VALID_TRON_BASE58) == tron_to_evm(VALID_TRON_BASE58).lower()


# 添加新的测试用例
def test_base58_decode_errors():
    """Test Base58 decoding error handling"""
    with pytest.raises(ValueError, match="Invalid Base58Check address"):
        tron_to_evm("T" + "I" * 33)  # 'I' is not a valid Base58 character
    
    with pytest.raises(ValueError, match="Invalid Base58Check address"):
        tron_to_evm("T" + "1" * 33)  # Invalid checksum


@pytest.mark.parametrize(
    "address,expected_type",
    [
        ("0x" + "0" * 40, "evm"),  # All zeros
        ("0x" + "f" * 40, "evm"),  # All f's
        ("41" + "0" * 40, "tron_hex"),  # All zeros after prefix
        (None, None),  # None input
        (123, None),  # Non-string input
        (True, None),  # Boolean input
        ("0x" + " " * 40, None),  # Spaces in address
        ("41" + " " * 40, None),  # Spaces in hex
    ],
)
def test_address_type_edge_cases(address, expected_type):
    """Test edge cases for address type detection"""
    assert get_address_type(address) == expected_type


def test_special_characters():
    """Test handling of special characters in addresses"""
    special_chars = [
        "0x123\t456",  # Tab character
        "0x123\n456",  # Newline character
        "0x123\r456",  # Carriage return
        "0x123 456",   # Space in middle
        "0x123\u00A0456",  # Non-breaking space
    ]
    
    for addr in special_chars:
        with pytest.raises(ValueError):
            evm_to_tron(addr)
            
        with pytest.raises(ValueError):
            tron_to_evm(addr)


def test_hex_validation_edge_cases():
    """Test edge cases for hex address validation"""
    # Test almost valid addresses
    assert not validate_tron_hex_address("41" + "0" * 39)  # One character short
    assert not validate_tron_hex_address("41" + "0" * 41)  # One character long
    assert not validate_tron_hex_address("40" + "0" * 40)  # Wrong prefix
    
    # Test invalid hex characters
    assert not validate_tron_hex_address("41" + "g" * 40)  # Invalid hex char
    assert not validate_tron_hex_address("41" + "G" * 40)  # Invalid hex char


def test_base58_validation_edge_cases():
    """Test edge cases for Base58 address validation"""
    # Test almost valid addresses
    assert not validate_tron_base58_address("A" + "1" * 33)  # Wrong prefix
    assert not validate_tron_base58_address("T" + "1" * 32)  # Too short
    assert not validate_tron_base58_address("T" + "1" * 34)  # Too long
    
    # Test invalid Base58 characters
    assert not validate_tron_base58_address("T" + "I" * 33)  # 'I' not in Base58
    assert not validate_tron_base58_address("T" + "O" * 33)  # 'O' not in Base58


def test_conversion_exceptions():
    """Test exception handling in conversion functions"""
    with pytest.raises(ValueError, match="Invalid hex characters in EVM address"):
        evm_to_tron("0x" + "g" * 40)
    
    with pytest.raises(ValueError, match="Invalid hex address"):
        tron_to_evm("41" + "g" * 40)


def test_get_address_type_comprehensive():
    """Test comprehensive scenarios for address type detection"""
    test_cases = [
        # EVM address variations
        ("0x" + "a" * 40, "evm"),
        ("0x" + "A" * 40, "evm"),
        ("0X" + "a" * 40, "evm"),
        # TRON hex variations
        ("41" + "a" * 40, "tron_hex"),
        ("0x41" + "a" * 40, "tron_hex"),
        # Invalid cases
        ("0x" + "a" * 39, None),  # Too short EVM
        ("0x" + "a" * 41, None),  # Too long EVM
        ("42" + "a" * 40, None),  # Wrong prefix
        ("0x42" + "a" * 40, None),  # Wrong prefix with 0x
        # Special cases
        (123.456, None),  # Float input
        ([], None),  # List input
        ({}, None),  # Dict input
    ]
    
    for address, expected in test_cases:
        assert get_address_type(address) == expected


def test_validation_error_handling():
    """Test error handling in validation functions"""
    invalid_inputs = [
        None,
        123,
        True,
        [],
        {},
        "0x" + "g" * 40,  # Invalid hex chars
        "41" + "g" * 40,  # Invalid hex chars in address
    ]
    
    for invalid_input in invalid_inputs:
        assert not validate_tron_base58_address(invalid_input)
        assert not validate_tron_hex_address(invalid_input)


def test_get_address_type_edge_cases():
    """Test edge cases for address type detection"""
    edge_cases = [
        ("0x" + "0" * 40, "evm"),  # All zeros
        ("0X" + "F" * 40, "evm"),  # All F's with capital 0X
        ("41" + "0" * 40, "tron_hex"),  # All zeros after prefix
        ("0x41" + "0" * 40, "tron_hex"),  # TRON hex with 0x prefix
        ("T" + "1" * 33, None),  # Invalid Base58
        ("0x" + "g" * 40, None),  # Invalid hex chars
        ("41" + "g" * 40, None),  # Invalid hex
        (" ", None),  # Just space
        ("", None),  # Empty string
        (None, None),  # None
        (123, None),  # Integer
        (True, None),  # Boolean
    ]
    
    for address, expected in edge_cases:
        assert get_address_type(address) == expected
