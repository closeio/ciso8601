#!/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w "wheelhouse/$PLAT/"
    fi
}

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" wheel /root/project/ --no-deps -w wheelhouse_pre_audit/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse_pre_audit/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install ciso8601 --no-index -f "/root/project/wheelhouse/$PLAT/"
    (cd /root/project/; "${PYBIN}/python" setup.py test)
done
