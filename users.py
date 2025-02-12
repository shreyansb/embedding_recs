from pydantic import BaseModel
from models import SessionLocal, Course
from embedding import get_embedding
from courses import find_courses_by_vector

db = SessionLocal()


class User(BaseModel):
    job_title: str
    courses_taken: list[int]
    courses_interested: list[int]


user_1 = User(
    job_title="Product manager",
    courses_taken=[1],
    courses_interested=[],
)

user_2 = User(
    job_title="Head of engineering",
    courses_taken=[],
    courses_interested=[55, 65, 33],
)


def user_to_string(user: User) -> str:
    user_string_components = ["This user is a " + user.job_title]

    for course_id in user.courses_taken:
        course = db.get(Course, course_id)
        user_string_components.append(
            f"This user has taken the course '{course.name}', about {course.description}."
        )

    for course_id in user.courses_interested:
        course = db.get(Course, course_id)
        user_string_components.append(
            f"This user is interested in the course '{course.name}', about {course.description}."
        )

    return "\n".join(user_string_components)


def get_user_recommendations(user: User) -> list[Course]:
    user_string = user_to_string(user)
    user_embedding = get_embedding(user_string)
    exclude_course_ids = [
        course_id for course_id in user.courses_taken + user.courses_interested
    ]
    return find_courses_by_vector(user_embedding, exclude_course_ids=exclude_course_ids)
