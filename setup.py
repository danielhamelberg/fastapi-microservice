from setuptools import setup, find_packages

def setup_package():
	"""
	Set up the package with the required dependencies.

	This function uses setuptools to define the package name, version, packages, and install requirements.
	The package name is set to "fastapi-microservice" and the version is set to "0.1.0".
	The packages are automatically discovered using the find_packages() function.
	The install_requires list specifies the required dependencies for the package.

	Returns:
		None
	"""
	setup(
		name="fastapi-microservice",
		version="0.1.0",
		packages=find_packages(),
		install_requires=[
			"fastapi",
			"uvicorn",
			"sqlalchemy",
			"pydantic",
			"python-dotenv",
			"psycopg2-binary",
			"alembic",
			"passlib",
			"python-jose",
			"python-multipart",
			"pyjwt",
			"bcrypt",
		],
	)

setup_package()
