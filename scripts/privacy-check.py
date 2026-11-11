#!/usr/bin/env python3
import pathlib,re,subprocess,json,xml.etree.ElementTree as ET
p=pathlib.Path(__file__).resolve().parent.parent
names=["a"+"rezki","chou"+"gar","kech"+"idi","fe"+"lla"]
paths=["/srv/"+"lxc/","/home/"+"arezki","home"+".arpa"]
patterns=[re.compile(re.escape(s),re.I) for s in names+paths]
patterns += [re.compile(r"192[.]168[.]"+r"\d{1,3}[.]\d{1,3}"),
             re.compile("-----BEGIN "+"PRIVATE KEY"),
             re.compile(r"ghp_[A-Za-z0-9]{25}"),
             re.compile(r"github_pat_[A-Za-z0-9_]{30}")]
subprocess.run(['git','-C',str(p),'rev-parse','--is-inside-work-tree'],check=True,capture_output=True)
data=subprocess.check_output(['git','-C',str(p),'ls-files','-z']).decode('utf8','replace').split(chr(0))
violations=[]
for path in data:
 if not path or path=='scripts/privacy-check.py':continue
 f=p/path
 if not f.is_file() or f.stat().st_size>2_000_000:continue
 b=f.read_bytes()
 if bytes([0]) in b[:4096]:continue
 if any(regex.search(b.decode('utf8','replace')) for regex in patterns):violations.append(path)
assert not violations, 'REVIEW_PRIVATE_FIELDS '+str(sorted(set(violations)))
contract=json.loads((p/'contract-tools.json').read_text())
assert len(contract)==97
ET.parse(p/'docs/assets/logo.svg');ET.parse(p/'docs/assets/tool-map.svg')
print("YOUTUBE_PUBLIC_PRIVACY_AND_97_TOOL_CONTRACT_PASS")
