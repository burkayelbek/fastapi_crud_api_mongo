def return_post(post) -> dict:
    return {
        "id": str(post["_id"]),
        "short_description": post["short_description"],
        "description": post["description"],
        "tags": post["tags"],
        "created_at": post["created_at"],
        "updated_at": post["updated_at"],
    }


def list_posts(posts) -> list:
    return [return_post(post) for post in posts]
