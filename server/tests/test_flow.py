from fastapi.testclient import TestClient
from app.main import app

def test_demo_full_text_interview_flow():
    with TestClient(app) as client:
        login=client.post('/api/auth/login',json={'email':'demo@interviewiq.ai','password':'Password@123'})
        assert login.status_code==200,login.text
        headers={'Authorization':f"Bearer {login.json()['token']}"}
        assert client.get('/api/auth/me',headers=headers).status_code==200
        resume=client.get('/api/resumes',headers=headers).json()[0]
        started=client.post('/api/interviews',headers=headers,json={'role':'Python Developer','type':'mixed','difficulty':'medium','mode':'text','total_questions':5,'resume_id':resume['id']})
        assert started.status_code==200,started.text
        sid=started.json()['id']
        categories=[]
        for _ in range(5):
            ans=client.post(f'/api/interviews/{sid}/answer',headers=headers,json={'transcript':'I diagnosed the problem, chose a solution, tested it, and measured the result.','input_mode':'text','duration_sec':45})
            assert ans.status_code==200,ans.text
            if ans.json()['next_question']:
                categories.append(ans.json()['next_question']['category'])
        assert 'coding' in categories
        assert 'resume_based' in categories
        assert ans.json()['report']['verdict'] in {'needs_improvement','average','good','excellent'}
        report=client.get(f'/api/interviews/{sid}/report',headers=headers)
        assert report.status_code==200,report.text
        assert len(report.json()['questions'])==5
        dashboard=client.get('/api/dashboard',headers=headers)
        assert dashboard.status_code==200 and dashboard.json()['total_interviews']>=1
