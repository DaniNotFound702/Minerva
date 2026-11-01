_api_wrapper_key = None


def configure_api_wrapper(api_key):
	"""Configure the API wrapper without editing Minerva's files or .env."""
	if not isinstance(api_key, str) or not api_key.strip():
		raise ValueError("api_key must be a non-empty string")

	global _api_wrapper_key
	_api_wrapper_key = api_key


def get_api_wrapper_key():
	return _api_wrapper_key
