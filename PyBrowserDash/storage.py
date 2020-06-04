from whitenoise.storage import CompressedStaticFilesStorage


class WhiteNoiseStaticFilesStorage(CompressedStaticFilesStorage):
    """Prevent admin storage errors when DEBUG = False in settings."""

    manifest_strict = False
