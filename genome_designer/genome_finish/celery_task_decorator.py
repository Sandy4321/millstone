from functools import wraps
import os
import traceback

from main.models import ExperimentSampleToAlignment


def set_assembly_status(sample_alignment, status, force=False):
    """Sets assembly status field.
    """
    sample_alignment = ExperimentSampleToAlignment.objects.get(
            uid=sample_alignment.uid)

    # Make sure assembly status is not FAILED
    if not force:
        assert sample_alignment.data.get('assembly_status') != (
                ExperimentSampleToAlignment.ASSEMBLY_STATUS.FAILED)

    # Set assembly status for UI
    sample_alignment.data['assembly_status'] = status
    sample_alignment.save()


def get_failure_report_path(sample_alignment, report_filename):
    """Returns full path to given report for ExperimentSampleToAlignment.
    """
    return os.path.join(sample_alignment.get_model_data_dir(), report_filename)


def report_failure_stats(file_name):
    """Decorator that writes to file the traceback and exception of the
    decorated function, which must have one argument that is an instance
    of the ExperimentSampleToAlignment model class that it will set the
    assembly status of to failed
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Asserts that should fail at beginning of run that should be
            # caught at development/test time.
            assert len(args) >= 1
            sample_alignment_args = [arg for arg in args if
                    isinstance(arg, ExperimentSampleToAlignment)]
            assert len(sample_alignment_args) == 1
            sample_alignment = sample_alignment_args[0]

            try:
                return func(*args, **kwargs)
            except Exception as exc:
                # Set assembly status to FAILED
                set_assembly_status(
                        sample_alignment,
                        ExperimentSampleToAlignment.ASSEMBLY_STATUS.FAILED,
                        force=True)

                # Write exception with traceback to file
                tb = traceback.format_exc()
                file_path = get_failure_report_path(sample_alignment, file_name)
                with open(file_path, 'w') as fh:
                    fh.write('tracback:%s\nexception:%r' % (tb, exc))

                # NOTE: Do not raise the exception so that the rest of the
                # pipeline can proceed.

        return wrapper
    return decorator
