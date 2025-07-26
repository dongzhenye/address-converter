# Address Converter

A lightweight Python library for converting blockchain addresses between different formats, with initial support for EVM-compatible chains and other blockchain networks.

[![PyPI version](https://badge.fury.io/py/address-converter.svg)](https://badge.fury.io/py/address-converter)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- Convert addresses between different blockchain formats
- Support multiple encoding formats (Base58Check, Hex)
- Comprehensive address validation
- Minimal dependencies (only `base58`)
- Type hints support
- Thoroughly tested

## Installation

```bash
pip install address-converter
```

## Quick Start

```python
from address_converter import evm_to_tron, tron_to_evm, get_address_type

# Convert EVM format to alternative format
evm_address = "0x123456789abcdef123456789abcdef123456789a"
alt_base58 = evm_to_tron(evm_address, output_format='base58')
alt_hex = evm_to_tron(evm_address, output_format='hex')

print(f"Base58 format: {alt_base58}")
print(f"Hex format: {alt_hex}")

# Convert from alternative format to EVM
alt_address = "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
evm_result = tron_to_evm(alt_address, add_prefix=True)
print(f"EVM format: {evm_result}")

# Detect address type
address_type = get_address_type(evm_address)
print(f"Address type: {address_type}")  # 'evm'
```

## API Reference

### `evm_to_tron(evm_address: str, output_format: str = 'base58') -> str`

Convert an EVM address to alternative blockchain format.

- **Parameters:**
  - `evm_address`: EVM address (with or without '0x' prefix)
  - `output_format`: Output format, either 'base58' or 'hex'
- **Returns:** Address in specified format
- **Raises:** ValueError if address is invalid

### `tron_to_evm(tron_address: str, add_prefix: bool = True) -> str`

Convert an address from alternative blockchain format to EVM format.

- **Parameters:**
  - `tron_address`: Address in Base58Check or Hex format
  - `add_prefix`: Whether to add '0x' prefix
- **Returns:** EVM address
- **Raises:** ValueError if address is invalid

### `get_address_type(address: str) -> Optional[str]`

Detect address type.

- **Parameters:**
  - `address`: Address to detect
- **Returns:** Address type string ('evm', 'tron_base58', 'tron_hex') or None if invalid

## Address Format Details

### EVM Address

- 40 hexadecimal characters (excluding '0x' prefix)
- Case-insensitive
- Optional '0x' prefix

### Alternative Address Formats

- Base58Check format: Specific prefix character, fixed length
- Hex format: Specific byte prefix, fixed length

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Technical References

- [EVM Address Format](https://ethereum.org/en/developers/docs/accounts/)
- [Base58Check Encoding](https://en.bitcoin.it/wiki/Base58Check_encoding)
- Various blockchain address format specifications

## Support

If you have any questions or need help, please:

1. Check the [issues](https://github.com/dongzhenye/address-converter/issues) page
2. Create a new issue if you can't find an answer

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dongzhenye/address-converter&type=Date)](https://star-history.com/#dongzhenye/address-converter&Date)

## Disclaimer

This is an independent open-source project developed for educational and research purposes. It is not affiliated with, endorsed by, or connected to any organization or entity. The code is provided "as is" under the MIT License.
