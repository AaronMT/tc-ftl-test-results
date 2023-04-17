import xml

from beautifultable import BeautifulTable
from junitparser import Attr, Failure, JUnitXml, TestSuite


class _TestSuite(TestSuite):
    flakes = Attr()


def _parse_print_failure_results(results):
    table = BeautifulTable()
    table.columns.header = (['UI Test', 'Outcome'])

    for suite in results:
        cur_suite = _TestSuite.fromelem(suite)
        if cur_suite.flakes != '0':
            for case in suite:
                if case.result:
                    table.rows.append(
                        ["%s#%s" % (case.classname, case.name), "Flaky"])
        else:
            for case in suite:
                for entry in case.result:
                    if isinstance(entry, Failure):
                        table.rows.append(
                            ["%s#%s" % (case.classname, case.name), "Failure"])
                        break
    print(table)


def _load_results_file(filename):
    ret = None
    try:
        f = open(filename, 'r')
        try:
            ret = JUnitXml.fromfile(f)
        except xml.etree.ElementTree.ParseError as e:
            print(f'Error parsing {filename} file: {e}')
        finally:
            f.close()
    except IOError as e:
        print(e)

    return ret


def main():
    junitxml = _load_results_file('FullJUnitReport.xml')
    if junitxml:
        _parse_print_failure_results(junitxml)


if __name__ == '__main__':
    main()
