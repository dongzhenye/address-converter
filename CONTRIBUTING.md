# Contributing to Address Converter

Thanks for your interest in contributing! 

## Quick Start

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/address-converter.git
cd address-converter

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
pip install pytest
```

## Code Style

- Keep it simple and readable
- Follow existing patterns in the codebase
- Add tests for new features
- Update documentation if needed

## Adding New Address Formats

1. Add conversion logic in `converter.py`
2. Add validation functions
3. Add comprehensive tests
4. Update README with examples

## Design Philosophy

- **Simplicity First**: Choose simple solutions that work well
- **Avoid Over-engineering**: Start with the minimal viable solution
- **Backward Compatibility**: Don't break existing APIs without good reason
- **User-Focused**: APIs should be intuitive and easy to use

## Questions?

Feel free to open an issue for discussion before making big changes.