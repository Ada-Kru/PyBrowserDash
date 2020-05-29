from whitenoise.storage import CompressedManifestStaticFilesStorage


class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Prevent admin storage errors when DEBUG = False in settings."""

    manifest_strict = False
