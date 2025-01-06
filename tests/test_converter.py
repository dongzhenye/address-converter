import pytest
from address_converter import (
    evm_to_tron,
    tron_to_evm,
    get_address_type,
    normalize_evm_address,
    validate_tron_base58_address,
    validate_tron_hex_address
)

# 有效的测试地址
VALID_EVM_ADDRESS = "0x123456789abcdef123456789abcdef123456789a"
VALID_TRON_BASE58 = "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
VALID_TRON_HEX = "41123456789abcdef123456789abcdef123456789a"

# 基本功能测试
def test_evm_to_tron_base58():
    """测试EVM地址转波场Base58格式"""
    tron_address = evm_to_tron(VALID_EVM_ADDRESS, output_format='base58')
    assert isinstance(tron_address, str)
    assert tron_address.startswith('T')
    assert validate_tron_base58_address(tron_address)

def test_evm_to_tron_hex():
    """测试EVM地址转波场Hex格式"""
    tron_address = evm_to_tron(VALID_EVM_ADDRESS, output_format='hex')
    assert isinstance(tron_address, str)
    assert tron_address.startswith('41')
    assert validate_tron_hex_address(tron_address)

def test_tron_to_evm():
    """测试波场地址转EVM格式"""
    evm_address = tron_to_evm(VALID_TRON_BASE58)
    assert isinstance(evm_address, str)
    assert evm_address.startswith('0x')
    assert len(evm_address) == 42

# 参数化测试：地址类型检测
@pytest.mark.parametrize("address,expected_type", [
    (VALID_EVM_ADDRESS, "evm"),
    ("123456789abcdef123456789abcdef123456789a", "evm"),  # 无前缀EVM地址
    (VALID_TRON_BASE58, "tron_base58"),
    (VALID_TRON_HEX, "tron_hex"),
    ("invalid_address", None),
    ("", None),
    (" ", None),
])
def test_address_type_detection(address, expected_type):
    """测试地址类型检测功能"""
    assert get_address_type(address) == expected_type

# 参数化测试：无效输入处理
@pytest.mark.parametrize("invalid_address,expected_error", [
    ("0x123", "Invalid EVM address length"),  # 地址太短
    ("0xGGGG", "Invalid hex characters"),  # 非法字符
    (None, "Address must be a string"),  # 非字符串输入
    ("", "Empty address"),  # 空地址
    (" ", "Empty address"),  # 空白地址
])
def test_invalid_inputs(invalid_address, expected_error):
    """测试无效输入的错误处理"""
    with pytest.raises(ValueError, match=expected_error):
        evm_to_tron(invalid_address)

# 双向转换一致性测试
@pytest.mark.parametrize("original_address", [
    VALID_EVM_ADDRESS,
    "0X123456789ABCDEF123456789ABCDEF123456789A",  # 大写地址
    "123456789abcdef123456789abcdef123456789a",    # 无前缀地址
])
def test_bidirectional_conversion(original_address):
    """测试地址转换的双向一致性"""
    # EVM -> TRON -> EVM
    tron_address = evm_to_tron(original_address)
    converted_back = tron_to_evm(tron_address)
    
    # 移除0x前缀后比较
    assert converted_back.lower().replace('0x', '') == original_address.lower().replace('0x', '')
    
    # TRON -> EVM -> TRON
    evm_address = tron_to_evm(VALID_TRON_BASE58)
    converted_back = evm_to_tron(evm_address)
    assert converted_back == VALID_TRON_BASE58

# 格式选项测试
def test_format_options():
    """测试不同的格式选项"""
    # 测试output_format选项
    with pytest.raises(ValueError, match="output_format must be 'base58' or 'hex'"):
        evm_to_tron(VALID_EVM_ADDRESS, output_format='invalid')
    
    # 测试add_prefix选项
    assert not tron_to_evm(VALID_TRON_BASE58, add_prefix=False).startswith('0x')
    assert tron_to_evm(VALID_TRON_BASE58, add_prefix=True).startswith('0x')

# 地址验证测试
def test_address_validation():
    """测试地址验证功能"""
    # Base58地址验证
    assert validate_tron_base58_address(VALID_TRON_BASE58)
    assert not validate_tron_base58_address("T" + "1" * 33)  # 无效的Base58地址
    
    # Hex地址验证
    assert validate_tron_hex_address(VALID_TRON_HEX)
    assert not validate_tron_hex_address("42" + "1" * 40)  # 无效的前缀
    assert not validate_tron_hex_address("41" + "1" * 39)  # 无效的长度

# 大小写处理测试
def test_case_handling():
    """测试地址大小写处理"""
    upper_evm = VALID_EVM_ADDRESS.upper()
    lower_evm = VALID_EVM_ADDRESS.lower()
    
    # 确保大小写输入得到相同结果
    assert evm_to_tron(upper_evm) == evm_to_tron(lower_evm)
    
    # 确保输出的EVM地址始终是小写的
    assert tron_to_evm(VALID_TRON_BASE58) == tron_to_evm(VALID_TRON_BASE58).lower() 