from distutils.core import setup, Extension
setup(name="BST", version="1.0",
      ext_modules=[
          Extension("BST", sources=["BST_module.cpp"])
      ]
)