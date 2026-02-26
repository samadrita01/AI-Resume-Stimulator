import streamlit as st
import os
import tempfile
import time
import re
import random
import json
from datetime import datetime
from pathlib import Path
import base64

# Import document processing libraries
try:
    import PyPDF2
    import pdfplumber
    from docx import Document
except ImportError as e:
    st.error(f"Missing required libraries: {str(e)}")
    st.error("Please install: pip install PyPDF2 pdfplumber python-docx")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer - Global Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with animations
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 119, 180, 0.1);
        margin-bottom: 2rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease-out;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1f77b4 0%, #667eea 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: scaleIn 0.5s ease-out;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .skill-tag {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.3rem;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .skill-tag:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .upload-area:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #1f77b4;
        transform: scale(1.02);
    }
    
    .progress-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        margin: 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .progress-step.active {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(46, 204, 113, 0.3);
    }
    
    .progress-step.completed {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    }
    
    .question-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: slideInLeft 0.5s ease-out;
    }
    
    .job-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: slideInRight 0.5s ease-out;
    }
    
    .job-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        transform: translateY(-3px);
    }
    
    .success {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-out;
    }
    
    .warning {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-out;
    }
    
    .error {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-out;
    }
    
    .timer {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    .apply-btn {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .apply-btn:hover {
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
        transform: translateY(-2px);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .live-indicator {
        background: #2ecc71;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        animation: pulse 2s infinite;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    defaults = {
        'authenticated': False,
        'resume_data': None,
        'current_step': 1,
        'total_steps': 6,
        'skill_analysis': None,
        'interview_session': None,
        'interview_answers': [],
        'aptitude_session': None,
        'aptitude_answers': [],
        'job_recommendations': None,
        'applied_jobs': [],
        'performance_history': [],
        'user_profile': {},
        'real_time_updates': True,
        'current_time': datetime.now(),
        'timer_seconds': 0,
        'timer_running': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Resume processing class - NO LOCAL FILE DEPENDENCIES
class ResumeProcessor:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, file_bytes):
        try:
            import PyPDF2
            import io
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"PDF extraction error: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, file_bytes):
        try:
            import io
            from docx import Document
            docx_file = io.BytesIO(file_bytes)
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"DOCX extraction error: {str(e)}")
            return ""
    
    def extract_contact_info(self, text):
        contact_info = {}
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
        
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text)
        if linkedin:
            contact_info['linkedin'] = linkedin[0]
        
        return contact_info
    
    def extract_skills(self, text):
        if not text:
            return []
        
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'aws', 'docker', 'kubernetes',
            'machine learning', 'data science', 'html', 'css', 'git', 'linux', 'mongodb',
            'typescript', 'angular', 'vue', 'flask', 'django', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'matplotlib', 'scikit-learn', 'postman', 'api',
            'rest', 'graphql', 'microservices', 'jenkins', 'ci/cd', 'devops',
            'azure', 'gcp', 'terraform', 'ansible', 'elasticsearch', 'redis',
            'postgresql', 'mysql', 'oracle', 'firebase', 'supabase',
            'next.js', 'express', 'spring boot', 'hibernate', 'jpa', 'maven',
            'gradle', 'webpack', 'vite', 'sass', 'bootstrap', 'tailwind',
            'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin',
            'r', 'matlab', 'tableau', 'power bi', 'excel', 'vba', 'sap',
            'salesforce', 'jira', 'confluence', 'slack', 'teams', 'zoom',
            'agile', 'scrum', 'kanban', 'waterfall', 'lean', 'six sigma'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def calculate_resume_score(self, skills, text, contact_info):
        score = 0
        score += min(len(skills) * 3, 45)
        
        contact_score = 0
        if contact_info.get('email'):
            contact_score += 10
        if contact_info.get('phone'):
            contact_score += 10
        if contact_info.get('linkedin'):
            contact_score += 10
        score += contact_score
        
        word_count = len(text.split())
        if word_count > 200:
            score += 15
        elif word_count > 100:
            score += 10
        elif word_count > 50:
            score += 5
        
        return min(100, score)
    
    def process_resume(self, uploaded_file):
        if uploaded_file is None:
            return None
        
        file_bytes = uploaded_file.read()
        
        if uploaded_file.name.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_bytes)
        elif uploaded_file.name.endswith('.docx'):
            text = self.extract_text_from_docx(file_bytes)
        else:
            st.error("Unsupported file format. Please upload PDF or DOCX.")
            return None
        
        if not text:
            st.error("Could not extract text from file")
            return None
        
        contact_info = self.extract_contact_info(text)
        skills = self.extract_skills(text)
        score = self.calculate_resume_score(skills, text, contact_info)
        
        return {
            'filename': uploaded_file.name,
            'upload_time': datetime.now().isoformat(),
            'text_preview': text[:500] + "..." if len(text) > 500 else text,
            'skills': skills,
            'contact_info': contact_info,
            'score': score,
            'word_count': len(text.split()),
            'processing_time': datetime.now().isoformat()
        }

