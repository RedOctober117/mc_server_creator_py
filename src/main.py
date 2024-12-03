import requests
from io import BytesIO

def main():
    version_manifest = requests.get('https://gist.githubusercontent.com/cliffano/77a982a7503669c3e1acb0a0cf6127e9/raw/a36b1e2f05ed3f1d1bbe9a7cf7fd3cfc7cb7a3a8/minecraft-server-jar-downloads.md')
    version_manifest_by_line = version_manifest.text.split('\n')[2:]
    
    official_versions: dict[str, str] = {}
    
    for version in version_manifest_by_line:
        split = version.split('|')
        official_versions[split[1].strip()]= split[2].strip()
    
    # print(version_manifest[13]) 
    for key in official_versions.keys():
        print(key)   
    
    print('Please choose a version to download: ', end='')
    
    selection = input()
    
    if selection in official_versions.keys():
        print(f'Selected {selection}. Downloading. . .')
    else:
        print('Invalid selection, shutting down. . .')
        exit()
    
    r = requests.get(official_versions[selection])
    
    with open(f'{selection}_server.jar', 'wb') as file:
        file.write(BytesIO(r.content).getbuffer())
main()