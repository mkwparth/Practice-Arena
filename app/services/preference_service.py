from sqlalchemy.orm import Session
from app.models.userPreference import UserPreference
from app.models.category import Category


def get_all_categories(db: Session):
    return db.query(Category).filter(Category.is_active == True).all()


def save_user_preferences(db: Session, user_id: int, category_ids: list):

    # remove old preferences
    db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).delete()

    for cat_id in category_ids:
        pref = UserPreference(
            user_id=user_id,
            category_id=cat_id
        )
        db.add(pref)

    db.commit()

    return True


def get_user_preferences(db: Session, user_id: int):
    prefs = (
        db.query(Category)
        .join(UserPreference, UserPreference.category_id == Category.id)
        .filter(UserPreference.user_id == user_id)
        .all()
    )

    return prefs