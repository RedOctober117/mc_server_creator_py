# import hashlib
# from optional import Nothing, Option, Optional, Something
import requests
from io import BytesIO
# from pathlib import Path

def main():
    mojang_mani = get_mojang_manifest('https://gist.githubusercontent.com/cliffano/77a982a7503669c3e1acb0a0cf6127e9/raw/a36b1e2f05ed3f1d1bbe9a7cf7fd3cfc7cb7a3a8/minecraft-server-jar-downloads.md') 
      
    print(list_manifest_versions(mojang_mani, 0, 5))
    # print('Please choose a version to download: ', end='')
    
    # selection = input()
    
    # if selection in mojang_mani.keys():
    #     print(f'Selected {selection}. Downloading. . .')
    # else:
    #     print('Invalid selection, shutting down. . .')
    #     exit()
    
    # r = requests.get(mojang_mani[selection])
    
    # with open(f'{selection}_server.jar', 'wb') as file:
    #     file.write(BytesIO(r.content).getbuffer())

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