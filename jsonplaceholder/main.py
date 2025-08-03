import pyperclip
import time
import json

def replace_object(value: dict | list | str):
    """
    Will convert your dictionary, list or stringified JSON to its placeholder version.

    Args:
        value (dict | list | str: JSON)

    Returns:
        str: The placeholdered object
    """
    if not isinstance(value, str) and not isinstance(value, list) and not isinstance(value, dict):
        raise TypeError("Param must be string or dictionary")

    # convert to list or dict 
    try:
        if isinstance(value, str):
            value = json.loads(value)
    except json.JSONDecodeError:
        raise TypeError(f'"{value}" is an invalid JSON')

    if isinstance(value, list):
        for i in range(0, len(value)):
            if isinstance(value[i], str) or isinstance(value[i], int) or isinstance(value[i], float) or isinstance(value[i], bool):
                value[i] = set_placeholder(value[i])
            elif isinstance(value[i], dict) or isinstance(value[i], list):
                replace_object(value[i])

    elif isinstance(value, dict):
        for key in value:
            if isinstance(value[key], str) or isinstance(value[key], int) or isinstance(value[key], float) or isinstance(value[key], bool):
                value[key] = set_placeholder(value[key])
            elif isinstance(value[key], dict) or isinstance(value[key], list):
                replace_object(value[key])

    return json.dumps(value, sort_keys=True, indent=4)

def set_placeholder(value: str | int | float | bool, ) -> str:
    """
    Convert the given value to its placeholder

    Args:
        value (str | int | float | bool)

    Returns:
        str: "xxx" | 123 | 1.23 | true/false
    """
    placeholders: dict = {
        "str"   : '"xxx"',
        "int"   : "123",
        "float" : "1.23",
        "bool"  : "true/false",
    }
    return placeholders.get(type(value).__name__)

def remove_quotes(value: str) -> str:
    """
    Remove all unescaped quotes (single and double) from the string,
    but keep escaped ones like \" or \'
    """
    # Temporary aliases to protect escaped quotes
    alias: dict = {
        "double_quote" : "fjkaniv5un8ount89vcn37-jkcwtmekfion",
        "single_quote" : "vtiurpcxjk99hviuhspcm8t4cq7j98 pfio"
    }

    # Protect escaped quotes
    value = value.replace('\\\"', alias["double_quote"])
    value = value.replace("\\\'", alias["single_quote"])

    # Remove remaining (unescaped) quotes
    value = value.replace('\"', '')
    value = value.replace("\'", '')

    # Restore escaped quotes
    value = value.replace(alias["double_quote"], '\"')
    value = value.replace(alias["single_quote"], "\'")

    return value

def run_default():
    print()
    clipboard_cached: str = ""
    time_pass: int = 0
    while True:
        clipboard: str = pyperclip.paste()

        if clipboard != clipboard_cached:
            clipboard_cached = clipboard
            try:
                obj: str = replace_object(clipboard)
                noquote: str = remove_quotes(obj)

                clipboard_cached = noquote
                pyperclip.copy(noquote)

                print(f"{time_pass}: \n{noquote} \nhas been copied to clipboard")
            except Exception as e:
                print(f"{time_pass}: {e}")
        else:
            print(f"{time_pass}: Waiting")

        time_pass += 1
        time.sleep(1)

if (__name__) == "__main__": 
    run_default()