# Enhanced Skill Analysis Module
class SkillAnalyzer:
    def __init__(self):
        self.skill_database = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express'],
            'data_science': ['machine learning', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'databases': ['sql', 'postgresql', 'mysql', 'mongodb', 'redis'],
            'devops': ['git', 'jenkins', 'ci/cd', 'terraform', 'ansible']
        }
        
        self.learning_resources = {
            'python': ['Python.org Tutorial', 'Coursera Python Courses', 'Udemy Python Bootcamp'],
            'react': ['React Documentation', 'React Tutorial on YouTube', 'Frontend Masters'],
            'aws': ['AWS Training', 'Cloud Practitioner Certification', 'Udemy AWS Courses'],
            'machine learning': ['Andrew Ng ML Course', 'Fast.ai', 'Kaggle Learn']
        }
    
    def analyze_skills(self, resume_skills):
        analysis = {
            'current_skills': resume_skills,
            'skill_gaps': [],
            'skill_strengths': {},
            'learning_recommendations': [],
            'career_paths': [],
            'skill_levels': {},
            'improvement_priority': []
        }
        
        # Analyze skill categories
        for category, skills in self.skill_database.items():
            user_skills_in_category = [skill for skill in resume_skills if skill.lower() in skills]
            missing_skills = [skill for skill in skills if skill not in [s.lower() for s in resume_skills]]
            
            if user_skills_in_category:
                analysis['skill_strengths'][category] = user_skills_in_category
                analysis['skill_levels'][category] = len(user_skills_in_category) / len(skills) * 100
            
            if missing_skills:
                analysis['skill_gaps'].extend(missing_skills)
        
        # Generate learning recommendations
        for skill in resume_skills:
            if skill.lower() in self.learning_resources:
                analysis['learning_recommendations'].extend(self.learning_resources[skill.lower()])
        
        # Career path suggestions
        if any(skill in ['python', 'java', 'javascript'] for skill in resume_skills):
            analysis['career_paths'].append('Software Developer')
        if any(skill in ['machine learning', 'data science', 'pandas', 'numpy'] for skill in resume_skills):
            analysis['career_paths'].append('Data Scientist')
        if any(skill in ['aws', 'azure', 'docker', 'kubernetes'] for skill in resume_skills):
            analysis['career_paths'].append('Cloud Engineer')
        if any(skill in ['react', 'angular', 'vue', 'html', 'css'] for skill in resume_skills):
            analysis['career_paths'].append('Frontend Developer')
        
        return analysis

# Real-time Mock Interview Module
class MockInterviewSimulator:
    def __init__(self):
        self.technical_questions = [
            {
                'question': 'What is difference between REST and GraphQL?',
                'type': 'technical',
                'category': 'API Design',
                'difficulty': 'medium',
                'sample_answer': 'REST is an architectural style that uses HTTP methods and status codes, while GraphQL is a query language that allows clients to request exactly what data they need.',
                'time_limit': 120  # seconds
            },
            {
                'question': 'Explain concept of microservices architecture.',
                'type': 'technical',
                'category': 'System Design',
                'difficulty': 'medium',
                'sample_answer': 'Microservices is an architectural style where an application is built as a collection of small, independent services that communicate over well-defined APIs.',
                'time_limit': 150
            },
            {
                'question': 'How would you optimize database performance?',
                'type': 'technical',
                'category': 'Database',
                'difficulty': 'hard',
                'sample_answer': 'I would use indexing, query optimization, proper database design, caching strategies, and consider database sharding for large datasets.',
                'time_limit': 180
            },
            {
                'question': 'What is the difference between synchronous and asynchronous programming?',
                'type': 'technical',
                'category': 'Programming',
                'difficulty': 'medium',
                'sample_answer': 'Synchronous programming executes tasks sequentially, while asynchronous programming allows tasks to run concurrently without blocking the main thread.',
                'time_limit': 120
            }
        ]
        
        self.behavioral_questions = [
            {
                'question': 'Tell me about a time when you faced a difficult technical challenge.',
                'type': 'behavioral',
                'category': 'Problem Solving',
                'difficulty': 'medium',
                'sample_answer': 'I once faced a performance issue in a production application. I systematically analyzed the bottleneck, identified the root cause, and implemented a caching solution that improved response time by 60%.',
                'time_limit': 180
            },
            {
                'question': 'How do you stay updated with the latest technology trends?',
                'type': 'behavioral',
                'category': 'Learning',
                'difficulty': 'easy',
                'sample_answer': 'I regularly read tech blogs, follow industry leaders on social media, participate in online courses, and contribute to open-source projects.',
                'time_limit': 120
            },
            {
                'question': 'Describe a situation where you had to work with a difficult team member.',
                'type': 'behavioral',
                'category': 'Teamwork',
                'difficulty': 'medium',
                'sample_answer': 'I once worked with a team member who had different working styles. I initiated a conversation to understand their perspective, found common ground, and established clear communication protocols.',
                'time_limit': 150
            }
        ]
    
    def generate_interview(self, skills, num_questions=5):
        interview = {
            'session_id': f"interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'questions': [],
            'total_questions': num_questions,
            'skills_covered': skills,
            'start_time': datetime.now(),
            'total_time_limit': num_questions * 120  # 2 minutes per question
        }
        
        # Mix technical and behavioral questions
        all_questions = self.technical_questions + self.behavioral_questions
        selected_questions = random.sample(all_questions, min(num_questions, len(all_questions)))
        
        interview['questions'] = selected_questions
        return interview
    
    def evaluate_answer_realtime(self, question, user_answer, time_taken):
        evaluation = {
            'question': question['question'],
            'user_answer': user_answer,
            'time_taken': time_taken,
            'score': 0,
            'feedback': '',
            'improvement_suggestions': [],
            'time_bonus': 0,
            'content_score': 0
        }
        
        # Time-based scoring
        time_limit = question.get('time_limit', 120)
        if time_taken <= time_limit:
            evaluation['time_bonus'] = 2
        elif time_taken <= time_limit * 1.5:
            evaluation['time_bonus'] = 1
        else:
            evaluation['time_bonus'] = 0
        
        # Content-based scoring
        answer_length = len(user_answer.split())
        
        if answer_length < 10:
            evaluation['content_score'] = 2
            evaluation['feedback'] = 'Answer is too brief. Please provide more details.'
            evaluation['improvement_suggestions'].append('Elaborate on your answer with specific examples.')
        elif answer_length < 30:
            evaluation['content_score'] = 4
            evaluation['feedback'] = 'Good answer, but could be more detailed.'
            evaluation['improvement_suggestions'].append('Add specific examples and technical details.')
        else:
            evaluation['content_score'] = 6
            evaluation['feedback'] = 'Excellent detailed answer!'
        
        # Check for relevant keywords
        if question['type'] == 'technical':
            tech_keywords = ['architecture', 'performance', 'security', 'scalability', 'optimization', 'design', 'implementation']
            keyword_matches = sum(1 for keyword in tech_keywords if keyword in user_answer.lower())
            evaluation['content_score'] = min(8, evaluation['content_score'] + keyword_matches)
        
        # Calculate total score
        evaluation['score'] = evaluation['content_score'] + evaluation['time_bonus']
        
        return evaluation

