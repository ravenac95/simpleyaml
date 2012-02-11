
NAME = 'simpleyaml'
VERSION = '1.0'
DESCRIPTION = "YAML parser and emitter for Python"
LONG_DESCRIPTION = """
This is PyYAML but without any libyaml support.

It's packaged just in case it's useful to someone else. The original author 
is Kirill Simonov.
"""
AUTHOR = "Reuven V. Gonzales"
AUTHOR_EMAIL = 'reuven@tobetter.us'
LICENSE = "MIT"
PLATFORMS = "Any"
URL = "http://pyyaml.org/wiki/PyYAML"
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing :: Markup",
]

import sys, os.path

from distutils.core import setup, Command
from distutils.core import Distribution as _Distribution

class Distribution(_Distribution):

    def __init__(self, attrs=None):
        _Distribution.__init__(self, attrs)
        if not self.ext_modules:
            return
        for idx in range(len(self.ext_modules)-1, -1, -1):
            ext = self.ext_modules[idx]
            if not isinstance(ext, Extension):
                continue
            setattr(self, ext.attr_name, None)
            self.global_options = [
                    (ext.option_name, None,
                        "include %s (default if %s is available)"
                        % (ext.feature_description, ext.feature_name)),
                    (ext.neg_option_name, None,
                        "exclude %s" % ext.feature_description),
            ] + self.global_options
            self.negative_opt = self.negative_opt.copy()
            self.negative_opt[ext.neg_option_name] = ext.option_name

    def has_ext_modules(self):
        if not self.ext_modules:
            return False
        for ext in self.ext_modules:
            with_ext = self.ext_status(ext)
            if with_ext is None or with_ext:
                return True
        return False

    def ext_status(self, ext):
        if 'Java' in sys.version or 'IronPython' in sys.version or 'PyPy' in sys.version:
            return False
        if isinstance(ext, Extension):
            with_ext = getattr(self, ext.attr_name)
            return with_ext
        else:
            return True


class test(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_cmd = self.get_finalized_command('build')
        build_cmd.run()
        sys.path.insert(0, build_cmd.build_lib)
        if sys.version_info[0] < 3:
            sys.path.insert(0, 'tests/lib')
        else:
            sys.path.insert(0, 'tests/lib3')
        import test_all
        test_all.main([])


if __name__ == '__main__':

    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        platforms=PLATFORMS,
        url=URL,
        classifiers=CLASSIFIERS,

        package_dir={'': {2: 'lib', 3: 'lib3'}[sys.version_info[0]]},
        packages=['simpleyaml'],
        ext_modules=[],

        distclass=Distribution,

        cmdclass={
            'test': test,
        },
    )

