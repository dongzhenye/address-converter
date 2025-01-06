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
    """Test converting EVM address to TRON Base58 format"""
    tron_address = evm_to_tron(VALID_EVM_ADDRESS, output_format="base58")
    assert isinstance(tron_address, str)
    assert tron_address.startswith("T")
    assert validate_tron_base58_address(tron_address)


def test_evm_to_tron_hex():
    """Test converting EVM address to TRON hex format"""
    tron_address = evm_to_tron(VALID_EVM_ADDRESS, output_format="hex")
    assert isinstance(tron_address, str)
    assert tron_address.startswith("41")
    assert validate_tron_hex_address(tron_address)


def test_tron_to_evm():
    """Test converting TRON address to EVM format"""
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
    # EVM -> TRON -> EVM
    tron_address = evm_to_tron(original_address)
    converted_back = tron_to_evm(tron_address)

    # Compare after removing 0x prefix
    assert converted_back.lower().replace("0x", "") == original_address.lower().replace(
        "0x", ""
    )

    # TRON -> EVM -> TRON
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
