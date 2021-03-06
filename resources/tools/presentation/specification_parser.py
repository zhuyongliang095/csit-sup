# Copyright (c) 2017 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Specification

Parsing of the specification YAML file.
"""


import logging
from yaml import load, YAMLError
from pprint import pformat

from errors import PresentationError


class Specification(object):
    """Specification of Presentation and analytics layer.

    - based on specification specified in the specification YAML file
    - presentation and analytics layer is model driven
    """

    # Tags are used in specification YAML file and replaced while the file is
    # parsed.
    TAG_OPENER = "{"
    TAG_CLOSER = "}"

    def __init__(self, cfg_file):
        """Initialization.

        :param cfg_file: File handler for the specification YAML file.
        :type cfg_file: BinaryIO
        """
        self._cfg_file = cfg_file
        self._cfg_yaml = None

        self._specification = {"environment": dict(),
                               "configuration": dict(),
                               "debug": dict(),
                               "static": dict(),
                               "input": dict(),
                               "output": dict(),
                               "tables": list(),
                               "plots": list(),
                               "files": list()}

    @property
    def specification(self):
        """Getter - specification.

        :returns: Specification.
        :rtype: dict
        """
        return self._specification

    @property
    def environment(self):
        """Getter - environment.

        :returns: Environment specification.
        :rtype: dict
        """
        return self._specification["environment"]

    @property
    def configuration(self):
        """Getter - configuration.

        :returns: Configuration of PAL.
        :rtype: dict
        """
        return self._specification["configuration"]

    @property
    def static(self):
        """Getter - static content.

        :returns: Static content specification.
        :rtype: dict
        """
        return self._specification["static"]

    @property
    def debug(self):
        """Getter - debug

        :returns: Debug specification
        :rtype: dict
        """
        return self._specification["debug"]

    @property
    def is_debug(self):
        """Getter - debug mode

        :returns: True if debug mode is on, otherwise False.
        :rtype: bool
        """

        try:
            if self.environment["configuration"]["CFG[DEBUG]"] == 1:
                return True
            else:
                return False
        except KeyError:
            return False

    @property
    def input(self):
        """Getter - specification - inputs.
        - jobs and builds.

        :returns: Inputs.
        :rtype: dict
        """
        return self._specification["input"]

    @property
    def builds(self):
        """Getter - builds defined in specification.

        :returns: Builds defined in the specification.
        :rtype: dict
        """
        return self.input["builds"]

    @property
    def output(self):
        """Getter - specification - output formats and versions to be generated.
        - formats: html, pdf
        - versions: full, ...

        :returns: Outputs to be generated.
        :rtype: dict
        """
        return self._specification["output"]

    @property
    def tables(self):
        """Getter - tables to be generated.

        :returns: List of specifications of tables to be generated.
        :rtype: list
        """
        return self._specification["tables"]

    @property
    def plots(self):
        """Getter - plots to be generated.

        :returns: List of specifications of plots to be generated.
        :rtype: list
        """
        return self._specification["plots"]

    @property
    def files(self):
        """Getter - files to be generated.

        :returns: List of specifications of files to be generated.
        :rtype: list
        """
        return self._specification["files"]

    def set_input_state(self, job, build_nr, state):
        """Set the state of input

        :param job:
        :param build_nr:
        :param state:
        :return:
        """

        try:
            for build in self._specification["input"]["builds"][job]:
                if build["build"] == build_nr:
                    build["status"] = state
                    break
            else:
                raise PresentationError("Build '{}' is not defined for job '{}'"
                                        " in specification file.".
                                        format(build_nr, job))
        except KeyError:
            raise PresentationError("Job '{}' and build '{}' is not defined in "
                                    "specification file.".format(job, build_nr))

    def set_input_file_name(self, job, build_nr, file_name):
        """Set the state of input

        :param job:
        :param build_nr:
        :param file_name:
        :return:
        """

        try:
            for build in self._specification["input"]["builds"][job]:
                if build["build"] == build_nr:
                    build["file-name"] = file_name
                    break
            else:
                raise PresentationError("Build '{}' is not defined for job '{}'"
                                        " in specification file.".
                                        format(build_nr, job))
        except KeyError:
            raise PresentationError("Job '{}' and build '{}' is not defined in "
                                    "specification file.".format(job, build_nr))

    def _get_type_index(self, item_type):
        """Get index of item type (environment, input, output, ...) in
        specification YAML file.

        :param item_type: Item type: Top level items in specification YAML file,
        e.g.: environment, input, output.
        :type item_type: str
        :returns: Index of the given item type.
        :rtype: int
        """

        index = 0
        for item in self._cfg_yaml:
            if item["type"] == item_type:
                return index
            index += 1
        return None

    def _find_tag(self, text):
        """Find the first tag in the given text. The tag is enclosed by the
        TAG_OPENER and TAG_CLOSER.

        :param text: Text to be searched.
        :type text: str
        :returns: The tag, or None if not found.
        :rtype: str
        """
        try:
            start = text.index(self.TAG_OPENER)
            end = text.index(self.TAG_CLOSER, start + 1) + 1
            return text[start:end]
        except ValueError:
            return None

    def _replace_tags(self, data, src_data=None):
        """Replace tag(s) in the data by their values.

        :param data: The data where the tags will be replaced by their values.
        :param src_data: Data where the tags are defined. It is dictionary where
        the key is the tag and the value is the tag value. If not given, 'data'
        is used instead.
        :type data: str or dict
        :type src_data: dict
        :returns: Data with the tags replaced.
        :rtype: str or dict
        :raises: PresentationError if it is not possible to replace the tag or
        the data is not the supported data type (str, dict).
        """

        if src_data is None:
            src_data = data

        if isinstance(data, str):
            tag = self._find_tag(data)
            if tag is not None:
                data = data.replace(tag, src_data[tag[1:-1]])

        elif isinstance(data, dict):
            counter = 0
            for key, value in data.items():
                tag = self._find_tag(value)
                if tag is not None:
                    try:
                        data[key] = value.replace(tag, src_data[tag[1:-1]])
                        counter += 1
                    except KeyError:
                        raise PresentationError("Not possible to replace the "
                                                "tag '{}'".format(tag))
            if counter:
                self._replace_tags(data, src_data)
        else:
            raise PresentationError("Replace tags: Not supported data type.")

        return data

    def _parse_env(self):
        """Parse environment specification in the specification YAML file.
        """

        logging.info("Parsing specification file: environment ...")

        idx = self._get_type_index("environment")
        if idx is None:
            return None

        try:
            self._specification["environment"]["configuration"] = \
                self._cfg_yaml[idx]["configuration"]
        except KeyError:
            self._specification["environment"]["configuration"] = None

        try:
            self._specification["environment"]["paths"] = \
                self._replace_tags(self._cfg_yaml[idx]["paths"])
        except KeyError:
            self._specification["environment"]["paths"] = None

        try:
            self._specification["environment"]["urls"] = \
                self._replace_tags(self._cfg_yaml[idx]["urls"])
        except KeyError:
            self._specification["environment"]["urls"] = None

        try:
            self._specification["environment"]["make-dirs"] = \
                self._cfg_yaml[idx]["make-dirs"]
        except KeyError:
            self._specification["environment"]["make-dirs"] = None

        try:
            self._specification["environment"]["remove-dirs"] = \
                self._cfg_yaml[idx]["remove-dirs"]
        except KeyError:
            self._specification["environment"]["remove-dirs"] = None

        try:
            self._specification["environment"]["build-dirs"] = \
                self._cfg_yaml[idx]["build-dirs"]
        except KeyError:
            self._specification["environment"]["build-dirs"] = None

        logging.info("Done.")

    def _parse_configuration(self):
        """Parse configuration of PAL in the specification YAML file.
        """

        logging.info("Parsing specification file: configuration ...")

        idx = self._get_type_index("configuration")
        if idx is None:
            logging.warning("No configuration information in the specification "
                            "file.")
            return None

        try:
            self._specification["configuration"] = self._cfg_yaml[idx]
        except KeyError:
            raise PresentationError("No configuration defined.")

        logging.info("Done.")

    def _parse_debug(self):
        """Parse debug specification in the specification YAML file.
        """

        if int(self.environment["configuration"]["CFG[DEBUG]"]) != 1:
            return None

        logging.info("Parsing specification file: debug ...")

        idx = self._get_type_index("debug")
        if idx is None:
            self.environment["configuration"]["CFG[DEBUG]"] = 0
            return None

        try:
            for key, value in self._cfg_yaml[idx]["general"].items():
                self._specification["debug"][key] = value

            self._specification["input"]["builds"] = dict()
            for job, builds in self._cfg_yaml[idx]["builds"].items():
                if builds:
                    self._specification["input"]["builds"][job] = list()
                    for build in builds:
                        self._specification["input"]["builds"][job].\
                            append({"build": build["build"],
                                    "status": "downloaded",
                                    "file-name": self._replace_tags(
                                        build["file"],
                                        self.environment["paths"])})
                else:
                    logging.warning("No build is defined for the job '{}'. "
                                    "Trying to continue without it.".
                                    format(job))

        except KeyError:
            raise PresentationError("No data to process.")

    def _parse_input(self):
        """Parse input specification in the specification YAML file.

        :raises: PresentationError if there are no data to process.
        """

        logging.info("Parsing specification file: input ...")

        idx = self._get_type_index("input")
        if idx is None:
            raise PresentationError("No data to process.")

        try:
            for key, value in self._cfg_yaml[idx]["general"].items():
                self._specification["input"][key] = value
            self._specification["input"]["builds"] = dict()
            for job, builds in self._cfg_yaml[idx]["builds"].items():
                if builds:
                    self._specification["input"]["builds"][job] = list()
                    for build in builds:
                        self._specification["input"]["builds"][job].\
                            append({"build": build, "status": None})
                else:
                    logging.warning("No build is defined for the job '{}'. "
                                    "Trying to continue without it.".
                                    format(job))
        except KeyError:
            raise PresentationError("No data to process.")

        logging.info("Done.")

    def _parse_output(self):
        """Parse output specification in the specification YAML file.

        :raises: PresentationError if there is no output defined.
        """

        logging.info("Parsing specification file: output ...")

        idx = self._get_type_index("output")
        if idx is None:
            raise PresentationError("No output defined.")

        try:
            self._specification["output"] = self._cfg_yaml[idx]["format"]
        except KeyError:
            raise PresentationError("No output defined.")

        logging.info("Done.")

    def _parse_static(self):
        """Parse specification of the static content in the specification YAML
        file.
        """

        logging.info("Parsing specification file: static content ...")

        idx = self._get_type_index("static")
        if idx is None:
            logging.warning("No static content specified.")

        for key, value in self._cfg_yaml[idx].items():
            if isinstance(value, str):
                try:
                    self._cfg_yaml[idx][key] = self._replace_tags(
                        value, self._specification["environment"]["paths"])
                except KeyError:
                    pass

        self._specification["static"] = self._cfg_yaml[idx]

        logging.info("Done.")

    def _parse_elements(self):
        """Parse elements (tables, plots) specification in the specification
        YAML file.
        """

        logging.info("Parsing specification file: elements ...")

        count = 1
        for element in self._cfg_yaml:
            try:
                element["output-file"] = self._replace_tags(
                    element["output-file"],
                    self._specification["environment"]["paths"])
            except KeyError:
                pass

            # add data sets to the elements:
            if isinstance(element.get("data", None), str):
                data_set = element["data"]
                try:
                    element["data"] = self.configuration["data-sets"][data_set]
                except KeyError:
                    raise PresentationError("Data set {0} is not defined in "
                                            "the configuration section.".
                                            format(data_set))

            if element["type"] == "table":
                logging.info("  {:3d} Processing a table ...".format(count))
                try:
                    element["template"] = self._replace_tags(
                        element["template"],
                        self._specification["environment"]["paths"])
                except KeyError:
                    pass
                self._specification["tables"].append(element)
                count += 1

            elif element["type"] == "plot":
                logging.info("  {:3d} Processing a plot ...".format(count))

                # Add layout to the plots:
                layout = element["layout"].get("layout", None)
                if layout is not None:
                    element["layout"].pop("layout")
                    try:
                        for key, val in (self.configuration["plot-layouts"]
                                         [layout].items()):
                            element["layout"][key] = val
                    except KeyError:
                        raise PresentationError("Layout {0} is not defined in "
                                                "the configuration section.".
                                                format(layout))
                self._specification["plots"].append(element)
                count += 1

            elif element["type"] == "file":
                logging.info("  {:3d} Processing a file ...".format(count))
                try:
                    element["dir-tables"] = self._replace_tags(
                        element["dir-tables"],
                        self._specification["environment"]["paths"])
                except KeyError:
                    pass
                self._specification["files"].append(element)
                count += 1

        logging.info("Done.")

    def read_specification(self):
        """Parse specification in the specification YAML file.

        :raises: PresentationError if an error occurred while parsing the
        specification file.
        """
        try:
            self._cfg_yaml = load(self._cfg_file)
        except YAMLError as err:
            raise PresentationError(msg="An error occurred while parsing the "
                                        "specification file.",
                                    details=str(err))

        self._parse_env()
        self._parse_configuration()
        self._parse_debug()
        if not self.debug:
            self._parse_input()
        self._parse_output()
        self._parse_static()
        self._parse_elements()

        logging.debug("Specification: \n{}".
                      format(pformat(self._specification)))
