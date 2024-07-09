from repositories.post_repository import PostRepository
from src.models import Post, User
from sqlalchemy.orm import Session
from typing import List
from src.core.logging import setup_logging

logger = setup_logging()


class PostService:
	"""
	Service class for managing posts.
	"""

	def __init__(self, db: Session):
		"""
		Initializes a new instance of the PostService class.

		Args:
			db (Session): The database session object.
		"""
		self.post_repo = PostRepository(Post, db)

	# Cache dictionary to store posts
	self.post_cache = {}

	def create_post(self, title: str, content: str, author: User) -> Post:
		"""
		Creates a new post.

		Args:
			title (str): The title of the post.
			content (str): The content of the post.
			author (User): The author of the post.

		Returns:
			Post: The created post.
		"""
		logger.info(f"Creating new post: {title} by user {author.username}")
		new_post = Post(title=title, content=content, author_id=author.id)
		return self.post_repo.create(new_post)

	def get_post(self, post_id: int) -> Post:
		"""
		Retrieves a post by its ID.

		Args:
			post_id (int): The ID of the post.

		Returns:
			Post: The retrieved post.
		"""
		logger.info(f"Fetching post with id: {post_id}")
		if post_id in self.post_cache:
			return self.post_cache[post_id]
		post = self.post_repo.get(post_id)
		if post:
			self.post_cache[post_id] = post
		return post

	def update_post(self, post_id: int, title: str, content: str) -> Post:
		"""
		Updates a post.

		Args:
			post_id (int): The ID of the post.
			title (str): The new title of the post.
			content (str): The new content of the post.

		Returns:
			Post: The updated post.
		"""
		logger.info(f"Updating post with id: {post_id}")
		post = self.get_post(post_id)
		if post:
			post.title = title
			post.content = content
			return self.post_repo.update(post)
		return None

	def delete_post(self, post_id: int) -> bool:
		"""
		Deletes a post.

		Args:
			post_id (int): The ID of the post.

		Returns:
			bool: True if the post was deleted successfully, False otherwise.
		"""
		logger.info(f"Deleting post with id: {post_id}")
		return self.post_repo.delete(post_id)

	def get_user_posts(self, author_id: int) -> List[Post]:
		"""
		Retrieves posts by a specific user.

		Args:
			author_id (int): The ID of the user.

		Returns:
			List[Post]: The list of posts by the user.
		"""
		logger.info(f"Fetching posts for user with id: {author_id}")
		return self.post_repo.get_by_author(author_id)

	def get_recent_posts(self, limit: int = 10) -> List[Post]:
		"""
		Retrieves the most recent posts.

		Args:
			limit (int, optional): The maximum number of posts to retrieve. Defaults to 10.

		Returns:
			List[Post]: The list of recent posts.
		"""
		logger.info(f"Fetching {limit} recent posts")
		return self.post_repo.get_recent(limit)
