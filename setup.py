import cx_Freeze

executables = [cx_Freeze.Executable("CramClient.py")]

cx_Freeze.setup(
    name="Cram Client",
    options={"build.exe": {"packages": ["pygame"],
                           "included_files":[img]},
    executables = executables
)