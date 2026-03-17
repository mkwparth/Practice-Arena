from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import exists


from app.models.problem import Problem
from app.models.problem_category import ProblemCategory
from app.models.userPreference import UserPreference
from app.models.user_attempt import UserAttempt


def get_personalized_feed(db: Session, user_id: int, difficulty: str = None, limit: int = 10):

    # 1. user preferences
    category_ids = [
        c[0] for c in db.query(UserPreference.category_id)
        .filter(UserPreference.user_id == user_id)
        .all()
    ]

    print("category_ids :" ,category_ids)

    if not category_ids:
        return []

    # 2. base query
    query = db.query(Problem).join(
        ProblemCategory,
        Problem.id == ProblemCategory.problem_id
    ).filter(
        ProblemCategory.category_id.in_(category_ids),
        Problem.is_active == True,
        ~db.query(UserAttempt).filter(
            UserAttempt.problem_id == Problem.id,
            UserAttempt.user_id == user_id,
            UserAttempt.status == "solved"
        ).exists()
    )

    print("query :", query)

    # 3. difficulty
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)

    # 4. remove duplicates properly
    query = query.group_by(Problem.id)

    # 5. random
    problems = query.order_by(func.random()).limit(limit).all()
    print("problems :", problems)

    # 6. mark as served
    for problem in problems:
        existing = db.query(UserAttempt).filter(
            UserAttempt.user_id == user_id,
            UserAttempt.problem_id == problem.id
        ).first()

        print("existing :", existing)

        if not existing:
            db.add(UserAttempt(
                user_id=user_id,
                problem_id=problem.id,
                status="served"
            ))

    db.commit()

    return problems