# sleep-parameters
Calculates common sleep parameters defined by AASM



## Development

### Prerequisites

poetry (https://github.com/sdispater/poetry)

Remark: this includes, that @python@ and @pip@ need to call the desired version, e.g. by setting symlinks in .local/bin or whatever directory in your PATH

python3-venv
python3-pip

Account in pypi.org

### Download

@git clone https://github.com/somnonetz/sleep-parameters/@

### Test

```bash
cd sleep-parameters
poetry install
poetry run python tests/test_sn_run_sleep_parameters_class.py
```

### Build new version

Increment version number in pyproject.toml

```
git add --all
git commit -m "version xxx,blabla"
git push
poetry build
poetry publish
git tag -a "v0.x.0"
git push --tag
```

