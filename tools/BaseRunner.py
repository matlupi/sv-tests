import subprocess
import shutil


class BaseRunner:
    """Common base class shared by all runners
    Each runner must either implement prepare_run_cb
    or override the run method.

    prepare_run_cb is responsible for generating command to run
    and preparing the command working directory if required by the tool.

    Runners must be located in tools/runners subdirectory
    to be detected and launched by the Makefile.
    """

    def __init__(self, name, executable=None):
        """Base runner class constructor
        Arguments:
        name -- runner name.
        executable -- name of an executable used by the particular runner
        can be omitted if default can_run method isn't used.
        """
        self.name = name
        self.executable = executable

        self.url = "https://github.com/symbiflow/sv-tests"

    def run(self, tmp_dir, params):
        """Run the provided test case
        This method is called by the main runner script (tools/runner).

        Arguments:
        tmp_dir -- temporary directory created for this test run.
        params -- dictionary with all metadata from the test file.
                  All keys are used without colons, ie. :tags: becomes tags.

        Returns a tuple containing command execution log and return code.
        """
        self.prepare_run_cb(tmp_dir, params)

        proc = subprocess.Popen(self.cmd, cwd=tmp_dir,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        log, _ = proc.communicate()

        return (log.decode('utf-8'), proc.returncode)

    def can_run(self):
        """Check if runner can be used
        This method is called by the main runner script (tools/runner) as
        a sanity check to verify that tool used by the runner is properly
        installed.

        Returns True when tool is installed and can be used, False otherwise.
        """
        return shutil.which(self.executable) is not None
