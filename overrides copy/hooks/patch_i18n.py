"""MkDocs hook that hides the blog files from the i18n plugin

MIT Licence 2024 Kamil Krzyśków (HRY) for Gothic Modding Community (https://gothic-modding-community.github.io/)
"""

from mkdocs import plugins
from mkdocs.structure.files import Files


BLOG_FILES = None
"""
List of files that belong to a blog. They will be temporarily removed and added back to hide them
from the i18n plugin. Set later for mkdocs serve to work properly.
"""

@plugins.event_priority(-95)
def _on_files_disconnect_blog_files(files: Files, config, *_, **__):
    """Disconnect blog files before on_files from the i18n plugin runs (-100) after blog (-50)"""
    global BLOG_FILES
    BLOG_FILES = []
    non_blog_files: list[File] = []
    blog_prefixes = []

    for name, instance in config.plugins.items():
        if name.startswith("material/blog"):
            blog_prefixes.append(instance.config.blog_dir)

    blog_prefixes = tuple(map(lambda x: x.rstrip("/") + "/", blog_prefixes))

    # i18n blog prefix awareness can be used in overrides templates
    config.extra.i18n_blog_prefixes = blog_prefixes

    for file in files:
        if file.src_uri.startswith(blog_prefixes):
            BLOG_FILES.append(file)
        else:
            non_blog_files.append(file)

    return Files(non_blog_files)


@plugins.event_priority(-105)
def _on_files_connect_blog_files(files: Files, *_, **__):
    """Breaking the convention of a minimal -100. Restore blog files after i18n on_files"""
    for file in BLOG_FILES:
        files.append(file)

    return files


on_files = plugins.CombinedEvent(_on_files_disconnect_blog_files, _on_files_connect_blog_files)
