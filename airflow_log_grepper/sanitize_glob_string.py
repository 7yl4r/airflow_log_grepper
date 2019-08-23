
def sanitize_glob_string(glob_str):
    """
    Replaces characters in a glob string which might offend airflow's DAG and
    task naming conventions or graphite's metric namespacing.

    I.e. : convert glob strings to underscores, letters, numbers while trying
           to preserve the meaning of the glob.

   This works best if the glob_str uses only lowercase letters, because the
   replacements use uppercase letters.
    """
    for offensive_char, replacement in [
        ['*', 'X'],
        ['[', 'I'],
        [']', 'I'],
        ['{', 'I'],
        ['}', 'I'],
        [',', 'I'],
        ['.', 'O'],
        ['-', 'T'],
        ['?', 'Q'],
        ['/', 'V'],
    ]:
        glob_str = glob_str.replace(offensive_char, replacement)
    return glob_str
