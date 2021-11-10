TITLE="EPIC UBNT-1101-PANEL"

PKG_NAME="UBNT-1101-PANEL"
PKG_VERSION="0.1"
PKG_RELEASE=2

MODULE_FILES=cpanel.py
MODULE_FILES_DIR=/usr/lib/python3.8/

.PHONY: all install

all: install

install:
	for f in $(MODULE_FILES); do cp $${f} $(MODULE_FILES_DIR); done

clean:
	for f in $(MODULE_FILES); do rm -f $(MODULE_FILES_DIR)$${f}; done
