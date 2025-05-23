# main.py 
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

def get_vector(text):
    """Convert text to vector using spaCy."""
    return nlp(text).vector

def normalize_text(text):
    """Normalize text by lowercasing."""
    return [token.lower() for token in text]

def calculate_similarity(user_skills, job_requirements):
    """Calculate similarity percentage between user skills and job requirements."""
    user_vector = get_vector(" ".join(normalize_text(user_skills)))
    job_vector = get_vector(" ".join(normalize_text(job_requirements)))

    if np.any(user_vector) and np.any(job_vector):  # Check if vectors are non-empty
        similarity = cosine_similarity([user_vector], [job_vector])
        return similarity[0][0] * 100  # Convert to percentage
    return 0.0

def recommend_jobs(user, jobs):
    recommendations = []

    for job in jobs:
        similarity_score = calculate_similarity(user['skills'], job['requirements'])

        # Check experience and location
        experience_match = user['experience'] >= job['experience_required']
        location_match = user['location'] == job['location']

        # Adjust similarity score based on experience and location
        if experience_match:
            similarity_score += 10  # Boost score if experience meets requirements
        if location_match:
            similarity_score += 5  # Boost score if location matches

        recommendations.append({
            'job': job,
            'similarity_score': similarity_score
        })

    recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    return recommendations

def rank_job_seekers(job, users):
    rankings = []

    for user in users:
        similarity_score = calculate_similarity(user['skills'], job['requirements'])

        # Check experience and location
        experience_match = user['experience'] >= job['experience_required']
        location_match = user['location'] == job['location']

        # Adjust similarity score based on experience and location
        if experience_match:
            similarity_score += 10  # Boost score if experience meets requirements
        if location_match:
            similarity_score += 5  # Boost score if location matches

        rankings.append({
            'user': user,
            'similarity_score': similarity_score
        })

    rankings.sort(key=lambda x: x['similarity_score'], reverse=True)
    return rankings

if __name__ == "__main__":
    jobs = [
        {
            'title': 'Software Engineer',
            'description': 'Develop software solutions.',
            'requirements': ['Python', 'Django', 'SQL'],
            'experience_required': 3,  # in years
            'location': 'New York'
        },
        {
            'title': 'Data Scientist',
            'description': 'Analyze data and build models.',
            'requirements': ['Python', 'Machine Learning', 'Pandas'],
            'experience_required': 2,
            'location': 'San Francisco'
        }
    ]

    user = {
        'skills': ['Python', 'SQL', 'Machine Learning'],
        'experience': 4,  # years of experience
        'location': 'New York'
    }

    # Get job recommendations
    # recommendations = recommend_jobs(user, jobs)

    # for rec in recommendations:
    #     print(f"Job Title: {rec['job']['title']}, Similarity Score: {rec['similarity_score']:.2f}%, Description: {rec['job']['description']}")

    specific_job = {
        'title': 'Data Scientist',
        'description': 'Analyze data and build models.',
        'requirements': ['Python', 'Machine Learning', 'Pandas', 'SQL'],
        'experience_required': 2,
        'location': 'San Francisco'
    }

    users = [
        {'skills': ['Python', 'SQL', 'Machine Learning'], 'experience': 1, 'location': 'New York'},
        {'skills': ['Java', 'Django', 'SQL'], 'experience': 1, 'location': 'New York'},
        {'skills': ['Python', 'Machine Learning', 'Pandas'], 'experience': 1, 'location': 'Addis'}
    ]

    # Rank job seekers for the specific job
    rankings = rank_job_seekers(specific_job, users)

    for rank in rankings:
        print(f"User Skills: {rank['user']['skills']}, Similarity Score: {rank['similarity_score']:.2f}%")