import os

for name, folders, files in os.walk(f"{os.curdir}/larek/apps"):
    if name.endswith("migrations"):
        for f in files:
            if f != "__init__.py":
                migr_path = f"{name}/{f}"
                print("Cleaning up migrations in:", migr_path)
                os.remove(migr_path)