# Real-time Aptitude Test Module
class AptitudeTestGenerator:
    def __init__(self):
        self.logical_reasoning = [
            {
                'question': 'If all roses are flowers and some flowers fade quickly, which statement must be true?',
                'options': ['All roses fade quickly', 'Some roses fade quickly', 'No roses fade quickly', 'Some flowers are roses'],
                'correct_answer': 1,
                'explanation': 'Since all roses are flowers and some flowers fade quickly, it follows that some roses fade quickly.',
                'time_limit': 60
            },
            {
                'question': 'What comes next in the sequence: 2, 6, 12, 20, 30, ?',
                'options': ['40', '42', '44', '46'],
                'correct_answer': 1,
                'explanation': 'The pattern adds consecutive even numbers: +4, +6, +8, +10, +12 = 42',
                'time_limit': 45
            },
            {
                'question': 'A man looks at a portrait and says, "Brothers and sisters I have none, but that man\'s father is my father\'s son." Who is in the portrait?',
                'options': ['His son', 'His father', 'His brother', 'Himself'],
                'correct_answer': 0,
                'explanation': 'If he has no brothers, then "my father\'s son" must be himself. So "that man\'s father" is himself, making the person in the portrait his son.',
                'time_limit': 90
            }
        ]
        
        self.quantitative = [
            {
                'question': 'If a project costs $5000 and is 25% complete, how much has been spent?',
                'options': ['$1250', '$1500', '$1750', '$2000'],
                'correct_answer': 0,
                'explanation': '25% of $5000 = $5000 × 0.25 = $1250',
                'time_limit': 30
            },
            {
                'question': 'A team of 8 people completes a task in 10 days. How long would 4 people take?',
                'options': ['15 days', '20 days', '25 days', '30 days'],
                'correct_answer': 1,
                'explanation': 'Half the team means double the time: 10 × 2 = 20 days',
                'time_limit': 45
            },
            {
                'question': 'If 3 machines can produce 300 widgets in 4 hours, how many widgets can 5 machines produce in 6 hours?',
                'options': ['750', '900', '1050', '1200'],
                'correct_answer': 0,
                'explanation': '3 machines × 4 hours = 12 machine-hours produce 300 widgets. So 1 machine-hour produces 25 widgets. 5 machines × 6 hours = 30 machine-hours × 25 = 750 widgets.',
                'time_limit': 60
            }
        ]
        
        self.verbal_reasoning = [
            {
                'question': 'Which word is the odd one out: Apple, Banana, Carrot, Orange?',
                'options': ['Apple', 'Banana', 'Carrot', 'Orange'],
                'correct_answer': 2,
                'explanation': 'Carrot is a vegetable, while the others are fruits.',
                'time_limit': 30
            },
            {
                'question': 'Complete the analogy: Doctor is to Hospital as Teacher is to ?',
                'options': ['Classroom', 'Student', 'Book', 'School'],
                'correct_answer': 3,
                'explanation': 'A doctor works in a hospital, similarly a teacher works in a school.',
                'time_limit': 30
            }
        ]
    
    def generate_aptitude_test(self, num_questions=10):
        test = {
            'test_id': f"aptitude_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'questions': [],
            'total_questions': num_questions,
            'start_time': datetime.now(),
            'total_time_limit': num_questions * 60  # 1 minute per question
        }
        
        all_questions = self.logical_reasoning + self.quantitative + self.verbal_reasoning
        selected_questions = random.sample(all_questions, min(num_questions, len(all_questions)))
        
        test['questions'] = selected_questions
        return test
    
    def evaluate_aptitude_answer_realtime(self, question, selected_option, time_taken):
        evaluation = {
            'question': question['question'],
            'selected_answer': selected_option,
            'correct_answer': question['correct_answer'],
            'is_correct': selected_option == question['correct_answer'],
            'explanation': question['explanation'],
            'time_taken': time_taken,
            'time_bonus': 0,
            'score': 0
        }
        
        # Time-based scoring
        time_limit = question.get('time_limit', 60)
        if time_taken <= time_limit:
            evaluation['time_bonus'] = 2
        elif time_taken <= time_limit * 1.5:
            evaluation['time_bonus'] = 1
        else:
            evaluation['time_bonus'] = 0
        
        # Calculate score
        if evaluation['is_correct']:
            evaluation['score'] = 8 + evaluation['time_bonus']
        else:
            evaluation['score'] = evaluation['time_bonus']
        
        return evaluation

