import json
from collections import OrderedDict

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class JSONFormatBear(Lint, LocalBear):
    try:
        DecodeError = json.decoder.JSONDecodeError
    except:
        DecodeError = ValueError

    diff_message = ("This file can be reformatted by sorting keys and "
                    "following indentation.")
    gives_corrected = True

    def lint(self, filename, file, **kwargs):
        try:
            json_content = json.loads(''.join(file),
                                      object_pairs_hook=OrderedDict)
        except self.DecodeError as err:
            return [Result.from_values(
                self,
                "This file does not contain parsable JSON. '{adv_msg}'"
                .format(adv_msg=str(err)),
                file=filename)]

        new_file = json.dumps(json_content, **kwargs).splitlines(True)
        # Because of a bug in several python versions we have to correct
        # whitespace here.
        output = [line.rstrip(" \n")+"\n" for line in new_file]
        return self.process_output(output, filename, file)

    def run(self,
            filename,
            file,
            json_sort: bool=False,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        """
        Raises issues for any deviations from the pretty-printed JSON.

        :param json_sort: Whether or not keys should be sorted.
        :param tab_width: Number of spaces to indent.
        """
        return self.lint(filename,
                         file,
                         sort_keys=json_sort,
                         indent=tab_width)
