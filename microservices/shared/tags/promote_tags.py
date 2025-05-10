# backend/tags/promote_tags.py
from typing import List
from storage_service.memory.models import AlignmentTag
from datetime import datetime
from collections import Counter


def promote_session_tags(
    session_tags: List[AlignmentTag],
    existing_persistent_tags: List[AlignmentTag],
) -> List[AlignmentTag]:
    """
    Promote session tags to persistent memory based on priority and recurrence.
    - Priority ≥ 7 always promotes
    - Otherwise, must be seen in 2+ sessions
    """
    promoted_tags = existing_persistent_tags.copy()
    now = datetime.now()

    # Index persistent tag IDs for easy matching
    persistent_ids = {tag.tag_id for tag in existing_persistent_tags}

    session_counts = Counter([t.tag_id for t in session_tags])

    for tag in session_tags:
        if tag.tag_id in persistent_ids:
            continue  # already promoted

        if tag.priority_level >= 7:
            tag.memory_scope = "persistent"
            tag.first_triggered_at = tag.first_triggered_at or now
            tag.last_confirmed_at = now
            promoted_tags.append(tag)

        elif session_counts[tag.tag_id] >= 2:
            tag.memory_scope = "persistent"
            tag.first_triggered_at = tag.first_triggered_at or now
            tag.last_confirmed_at = now
            promoted_tags.append(tag)

    return promoted_tags
