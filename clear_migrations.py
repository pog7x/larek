#!/usr/bin/env python

import os

for name, folders, files in os.walk(os.curdir):
    if name.endswith("migrations"):
        for file in files:
            if file != "__init__.py":
                migr_path = f"{name}/{file}"
                print("Cleaning up migration:", migr_path)
                os.remove(migr_path)
