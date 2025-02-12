from models import Course, SessionLocal
from embedding import get_embedding
from sqlalchemy import select

DEFAULT_LIMIT = 7
db = SessionLocal()


def find_courses_by_query(query: str, limit: int = DEFAULT_LIMIT) -> list[Course]:
    embedding = get_embedding(query)
    return find_courses_by_vector(embedding, limit)


def find_similar_courses(course_id: int, limit: int = DEFAULT_LIMIT) -> list[Course]:
    source_course = db.get(Course, course_id)
    return find_courses_by_vector(
        source_course.embedding, limit, exclude_course_ids=[course_id]
    )


def find_courses_by_vector(
    vector: list[float], limit: int = DEFAULT_LIMIT, exclude_course_ids: list[int] = []
) -> list[Course]:

    results = db.scalars(
        select(Course)
        .where(Course.id.notin_(exclude_course_ids))
        .order_by(Course.embedding.cosine_distance(vector))
        .limit(limit)
    ).all()

    print_courses(results)

    return results


def print_courses(courses: list[Course]) -> None:
    for course in courses:
        print(f"({course.id}) {course.name}")


def course_to_string(course: Course) -> str:
    components = [
        "This course is called: " + course.name,
        "It is about: " + course.description,
        "Tags: " + ", ".join(course.tags),
        "Instructor: " + course.instructor_names,
        # "Instructor caption: " + course.instructor_caption,
        # "Overview: " + course.overview_raw,
        # "It is for: " + course.personas_raw,
        "It covers the following topics: " + course.topics_raw,
    ]
    return "\n".join(components)


def embed_all_courses() -> None:
    courses = db.query(Course).all()
    for i, course in enumerate(courses):
        course_string = course_to_string(course)
        course.embedding = get_embedding(course_string)
        db.add(course)

        if (i + 1) % 20 == 0:
            print(f"Processed {i + 1} courses")
            db.commit()

    db.commit()
