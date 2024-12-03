import requests

def main():
    version_manifest = requests.get('https://gist.githubusercontent.com/cliffano/77a982a7503669c3e1acb0a0cf6127e9/raw/a36b1e2f05ed3f1d1bbe9a7cf7fd3cfc7cb7a3a8/minecraft-server-jar-downloads.md')
    version_manifest_by_line = version_manifest.text.split('\n')[2:]
    versions = {}
    
    for version in version_manifest_by_line:
        split = version.split('|')
        versions[split[1].strip()]= split[2].strip()
    
    # print(version_manifest[13])    
    print(versions.items())

main()