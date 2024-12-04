# import hashlib
from optional import Nothing, Option, Optional, Something
import requests
from io import BytesIO
from pathlib import Path

type Error = str
type Result[T] = T | Error

def main():
    mojang_mani = get_mojang_manifest('https://gist.githubusercontent.com/cliffano/77a982a7503669c3e1acb0a0cf6127e9/raw/a36b1e2f05ed3f1d1bbe9a7cf7fd3cfc7cb7a3a8/minecraft-server-jar-downloads.md') 
    cursor_index = 0
    global jar
    jar = Nothing
    help_string = '\n\th -- Display this help screen\n\tj -- Scroll down\n\tk -- Scroll up\
        \n\tls -- list all\n\tq -- Exit program\n'

    print(list_manifest_versions(mojang_mani, cursor_index, 5))
    print('Please select a version', end='')
    while(True):
        print(': ', end='')
        user_selection = input()
        match user_selection:
            case 'j' | 'J': 
                cursor_index = cursor_index + 1 if cursor_index < len(mojang_mani) else cursor_index
                print(list_manifest_versions(mojang_mani, cursor_index, 5))
            case 'k' | 'K': 
                cursor_index = cursor_index - 1 if cursor_index > 1 else cursor_index
                print(list_manifest_versions(mojang_mani, cursor_index, 5))
            case 'q' | 'Q':
                print('Exiting. . .')
                exit()
            case 'h' | 'H' | 'help':
                print(help_string)
            case 'ls':
                print(list_manifest_versions(mojang_mani, 0, len(mojang_mani)))
            case _: 
                if user_selection in mojang_mani:
                    print(f'Selected {user_selection}. Downloading. . .')
                    jar = Optional.of(download_jar(user_selection, mojang_mani[user_selection]))
                    break
                else:
                    print(f'\nInvalid entry. Enter a valid version number or see the commands below: {help_string}')

def download_jar(version_name: str, url: str) -> Result[Path]:    
    r = requests.get(url)
    container = Path('server_files')
    if not container.exists():
        container.mkdir()
    written_path = Path(container, f'{version_name}_server.jar')
    try:
        with open(written_path, 'wb') as file:
            file.write(BytesIO(r.content).getbuffer())
    except BlockingIOError as err:
        return f'BlockingIOError: {err}'
    except OSError as err:
        return f'OSError: {err}'
    
    return written_path

def get_mojang_manifest(url: str) -> dict[str, str]:
    version_manifest = requests.get(url)
    version_manifest_by_line = version_manifest.text.split('\n')[2:]
    
    official_versions: dict[str, str] = {}
    
    for version in version_manifest_by_line:
        split = version.split('|')
        official_versions[split[1].strip()]= split[2].strip()
    return official_versions

def list_manifest_versions(mani: dict[str, str], start_index: int, count: int) -> str:
    result = ''
    keys = [key for key in mani.keys()]
    for key_index in range(start_index, start_index + count):
        result = result + keys[key_index] + '\n'
    
    return result
        
        
# def cache_response(res: requests.Response):
#     cache = Path('.cache')
#     cache_contents = [content.name for content in cache.iterdir()]
#     if cache.exists():
#         hashed = str(hashlib.sha1(res.content))
#         if hashed in cache_contents:
#             return Optional.of(res)
#         else:
#             with open(f'{hashed}', 'w') as file:
#                 file.write(BytesIO(hashlib.sha1(res.content)).getbuffer())
                

main()