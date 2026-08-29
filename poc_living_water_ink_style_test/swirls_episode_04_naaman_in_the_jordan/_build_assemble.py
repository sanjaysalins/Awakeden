import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from swirls_assemble import assemble  # noqa: E402
from episode import MANIFEST  # noqa: E402

result = assemble(MANIFEST, "piano")
print(result)
