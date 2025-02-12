import pickle
from models import SessionLocal, Course

db = SessionLocal()

path = "./courses_minimal.pkl"


def load_courses():
    # Load courses from pickle file
    with open(path, "rb") as f:
        courses = pickle.load(f)

    try:
        # Convert each course dict to Course model and add to session
        for course_data in courses:
            course = Course(
                slug=course_data["course_slug"],
                name=course_data["course_name"],
                description=course_data.get("course_description"),
                school_name=course_data["school_name"],
                tags=course_data["tags"],
                instructor_names=course_data.get("instructor_names"),
                instructor_caption=course_data.get("instructor_caption"),
                overview_raw=course_data.get("overview_raw"),
                personas_raw=course_data.get("personas_raw"),
                topics_raw=course_data.get("topics_raw"),
            )
            db.add(course)

        # Commit all changes
        db.commit()
        print(f"Successfully loaded {len(courses)} courses")

    except Exception as e:
        print(f"Error loading courses: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_courses()
