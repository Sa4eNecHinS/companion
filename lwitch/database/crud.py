from lwitch.database.db import SessionLocal
from lwitch.database.models import Dialogue


def create_dialogue(
    timestamp: str,
    user_id: str,
    user_input: str,
    sanitized_user_input: str | None,
    is_blocked: bool,
    block_reason: str | None,
    llm_response: str | None,
):

    db = SessionLocal()

    try:
        dialogue = Dialogue(
            timestamp=timestamp,
            user_id=user_id,
            user_input=user_input,
            sanitized_user_input=sanitized_user_input,
            is_blocked=is_blocked,
            block_reason=block_reason,
            llm_response=llm_response,
        )

        db.add(dialogue)
        db.commit()
        db.refresh(dialogue)

        return dialogue

    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")

        return None

    finally:
        db.close()


if __name__ == "__main__":
    create_dialogue(
        timestamp="10929",
        user_id="default_user",
        user_input="ooo",
        sanitized_user_input="ooo",
        is_blocked=False,
        block_reason=None,
        llm_response="aaa",
    )
