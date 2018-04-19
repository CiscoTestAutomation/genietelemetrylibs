# Enable abstraction; This is the root package.
__import__('abstract').declare_package(__name__)

from .plugin import Plugin