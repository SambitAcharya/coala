import hashlib
import pickle
import os

from coalib.misc import Constants


def get_tags_dir(log_printer):
    try:
        os.makedirs(Constants.TAGS_DIR, exist_ok=True)
        return Constants.TAGS_DIR
    except PermissionError:
        log_printer.err("Unable to create tags directory '{}'. Continuing "
                        "without tagging.".format(Constants.TAGS_DIR))
    return None


def get_tag_path(tag, project, log_printer):
    """
    Creates a hash value that is used for tagging and creates a path for it.

    :param tag:         The name for the tag.
    :param project:     The related coafile.
    :param log_printer: The logger which logs errors.
    :return:            A path containing a hash as filename that identifies the
                        given parameters.
    """
    path = os.path.join(project, tag)
    hash = hashlib.sha224(path.encode()).hexdigest()
    tags_dir = get_tags_dir(log_printer)
    if not tags_dir is None:
        return os.path.join(tags_dir, hash)
    return None


def tag_results(tag, project, results, log_printer):
    """
    This method takes a tag provided from the user and saves the results
    dictionary output by coala to a file. That file is uniquely identified by
    the combined hash of the project (i.e. coafile) and the provided tag.

    :param tag:         Tag provided by user.
    :param project:     Path to the coafile the results belong to.
    :param log_printer: The logger which logs errors.
    :param results:     Results dictionary generated by coala.
    """
    if tag == "None":
        return
    tag_path = get_tag_path(tag, project, log_printer)
    if not tag_path is None:
        with open(tag_path, 'wb+') as file:
            pickle.dump(results, file)


def load_tagged_results(tag, project, log_printer):
    """
    Retrieves results previously stored with tag_results.

    :param tag:         The tag name.
    :param project:     Path to the coafile the results belong to.
    :param log_printer: The logger which logs errors.
    :return:            A results dictionary, as generated by coala.
    """
    if tag == "None":
        return None
    tag_path = get_tag_path(tag, project, log_printer)
    if not tag_path is None:
        with open(tag_path, 'rb') as file:
            return pickle.load(file)
    return None


def delete_tagged_results(tag, project, log_printer):
    """
    Deletes previously tagged results.

    :param tag:         The tag name.
    :param project:     Path to the coafile the results belong to.
    :param log_printer: The logger which logs errors.
    """
    if tag == "None":
        return
    tag_path = get_tag_path(tag, project, log_printer)
    if not tag_path is None and os.path.exists(tag_path):
        os.remove(tag_path)