# Enhanced Job Recommendation Module with Application System
class JobRecommendationEngine:
    def __init__(self):
        self.job_database = [
            {
                'id': 1,
                'title': 'Senior Python Developer',
                'company': 'TechCorp',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $180,000',
                'required_skills': ['python', 'django', 'postgresql', 'aws'],
                'description': 'We are looking for an experienced Python developer to join our growing team.',
                'match_score': 0,
                'application_deadline': '2024-03-15',
                'employment_type': 'Full-time',
                'experience_level': 'Senior'
            },
            {
                'id': 2,
                'title': 'Frontend Developer',
                'company': 'WebSolutions',
                'location': 'New York, NY',
                'salary': '$80,000 - $120,000',
                'required_skills': ['react', 'javascript', 'html', 'css'],
                'description': 'Join our frontend team to build amazing user experiences.',
                'match_score': 0,
                'application_deadline': '2024-03-20',
                'employment_type': 'Full-time',
                'experience_level': 'Mid-level'
            },
            {
                'id': 3,
                'title': 'Data Scientist',
                'company': 'DataTech',
                'location': 'Boston, MA',
                'salary': '$100,000 - $150,000',
                'required_skills': ['python', 'machine learning', 'pandas', 'numpy'],
                'description': 'Looking for a data scientist to help us derive insights from complex datasets.',
                'match_score': 0,
                'application_deadline': '2024-03-18',
                'employment_type': 'Full-time',
                'experience_level': 'Mid-level'
            },
            {
                'id': 4,
                'title': 'DevOps Engineer',
                'company': 'CloudSystems',
                'location': 'Seattle, WA',
                'salary': '$110,000 - $160,000',
                'required_skills': ['aws', 'docker', 'kubernetes', 'terraform'],
                'description': 'Help us build and maintain our cloud infrastructure.',
                'match_score': 0,
                'application_deadline': '2024-03-25',
                'employment_type': 'Full-time',
                'experience_level': 'Senior'
            },
            {
                'id': 5,
                'title': 'Full Stack Developer',
                'company': 'StartupHub',
                'location': 'Austin, TX',
                'salary': '$90,000 - $140,000',
                'required_skills': ['javascript', 'nodejs', 'react', 'mongodb'],
                'description': 'Join our fast-paced startup as a full stack developer.',
                'match_score': 0,
                'application_deadline': '2024-03-22',
                'employment_type': 'Full-time',
                'experience_level': 'Mid-level'
            }
        ]
    
    def calculate_skill_match(self, user_skills, job_skills):
        user_skills_lower = [skill.lower() for skill in user_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        matches = len(set(user_skills_lower) & set(job_skills_lower))
        total_required = len(job_skills_lower)
        
        return matches / total_required if total_required > 0 else 0
    
    def recommend_jobs(self, resume_skills, top_k=5):
        recommendations = []
        
        for job in self.job_database:
            match_score = self.calculate_skill_match(resume_skills, job['required_skills'])
            job['match_score'] = match_score
            
            if match_score > 0.2:  # Only include jobs with at least 20% match
                recommendations.append(job)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:top_k]
    
    def apply_for_job(self, job_id, user_profile):
        application = {
            'job_id': job_id,
            'user_profile': user_profile,
            'application_date': datetime.now().isoformat(),
            'status': 'Applied',
            'application_id': f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        return application

# Progress tracking system
def show_progress_tracker():
    steps = [
        "📁 Resume Upload",
        "🔍 Skill Analysis", 
        "🎯 Mock Interview",
        "🧠 Aptitude Test",
        "💼 Job Recommendations",
        "📊 Performance Dashboard"
    ]
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3>🎯 Your Career Journey Progress</h3>', unsafe_allow_html=True)
    
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i < st.session_state.current_step:
                status_class = "completed"
                icon = "✅"
            elif i == st.session_state.current_step:
                status_class = "active"
                icon = "📍"
            else:
                status_class = ""
                icon = f"{i+1}"
            
            st.markdown(f'<div class="progress-step {status_class}">{icon}<br><small>{step}</small></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Real-time timer component
def show_timer():
    if st.session_state.timer_running:
        # Update timer
        elapsed = time.time() - st.session_state.timer_start_time
        remaining = max(0, st.session_state.timer_seconds - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        st.markdown(f'<div class="timer">⏱️ Time Remaining: {minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)
        
        if remaining == 0:
            st.session_state.timer_running = False
            st.warning("⏰ Time's up!")
            return False
    return True

# Main application
def main():
    init_session_state()
    
    # Initialize processors
    resume_processor = ResumeProcessor()
    skill_analyzer = SkillAnalyzer()
    interview_simulator = MockInterviewSimulator()
    aptitude_generator = AptitudeTestGenerator()
    job_engine = JobRecommendationEngine()
    
    # Header with live indicator
    st.markdown("""
    <div class="main-header">
        <h1>📊 AI Resume Analyzer - Global Platform</h1>
        <p>Upload your resume for comprehensive analysis, interview preparation, and job applications</p>
        <span class="live-indicator">🔴 LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Show progress tracker
    show_progress_tracker()
    
    # Step-based navigation
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3>🧭 Navigation Controls</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Previous Step", disabled=st.session_state.current_step == 1):
            st.session_state.current_step = max(1, st.session_state.current_step - 1)
            st.rerun()
    
    with col2:
        st.markdown(f'<div style="text-align: center; padding: 1rem;"><strong>Step {st.session_state.current_step} of {st.session_state.total_steps}</strong></div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("Next Step ➡️", disabled=st.session_state.current_step == st.session_state.total_steps):
            st.session_state.current_step = min(st.session_state.total_steps, st.session_state.current_step + 1)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dynamic content based on current step
    if st.session_state.current_step == 1:
        show_step_1_upload(resume_processor)
    elif st.session_state.current_step == 2:
        show_step_2_skill_analysis(skill_analyzer)
    elif st.session_state.current_step == 3:
        show_step_3_interview(interview_simulator)
    elif st.session_state.current_step == 4:
        show_step_4_aptitude(aptitude_generator)
    elif st.session_state.current_step == 5:
        show_step_5_jobs(job_engine)
    elif st.session_state.current_step == 6:
        show_step_6_performance()

def show_step_1_upload(processor):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>📁 Step 1: Upload Your Resume</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose Resume File",
        type=['pdf', 'docx'],
        key="resume_upload",
        help="Supported formats: PDF, DOCX (Max 10MB)"
    )
    
    if uploaded_file and st.button("🚀 Process Resume", type="primary"):
        with st.spinner("🔄 Processing your resume..."):
            progress_bar = st.progress(0)
            
            for i in range(4):
                progress = (i + 1) / 4
                progress_bar.progress(progress)
                time.sleep(0.5)
            
            results = processor.process_resume(uploaded_file)
            
            if results:
                st.session_state.resume_data = results
                st.success("✅ Resume processed successfully!")
                st.balloons()
                time.sleep(2)
                st.session_state.current_step = 2
                st.rerun()
    
    if st.session_state.resume_data:
        results = st.session_state.resume_data
        
        st.markdown('<h3>📊 Analysis Results</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2.5rem;">{results["score"]}</div><div>Resume Score</div></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2.5rem;">{len(results["skills"])}</div><div>Skills Found</div></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2.5rem;">{results["word_count"]}</div><div>Word Count</div></div>', unsafe_allow_html=True)
        
        # Skills section
        st.markdown('<h3>🔍 Extracted Skills</h3>', unsafe_allow_html=True)
        skills = results['skills']
        skill_html = ' '.join([f'<span class="skill-tag">{skill}</span>' for skill in skills[:20]])
        st.markdown(skill_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_step_2_skill_analysis(analyzer):
    if not st.session_state.resume_data:
        st.warning("Please upload resume first")
        st.session_state.current_step = 1
        st.rerun()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>🔍 Step 2: Skill Analysis</h2>', unsafe_allow_html=True)
    
    if st.button("🚀 Analyze Skills", type="primary"):
        with st.spinner("🔍 Analyzing your skills..."):
            analysis = analyzer.analyze_skills(st.session_state.resume_data['skills'])
            st.session_state.skill_analysis = analysis
            st.success("✅ Skill analysis completed!")
            time.sleep(2)
            st.session_state.current_step = 3
            st.rerun()
    
    if st.session_state.skill_analysis:
        analysis = st.session_state.skill_analysis
        
        # Skill strengths
        st.markdown('<h3>💪 Skill Strengths</h3>', unsafe_allow_html=True)
        for category, skills in analysis['skill_strengths'].items():
            st.markdown(f'<h4>{category.title()} - {analysis["skill_levels"][category]:.0f}%</h4>', unsafe_allow_html=True)
            skill_html = ' '.join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
            st.markdown(skill_html, unsafe_allow_html=True)
        
        # Career paths
        if analysis['career_paths']:
            st.markdown('<h3>🎯 Recommended Career Paths</h3>', unsafe_allow_html=True)
            for path in analysis['career_paths']:
                st.markdown(f'<div class="success">{path}</div>', unsafe_allow_html=True)
        
        # Learning recommendations
        if analysis['learning_recommendations']:
            st.markdown('<h3>📚 Learning Recommendations</h3>', unsafe_allow_html=True)
            for rec in analysis['learning_recommendations'][:5]:
                st.markdown(f'<div class="warning">{rec}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_step_3_interview(simulator):
    if not st.session_state.resume_data:
        st.warning("Please upload resume first")
        st.session_state.current_step = 1
        st.rerun()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>🎯 Step 3: Mock Interview</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_questions = st.number_input("Number of Questions", min_value=3, max_value=10, value=5)
    
    with col2:
        st.markdown(f'<div class="metric-card"><h4>Interview Settings</h4><p>Questions: {num_questions}</p><p>Duration: {num_questions * 2} minutes</p></div>', unsafe_allow_html=True)
    
    if st.button("🚀 Start Interview", type="primary"):
        interview = simulator.generate_interview(st.session_state.resume_data['skills'], num_questions)
        st.session_state.interview_session = interview
        st.session_state.interview_answers = []
        st.session_state.timer_running = True
        st.session_state.timer_start_time = time.time()
        st.session_state.timer_seconds = interview['total_time_limit']
        st.rerun()
    
    if st.session_state.interview_session:
        session = st.session_state.interview_session
        current_question = len(st.session_state.interview_answers)
        
        if current_question < len(session['questions']):
            question = session['questions'][current_question]
            
            # Show timer
            if not show_timer():
                # Time's up - move to next question
                evaluation = {
                    'question': question['question'],
                    'user_answer': '',
                    'time_taken': question.get('time_limit', 120),
                    'score': 0,
                    'feedback': 'Time expired!',
                    'improvement_suggestions': ['Practice answering within time limits']
                }
                st.session_state.interview_answers.append(evaluation)
                if current_question + 1 < len(session['questions']):
                    st.session_state.timer_start_time = time.time()
                    st.session_state.timer_seconds = session['questions'][current_question + 1].get('time_limit', 120)
                st.rerun()
            
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<h3>Question {current_question + 1} of {len(session["questions"])}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>{question["question"]}</strong></p>', unsafe_allow_html=True)
            st.markdown(f'<p><em>Type: {question["type"].title()} | Category: {question["category"]}</em></p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            answer = st.text_area("Your Answer:", height=150, key=f"answer_{current_question}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Answer", type="primary"):
                    if answer:
                        time_taken = time.time() - st.session_state.timer_start_time
                        evaluation = simulator.evaluate_answer_realtime(question, answer, time_taken)
                        st.session_state.interview_answers.append(evaluation)
                        
                        if current_question + 1 < len(session['questions']):
                            st.session_state.timer_start_time = time.time()
                            st.session_state.timer_seconds = session['questions'][current_question + 1].get('time_limit', 120)
                        else:
                            st.session_state.timer_running = False
                        
                        st.rerun()
            with col2:
                if st.button("Skip Question"):
                    evaluation = {
                        'question': question['question'],
                        'user_answer': '',
                        'time_taken': time.time() - st.session_state.timer_start_time,
                        'score': 0,
                        'feedback': 'Question skipped',
                        'improvement_suggestions': ['Try to answer all questions']
                    }
                    st.session_state.interview_answers.append(evaluation)
                    
                    if current_question + 1 < len(session['questions']):
                        st.session_state.timer_start_time = time.time()
                        st.session_state.timer_seconds = session['questions'][current_question + 1].get('time_limit', 120)
                    else:
                        st.session_state.timer_running = False
                    
                    st.rerun()
        else:
            st.session_state.timer_running = False
            st.success("🎉 Interview completed!")
            
            # Show results
            total_score = sum(answer['score'] for answer in st.session_state.interview_answers)
            average_score = total_score / len(st.session_state.interview_answers)
            
            st.markdown(f'<div class="metric-card"><h3>Interview Results</h3><div style="font-size: 2.5rem;">{average_score:.1f}/10</div><div>Average Score</div></div>', unsafe_allow_html=True)
            
            for i, answer in enumerate(st.session_state.interview_answers):
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                st.markdown(f'<h4>Question {i+1}</h4>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>{answer["question"]}</strong></p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Your Answer:</strong> {answer["user_answer"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Score:</strong> {answer["score"]}/10</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Time Taken:</strong> {answer["time_taken"]:.1f}s</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Feedback:</strong> {answer["feedback"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔄 Start New Interview"):
                st.session_state.interview_session = None
                st.session_state.interview_answers = []
                st.rerun()
            
            if st.button("➡️ Continue to Aptitude Test"):
                st.session_state.current_step = 4
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_step_4_aptitude(generator):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>🧠 Step 4: Aptitude Test</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_questions = st.number_input("Number of Questions", min_value=5, max_value=15, value=10)
    
    with col2:
        st.markdown(f'<div class="metric-card"><h4>Test Settings</h4><p>Questions: {num_questions}</p><p>Duration: {num_questions} minutes</p></div>', unsafe_allow_html=True)
    
    if st.button("🚀 Start Aptitude Test", type="primary"):
        test = generator.generate_aptitude_test(num_questions)
        st.session_state.aptitude_session = test
        st.session_state.aptitude_answers = []
        st.session_state.timer_running = True
        st.session_state.timer_start_time = time.time()
        st.session_state.timer_seconds = test['total_time_limit']
        st.rerun()
    
    if st.session_state.aptitude_session:
        session = st.session_state.aptitude_session
        current_question = len(st.session_state.aptitude_answers)
        
        if current_question < len(session['questions']):
            question = session['questions'][current_question]
            
            # Show timer
            if not show_timer():
                # Time's up - move to next question
                evaluation = {
                    'question': question['question'],
                    'selected_answer': 'Not answered',
                    'correct_answer': question['correct_answer'],
                    'is_correct': False,
                    'explanation': question['explanation'],
                    'time_taken': question.get('time_limit', 60),
                    'score': 0
                }
                st.session_state.aptitude_answers.append(evaluation)
                if current_question + 1 < len(session['questions']):
                    st.session_state.timer_start_time = time.time()
                    st.session_state.timer_seconds = session['questions'][current_question + 1].get('time_limit', 60)
                st.rerun()
            
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<h3>Question {current_question + 1} of {len(session["questions"])}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>{question["question"]}</strong></p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            selected_option = st.radio("Select your answer:", question['options'], key=f"aptitude_{current_question}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Answer", type="primary"):
                    time_taken = time.time() - st.session_state.timer_start_time
                    evaluation = generator.evaluate_aptitude_answer_realtime(question, question['options'].index(selected_option), time_taken)
                    st.session_state.aptitude_answers.append(evaluation)
                    
                    if current_question + 1 < len(session['questions']):
                        st.session_state.timer_start_time = time.time()
                        st.session_state.timer_seconds = session['questions'][current_question + 1].get('time_limit', 60)
                    else:
                        st.session_state.timer_running = False
                    
                    st.rerun()
            with col2:
                if st.button("Skip Question"):
                    evaluation = {
                        'question': question['question'],
                        'selected_answer': 'Not answered',
                        'correct_answer': question['correct_answer'],
                        'is_correct': False,
                        'explanation': question['explanation'],
                        'time_taken': time.time() - st.session_state.timer_start_time,
                        'score': 0
                    }
                    st.session_state.aptitude_answers.append(evaluation)
                    
                    if current_question + 1 < len(session['questions']):
                        st.session_state.timer_start_time = time.time()
                        st.session_state.timer_seconds = session['questions'][current_question + 1].get('time_limit', 60)
                    else:
                        st.session_state.timer_running = False
                    
                    st.rerun()
        else:
            st.session_state.timer_running = False
            st.success("🎉 Aptitude test completed!")
            
            # Show results
            correct_answers = sum(1 for answer in st.session_state.aptitude_answers if answer['is_correct'])
            total_questions = len(st.session_state.aptitude_answers)
            percentage = (correct_answers / total_questions) * 100
            
            st.markdown(f'<div class="metric-card"><h3>Test Results</h3><div style="font-size: 2.5rem;">{percentage:.1f}%</div><div>Accuracy</div></div>', unsafe_allow_html=True)
            
            for i, answer in enumerate(st.session_state.aptitude_answers):
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                st.markdown(f'<h4>Question {i+1}</h4>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>{answer["question"]}</strong></p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Your Answer:</strong> {answer["selected_answer"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Correct:</strong> {"✅" if answer["is_correct"] else "❌"}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Time Taken:</strong> {answer["time_taken"]:.1f}s</p>', unsafe_allow_html=True)
                st.markdown(f'<p><strong>Explanation:</strong> {answer["explanation"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔄 Start New Test"):
                st.session_state.aptitude_session = None
                st.session_state.aptitude_answers = []
                st.rerun()
            
            if st.button("➡️ Continue to Job Recommendations"):
                st.session_state.current_step = 5
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_step_5_jobs(engine):
    if not st.session_state.resume_data:
        st.warning("Please upload resume first")
        st.session_state.current_step = 1
        st.rerun()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>💼 Step 5: Job Recommendations & Applications</h2>', unsafe_allow_html=True)
    
    if st.button("🚀 Get Job Recommendations", type="primary"):
        with st.spinner("🔍 Analyzing job matches..."):
            recommendations = engine.recommend_jobs(st.session_state.resume_data['skills'])
            st.session_state.job_recommendations = recommendations
            st.success("✅ Job recommendations generated!")
            time.sleep(2)
    
    if st.session_state.job_recommendations:
        recommendations = st.session_state.job_recommendations
        
        for job in recommendations:
            st.markdown('<div class="job-card">', unsafe_allow_html=True)
            st.markdown(f'<h3>{job["title"]} at {job["company"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>Location:</strong> {job["location"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>Salary:</strong> {job["salary"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>Match Score:</strong> {job["match_score"]:.1%}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>Required Skills:</strong> {", ".join(job["required_skills"])}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><strong>Deadline:</strong> {job["application_deadline"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p>{job["description"]}</p>', unsafe_allow_html=True)
            
            # Check if already applied
            already_applied = job['id'] in [app['job_id'] for app in st.session_state.applied_jobs]
            
            if not already_applied:
                if st.button(f"📝 Apply for {job['title']}", key=f"apply_{job['id']}", type="primary"):
                    application = engine.apply_for_job(job['id'], st.session_state.resume_data)
                    st.session_state.applied_jobs.append(application)
                    st.success(f"✅ Applied for {job['title']} at {job['company']}!")
                    st.balloons()
            else:
                st.markdown('<div class="success">✅ Already Applied</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show applied jobs
        if st.session_state.applied_jobs:
            st.markdown('<h3>📋 Your Applications</h3>', unsafe_allow_html=True)
            for app in st.session_state.applied_jobs:
                job = next((j for j in recommendations if j['id'] == app['job_id']), None)
                if job:
                    st.markdown(f'<div class="success">📝 {job["title"]} at {job["company"]} - {app["status"]}</div>', unsafe_allow_html=True)
        
        if st.button("➡️ Continue to Performance Dashboard"):
            st.session_state.current_step = 6
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_step_6_performance():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>📊 Step 6: Performance Dashboard</h2>', unsafe_allow_html=True)
    
    # Overall performance summary
    st.markdown('<h3>🎯 Overall Performance Summary</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.resume_data:
            resume_score = st.session_state.resume_data['score']
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{resume_score}</div><div>Resume Score</div></div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.interview_answers:
            scores = [answer['score'] for answer in st.session_state.interview_answers]
            avg_score = sum(scores) / len(scores)
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{avg_score:.1f}</div><div>Interview Score</div></div>', unsafe_allow_html=True)
    
    with col3:
        if st.session_state.aptitude_answers:
            correct = sum(1 for answer in st.session_state.aptitude_answers if answer['is_correct'])
            total = len(st.session_state.aptitude_answers)
            percentage = (correct / total) * 100
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{percentage:.0f}%</div><div>Aptitude Score</div></div>', unsafe_allow_html=True)
    
    with col4:
        applied_count = len(st.session_state.applied_jobs)
        st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{applied_count}</div><div>Jobs Applied</div></div>', unsafe_allow_html=True)
    
    # Detailed performance sections
    if st.session_state.interview_answers:
        st.markdown('<h3>🎯 Interview Performance Details</h3>', unsafe_allow_html=True)
        
        scores = [answer['score'] for answer in st.session_state.interview_answers]
        avg_score = sum(scores) / len(scores)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{avg_score:.1f}</div><div>Average Score</div></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{max(scores)}</div><div>Best Score</div></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{len(scores)}</div><div>Questions</div></div>', unsafe_allow_html=True)
    
    if st.session_state.aptitude_answers:
        st.markdown('<h3>🧠 Aptitude Performance Details</h3>', unsafe_allow_html=True)
        
        correct_answers = sum(1 for answer in st.session_state.aptitude_answers if answer['is_correct'])
        total_questions = len(st.session_state.aptitude_answers)
        percentage = (correct_answers / total_questions) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{percentage:.1f}%</div><div>Accuracy</div></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{correct_answers}</div><div>Correct</div></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="metric-card"><div style="font-size: 2rem;">{total_questions}</div><div>Total</div></div>', unsafe_allow_html=True)
    
    # Recommendations for improvement
    st.markdown('<h3>💡 Recommendations for Improvement</h3>', unsafe_allow_html=True)
    
    recommendations = []
    
    if st.session_state.resume_data and st.session_state.resume_data['score'] < 80:
        recommendations.append("📄 Improve your resume score by adding more skills and contact information")
    
    if st.session_state.interview_answers:
        avg_score = sum(answer['score'] for answer in st.session_state.interview_answers) / len(st.session_state.interview_answers)
        if avg_score < 7:
            recommendations.append("🎯 Practice answering interview questions with more detail and examples")
    
    if st.session_state.aptitude_answers:
        correct = sum(1 for answer in st.session_state.aptitude_answers if answer['is_correct'])
        total = len(st.session_state.aptitude_answers)
        percentage = (correct / total) * 100
        if percentage < 70:
            recommendations.append("🧠 Practice more aptitude questions to improve your logical reasoning")
    
    if len(st.session_state.applied_jobs) < 3:
        recommendations.append("💼 Apply for more jobs to increase your chances of getting hired")
    
    for rec in recommendations:
        st.markdown(f'<div class="warning">{rec}</div>', unsafe_allow_html=True)
    
    # Completion message
    st.markdown('<h3>🎉 Congratulations!</h3>', unsafe_allow_html=True)
    st.markdown('<div class="success">You have completed the entire AI Resume Analyzer journey! You have uploaded your resume, analyzed your skills, completed a mock interview, taken an aptitude test, and applied for jobs. Use the performance insights to improve your job search strategy.</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Start Over"):
        # Reset session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
