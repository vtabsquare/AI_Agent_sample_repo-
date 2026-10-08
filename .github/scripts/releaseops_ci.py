"""Copy to TARGET .github/scripts/releaseops_ci.py. No control-panel secrets are required."""
import json,os,pathlib,subprocess,sys,xml.etree.ElementTree as ET
root=pathlib.Path('candidate').resolve()
phase=os.environ['TEST_PHASE']
sha=os.environ['CANDIDATE_SHA']
report={'sha':sha,'session_id':os.environ['SESSION_ID'],'phase':phase,'exit_code':1,'passed':0,'failed':0,'log':''}
try:
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if actual!=sha: raise ValueError('Checked-out SHA mismatch')
    if phase=='unit':
        command=[sys.executable,'-m','pytest','--junitxml=unit.xml'] if os.environ['CODE_TYPE']=='python' else ['npm','run','test:unit','--','--reporter=junit','--outputFile=unit.xml']
    else:
        from urllib.parse import urlparse
        u=urlparse(os.environ.get('TARGET_URL',''))
        if u.scheme!='https' or not (u.hostname or '').endswith('.onrender.com'): raise ValueError('Target must be a verified Render HTTPS URL')
        # Projects use process.env.BASE_URL in their Playwright configuration.
        os.environ['BASE_URL']=os.environ['TARGET_URL']
        command=['npx','--no-install','playwright','test','--reporter=json']
    process=subprocess.run(command,cwd=root,text=True,capture_output=True,timeout=600)
    (root/'test-output.log').write_text((process.stdout+process.stderr)[-50000:],encoding='utf-8')
    report['log']=(process.stdout+process.stderr)[-12000:]
    report['exit_code']=process.returncode
    if phase=='unit':
        tree=ET.parse(root/'unit.xml')
        suites=[tree.getroot()] if tree.getroot().tag=='testsuite' else tree.getroot().findall('.//testsuite')
        total=sum(int(s.get('tests',0)) for s in suites)
        failed=sum(int(s.get('failures',0))+int(s.get('errors',0)) for s in suites)
        skipped=sum(int(s.get('skipped',0)) for s in suites)
        report.update(passed=total-failed-skipped,failed=failed)
    else:
        data=json.loads(process.stdout)
        stats=data['stats']
        report.update(passed=int(stats.get('expected',0)),failed=int(stats.get('unexpected',0))+int(stats.get('flaky',0)))
    if report['passed']<1 or report['failed'] or report['exit_code']!=0: report['exit_code']=1
except Exception as exc:
    report.update(exit_code=1,log=str(exc))
finally:
    root.mkdir(exist_ok=True)
    (root/'releaseops-report.json').write_text(json.dumps(report),encoding='utf-8')
sys.exit(report['exit_code'])
