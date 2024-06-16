import contextlib
import io
import logging
import os
import tempfile

import machine
import pytest
import translator


@pytest.mark.golden_test("../golden/*.yml")
def test_cpu(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdir:
        source = os.path.join(tmpdir, "source.asm")
        input_data = os.path.join(tmpdir, "input.txt")
        target = os.path.join(tmpdir, "target.json")

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["source"])

        with open(input_data, "w", encoding="utf-8") as file:
            file.write(golden["in"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main([None, source, target])
            machine.main([None, target, input_data])

        with open(target, encoding="utf-8") as file:
            code = file.read()

        assert code == golden.out["out_code"]
        assert stdout.getvalue() == golden.out["out"]
        assert caplog.text == golden.out["log"]
