from base58 import b58encode_check, b58decode_check
from typing import Optional

def normalize_evm_address(evm_address: str) -> str:
    """规范化EVM地址格式
    
    Args:
        evm_address: 0x开头或纯hex的EVM地址
        
    Returns:
        规范化的EVM地址(小写,不含0x前缀)
        
    Raises:
        ValueError: 当地址格式无效时
    """
    if not isinstance(evm_address, str):
        raise ValueError('Address must be a string')
        
    if not evm_address or evm_address.isspace():
        raise ValueError('Empty address')
        
    # 移除0x前缀和空格,转小写
    norm_address = evm_address.lower().replace('0x', '').strip()
    
    # 先检查是否为有效的16进制字符串
    try:
        int(norm_address, 16)
    except ValueError:
        raise ValueError('Invalid hex characters in EVM address')
        
    # 再检查长度
    if len(norm_address) != 40:
        raise ValueError(f'Invalid EVM address length: {len(norm_address)}, expected 40')
    
    return norm_address

def validate_tron_base58_address(address: str) -> bool:
    """验证波场Base58Check格式地址
    
    Args:
        address: 待验证的Base58Check格式地址
        
    Returns:
        bool: 地址是否有效
    """
    if not isinstance(address, str):
        return False
        
    if not address.startswith('T'):
        return False
        
    try:
        decoded = b58decode_check(address)
        return len(decoded) == 21 and decoded[0] == 0x41
    except Exception:
        return False

def validate_tron_hex_address(address: str) -> bool:
    """验证波场Hex格式地址
    
    Args:
        address: 待验证的Hex格式地址
        
    Returns:
        bool: 地址是否有效
    """
    if not isinstance(address, str):
        return False
        
    # 移除0x前缀和空格
    norm_address = address.lower().replace('0x', '').strip()
    
    if not norm_address.startswith('41'):
        return False
        
    if len(norm_address) != 42:
        return False
        
    try:
        int(norm_address, 16)
        return True
    except ValueError:
        return False

def evm_to_tron(evm_address: str, output_format: str = 'base58') -> str:
    """将EVM地址转换为波场地址
    
    Args:
        evm_address: 0x开头或纯hex的EVM地址
        output_format: 输出格式,'base58'或'hex'
        
    Returns:
        波场地址(Base58Check格式或Hex格式)
        
    Raises:
        ValueError: 当地址格式无效或output_format无效时
    """
    if output_format not in ['base58', 'hex']:
        raise ValueError("output_format must be 'base58' or 'hex'")
    
    # 规范化EVM地址
    evm_address = normalize_evm_address(evm_address)
    
    # 添加41前缀
    tron_hex = '41' + evm_address
    
    if output_format == 'hex':
        return tron_hex
        
    # 转换为Base58Check格式
    try:
        address_bytes = bytes.fromhex(tron_hex)
        base58check = b58encode_check(address_bytes)
        return base58check.decode()
    except Exception as e:
        raise ValueError(f'Failed to convert to Base58Check format: {str(e)}')

def tron_to_evm(tron_address: str, add_prefix: bool = True) -> str:
    """将波场地址转换为EVM地址
    
    Args:
        tron_address: T开头的Base58Check格式地址或41开头的Hex格式地址
        add_prefix: 是否添加0x前缀
        
    Returns:
        EVM地址(可选0x前缀)
        
    Raises:
        ValueError: 当地址格式无效时
    """
    if not isinstance(tron_address, str):
        raise ValueError('Address must be a string')
        
    if not tron_address or tron_address.isspace():
        raise ValueError('Empty address')
    
    # 处理Base58Check格式
    if tron_address.startswith('T'):
        if not validate_tron_base58_address(tron_address):
            raise ValueError('Invalid TRON Base58Check address')
            
        try:
            address_bytes = b58decode_check(tron_address)
            tron_hex = address_bytes.hex()
        except Exception as e:
            raise ValueError(f'Failed to decode Base58Check address: {str(e)}')
    else:
        # 处理Hex格式
        if not validate_tron_hex_address(tron_address):
            raise ValueError('Invalid TRON hex address')
            
        tron_hex = tron_address.lower().replace('0x', '').strip()
    
    # 移除41前缀
    evm_address = tron_hex[2:]
    
    return f'0x{evm_address}' if add_prefix else evm_address

def get_address_type(address: str) -> Optional[str]:
    """识别地址类型
    
    Args:
        address: 待识别的地址
        
    Returns:
        str: 地址类型 ('evm', 'tron_base58', 'tron_hex', None)
    """
    if not isinstance(address, str) or not address:
        return None
        
    address = address.strip()
    
    try:
        # 检查是否为EVM地址
        if address.startswith('0x'):
            normalize_evm_address(address)
            return 'evm'
            
        # 检查是否为波场Base58Check地址
        if validate_tron_base58_address(address):
            return 'tron_base58'
            
        # 检查是否为波场Hex地址
        if validate_tron_hex_address(address):
            return 'tron_hex'
            
        # 检查是否为不带0x前缀的EVM地址
        if len(address) == 40:
            normalize_evm_address(address)
            return 'evm'
    except ValueError:
        pass
        
    return None

# 测试用例
if __name__ == '__main__':
    test_cases = [
        '0x123456789abcdef123456789abcdef123456789a',  # 标准EVM地址
        '123456789ABCDEF123456789ABCDEF123456789A',    # 大写无前缀EVM地址
        'TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW',         # Base58Check地址
        '4154fdaf1515acfd32744cc33935817ff4d383e31f',  # Hex格式波场地址
        '0x4154fdaf1515acfd32744cc33935817ff4d383e31f', # 带0x的Hex格式波场地址
        'invalid_address',                              # 无效地址
        ''                                             # 空地址
    ]
    
    print("Testing address type detection and conversions:")
    for addr in test_cases:
        print(f'\nTesting address: {addr}')
        try:
            addr_type = get_address_type(addr)
            print(f'Address type: {addr_type}')
            
            if addr_type in ['evm']:
                tron_base58 = evm_to_tron(addr, 'base58')
                tron_hex = evm_to_tron(addr, 'hex')
                print(f'EVM -> TRON Base58: {tron_base58}')
                print(f'EVM -> TRON Hex: {tron_hex}')
                
                # 验证反向转换
                evm_back = tron_to_evm(tron_base58)
                print(f'TRON -> EVM: {evm_back}')
                
            elif addr_type in ['tron_base58', 'tron_hex']:
                evm = tron_to_evm(addr)
                print(f'TRON -> EVM: {evm}')
                
                # 验证反向转换
                tron_back = evm_to_tron(evm)
                print(f'EVM -> TRON: {tron_back}')
                
        except ValueError as e:
            print(f'Error: {str(e)}')