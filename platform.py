import os
import sys
import platform

from parsley import makeGrammar

grammar = """
    wsp ...
    """
tests = [
    "A",
    "A.B-C_D",
    "aa",
    "name",
    "name<=1",
    "name>=3",''
    "name>=3,<2",
    "name@http://foo.com",
    "name [fred,bar] @ http://foo.com ; python_version=='2.7'",
    "name[quux, strange];python_version<'2.7' and platform_version=='2'",
    "name; os_name=='a' or os_name=='b'",
    # Should parse as (a and b) or c
    "name; os_name=='a' and os_name=='b' or os_name=='c'",
    # Overriding precedence -> a and (b or c)
    "name; os_name=='a' and (os_name=='b' or os_name=='c')",
    # should parse as a or (b and c)
    "name; os_name=='a' or os_name=='b' and os_name=='c'",
    # Overriding precedence -> (a or b) and c
    "name; (os_name=='a' or os_name=='b') and os_name=='c'",
    ]

def format_full_version(info):
    version = '{0.major}.{0.minor}.{0.micro}'.format(info)
    kind = info.releaselevel
    if kind != 'final':
        version += kind[0] + str(info.serial)
    return version

if hasattr(sys, 'implementation'):
    implementation_version = format_full_version(sys.implementation.version)
    implementation_name = sys.implementation.name
else:
    implementation_version = '0'
    implementation_name = ''
bindings = {
    'implementation_name': implementation_name,
    'implementation_version': implementation_version,
    'os_name': os.name,
    'platform_machine': platform.machine(),
    'platform_python_implementation': platform.python_implementation(),
    'platform_release': platform.release(),
    'platform_system': platform.system(),
    'platform_version': platform.version(),
    'python_full_version': platform.python_version(),
    'python_version': '.'.join(platform.python_version_tuple()[:2]),
    'sys_platform': sys.platform,
}

compiled = makeGrammar(grammar, {'lookup': bindings.__getitem__})
for test in tests:
    parsed = compiled(test).specification()
    print("%s -> %s" % (test, parsed))