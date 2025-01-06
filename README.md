# Address Converter

A lightweight Python library for converting addresses between EVM-compatible chains and TRON network.

[![PyPI version](https://badge.fury.io/py/address-converter.svg)](https://badge.fury.io/py/address-converter)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- Convert addresses between EVM-compatible chains and TRON network
- Support both Base58Check and Hex formats for TRON addresses
- Comprehensive address validation
- Zero dependencies except for `base58`
- Type hints support
- Thoroughly tested

## Installation

```bash
pip install address-converter
```

## Quick Start

```python
from address_converter import evm_to_tron, tron_to_evm, get_address_type

# Convert EVM address to TRON address
evm_address = "0x123456789abcdef123456789abcdef123456789a"
tron_base58 = evm_to_tron(evm_address, output_format='base58')
tron_hex = evm_to_tron(evm_address, output_format='hex')

print(f"TRON Base58: {tron_base58}")
print(f"TRON Hex: {tron_hex}")

# Convert TRON address to EVM address
tron_address = "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
evm_result = tron_to_evm(tron_address, add_prefix=True)
print(f"EVM: {evm_result}")

# Detect address type
address_type = get_address_type(evm_address)
print(f"Address type: {address_type}")  # 'evm'
```

## API Reference

### `evm_to_tron(evm_address: str, output_format: str = 'base58') -> str`

Convert an EVM address to TRON format.

- **Parameters:**
  - `evm_address`: EVM address (with or without '0x' prefix)
  - `output_format`: Output format, either 'base58' or 'hex'
- **Returns:** TRON address in specified format
- **Raises:** ValueError if address is invalid

### `tron_to_evm(tron_address: str, add_prefix: bool = True) -> str`

Convert a TRON address to EVM format.

- **Parameters:**
  - `tron_address`: TRON address (Base58Check or Hex format)
  - `add_prefix`: Whether to add '0x' prefix
- **Returns:** EVM address
- **Raises:** ValueError if address is invalid

### `get_address_type(address: str) -> Optional[str]`

Detect address type.

- **Parameters:**
  - `address`: Address to detect
- **Returns:** 'evm', 'tron_base58', 'tron_hex', or None if invalid

## Address Format Details

### EVM Address

- 40 hexadecimal characters (excluding '0x' prefix)
- Case-insensitive
- Optional '0x' prefix

### TRON Address

- Base58Check format: Starts with 'T', 34 characters
- Hex format: Starts with '41', 42 characters (excluding '0x' prefix)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TRON Address Format](https://developers.tron.network/docs/account#address-format)
- [EVM Address Format](https://ethereum.org/en/developers/docs/accounts/)

## Support

If you have any questions or need help, please:

1. Check the [issues](https://github.com/dongzhenye/address-converter/issues) page
2. Create a new issue if you can't find an answer

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dongzhenye/address-converter&type=Date)](https://star-history.com/#dongzhenye/address-converter&Date)
